from json import load

from dto.repo import Repo
from dto.kodiAddon import KodiAddon
from services.xmlAddonGenerator import Generator
from zipfile import ZipFile
import json, sys, os, git, urllib.request, urllib.parse, wget, glob, zipfile, shutil, logging, logging.config

# Logging config from file
file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'resources/logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger('dev')
logger.info('Logging actived!')

# global variables
rootDir = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
reposGitTargetFolder = "/mnt/comun/temp/kodirepotest/"
addonNoGitTargetFolder = "/mnt/comun/temp/kodiaddontest/"
xDevRepoTargetFolderTemp = "/mnt/comun/temp/xdevrepotest/"
xDevRepoTargetFolder = "/mnt/comun/git-repos/github/XDKodiRepo/"

def createRepoXD():
    #clean addon no git temp folder
    logging.info('Starting repo XD creation...')

    logging.info('Clean temporal folders')
    cleanFolder(reposGitTargetFolder)
    cleanFolder(addonNoGitTargetFolder)
    cleanFolder(xDevRepoTargetFolderTemp)

    logging.info('Getting Git repos for addons first')
    getGitReposContent()

    logging.info('Downloading and constructing no git addons')
    dowloadNoGitAddons()
    extractFilesFromZip()
    cleanFilesExtarctedFromZip()
    moveZipFilesToFolders()

    logging.info('Moving folders getted to repo XD folder')
    moveGitAddonToXDRepo()
    moveNoGitAddonToXDRepo()

    logging.info('Finished repo XD creation...')

    # close logging handlers
    #for handler in logConfig.handlers:
    #    handler.close()
    #    logConfig.removeFilter(handler)

def getGitReposContent():
    for repo in getRepos():
        if repo['git']:
            logging.info("git repo " + repo['name'] + ", cloning...")
            try:
                git.Repo.clone_from(repo['repo'], reposGitTargetFolder + repo['name'])
            except Exception as e:
                # error perform git clone to repo
                logger.error("Calling to clone git repo %s failed" % (repo['repo'], e,))
        else:
            logging.info("no git: " + repo['name'])

def dowloadNoGitAddons():
    for addon in getAddons():
        if not addon['extraInfo'] == "":
            logging.info("not git addon " + addon['name'] + ", url: " + addon['addonFolder'])

            #solution in error with a space character in path param in kodiadictos Addon Deportes
            if " " in addon['addonFolder']:
                rep = urllib.parse.quote(" ")
                urldef = addon['addonFolder'].replace(" ",rep)
            else:
                urldef = addon['addonFolder']
            try:
                fp = urllib.request.urlopen(urldef)
                #fp = urllib.request.urlopen(urllib.parse.urlparse(element['addonFolder']))
                bytesPage = fp.read()
                pageStr = bytesPage.decode("utf8")
                fp.close()

                urlAddon = getHrefAddon(addon['addonFolder'],pageStr,addon['extraInfo'])
                logging.info("addon href content extracted: " + urlAddon)

                #OK
                wget.download(urlAddon,out=addonNoGitTargetFolder)
            except Exception as e:
                # error calling repo no git url
                logger.info("Call to %s failed" % (urldef, e,))
        else:
            logging.info("git addon " + addon['name'] + ", nothing to do")

#Unzip no git downloaded files
def extractFilesFromZip():
    os.chdir(addonNoGitTargetFolder)  # change directory from working dir to dir with files

    for item in os.listdir(addonNoGitTargetFolder):  # loop through items in dir
        if item.endswith(".zip"):  # check for ".zip" extension
            fileName = os.path.abspath(item)  # get full path of files
            zipRef = zipfile.ZipFile(fileName)  # create zipfile object
            zipRef.extractall(addonNoGitTargetFolder)  # extract file to dir
            zipRef.close()  # close file

    logging.info("extracted zip content from no git addons")

#remove files unneeded in addons folders
def cleanFilesExtarctedFromZip():
    #get folders of addons)
    for addonFolder in os.listdir(addonNoGitTargetFolder):
        addonFolderAbs = addonNoGitTargetFolder + addonFolder
        if os.path.isdir(addonFolderAbs):
            for fileName in os.listdir(addonFolderAbs):
                if not fileName.startswith('fanart.') and not fileName.startswith('icon.') and not fileName.startswith(
                        'changelog.') and not fileName.startswith('addon.xml'):
                    logging.debug(repr("file/folder deleted: " + addonFolderAbs + "/" + fileName))
                    fileInAddon = addonFolderAbs + "/" + fileName
                    if os.path.isdir(fileInAddon):
                        shutil.rmtree(fileInAddon)
                    else:
                        os.remove(fileInAddon)

def moveZipFilesToFolders():
    os.chdir(addonNoGitTargetFolder)  # change directory from working dir to dir with files

    for item in os.listdir(addonNoGitTargetFolder):  # loop through items in dir
        if item.endswith(".zip"):
            #if contains - and a number after them
            if ("-" in item and item[item.find("-") + 1:item.find("-") + 2].isdigit()):
                pos = item.find("-")
                shutil.move(addonNoGitTargetFolder + item,addonNoGitTargetFolder + item[:pos] + "/" + item)
                logging.debug("moved zip with version in name: " + item)
            else:
                shutil.move(addonNoGitTargetFolder + item,addonNoGitTargetFolder + item[:-4] + "/" + item)
                logging.debug("moved zip without version in name: " + item)

def moveGitAddonToXDRepo():
    for addon in getAddons():
        if addon['extraInfo'] == "":
            if not addon['addonFolder'] == "":
                shutil.move(reposGitTargetFolder + addon['repo'] + "/" + addon['addonFolder'], xDevRepoTargetFolderTemp)
            elif not addon['addonRepoFolder'] == "":
                shutil.move(reposGitTargetFolder + addon['repo'] + "/" + addon['addonRepoFolder'], xDevRepoTargetFolderTemp)

def moveNoGitAddonToXDRepo():
    for addonFolder in os.listdir(addonNoGitTargetFolder):
        addonFolderAbs = addonNoGitTargetFolder + addonFolder
        if os.path.isdir(addonFolderAbs):
            shutil.move(addonFolderAbs, xDevRepoTargetFolderTemp)

def getHrefAddon(urlBase,pageStr,extraInfo):
    infoScrap = extraInfo.split(";")
    posIni = pageStr.find(infoScrap[0], 0)
    posFin = pageStr.find(infoScrap[1], posIni + len(infoScrap[0]))
    href = urlBase + pageStr[posIni:posFin + len(infoScrap[1])].split('"')[1]
    logging.debug("href constructed: " + href)

    return href

# TODO - IMPORTANT fist execute git pull in dest repo and check if is not empty, and AFTER perform push with new num version of repo and new repo .zip
def copyGettedAddonFolderFilestoRepoFolder():
    os.chdir(xDevRepoTargetFolder)  # change directory from working dir to dir with files

    logging.info("begin the copy of getted addons folders and contents to target repo folder")
    for folderName in os.listdir(xDevRepoTargetFolderTemp):  # loop through items in dir
        pathFolder = xDevRepoTargetFolderTemp + folderName
        logging.debug("complet fodler item path: " + pathFolder)
        for fileName in os.listdir(pathFolder):
            logging.debug("file name:" + fileName)
            if not os.path.isdir(fileName) and not fileName.startswith("."):
                fileOrig = pathFolder + "/" + fileName
                fileDest = xDevRepoTargetFolder + folderName + "/" + fileName
                # Create folder dest if not exists
                if not os.path.exists(xDevRepoTargetFolder + folderName):
                    os.mkdir(xDevRepoTargetFolder + folderName)
                #os.makedirs(os.path.dirname(xDevRepoTargetFolder + folderName), exist_ok=True)
                shutil.copy(fileOrig,fileDest)
                logging.debug("orig file: " + fileOrig + "; des file: " + fileDest)
                logging.info("copied file: " + fileName)
            elif not os.path.isdir(fileName):
                logging.info("ignored (no folder) file: " + fileName)

# creation of general addon.xmlfile of the repo
def create_addon_xml_file():
    generatiorAddonXml = Generator(xDevRepoTargetFolder)
    generatiorAddonXml._generate_addons_files()

def cleanFolder(folder):
    files = glob.glob(folder + '/*')
    for f in files:
        if os.path.isdir(f):
            shutil.rmtree(f)
        else:
            os.remove(f)

#get json repo list
def getRepos():
    repoAddonsFile = os.path.join(rootDir, 'data/repo-addons.json')  # requires `import os`
    return json.loads(fileToString(repoAddonsFile))

#get json addons list
def getAddons():
    addonsFile = os.path.join(rootDir, 'data/addons.json')  # requires `import os`
    return json.loads(fileToString(addonsFile))

def fileToString(filepath):
    f = open(filepath, "r")
    result = f.read()
    f.close()
    return result

if __name__ == '__main__':
    createRepoXD()
    copyGettedAddonFolderFilestoRepoFolder()
    create_addon_xml_file()
