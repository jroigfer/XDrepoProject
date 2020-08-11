from unittest import TestCase

from git import Repo
from src import updateRepo
import logging, os, urllib
import time
import git

# Logging config from file
file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, '../resources/logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger('dev')
logger.info('Logging actived!')

class TestReadRepo(TestCase):

    def test_readRepo(self):
        reposList = updateRepo.getRepos()
        for element in reposList:
            print("name: " + element['name'])
        print("size: " + repr(len(reposList)))
        self.assertGreater(len(reposList),1)

    def test_readAddons(self):
        addonsList = updateRepo.getAddons()
        for element in addonsList:
            print("name: " + element['name'])
        print("size: " + repr(len(addonsList)))
        self.assertGreater(len(addonsList), 1)

    def test_getReposContent(self):
        updateRepo.getReposContent()

    def test_getNoGitAddons(self):
        updateRepo.getNoGitAddons()

    def test_extrcatAndCleanZipNoGit(self):
        updateRepo.extractFilesFromZip()
        updateRepo.cleanFilesExtarctedFromZip()
        updateRepo.moveZipFilesToFolders()

    def test_createXDRepo(self):
        updateRepo.moveGitAddonToXDRepo()
        updateRepo.moveNoGitAddonToXDRepo()

    def test_createRepoXD_comp(self):
        updateRepo.createRepoXD()

    def test_copyFiles(self):
        updateRepo.copyGettedAddonFolderFilestoRepoFolder()

    def test(self):
        test = ""
        if not test:
            print("vacio!")
        else:
            print("no vacio")

    def test2(self):
        test = "hola.zip"
        print(test[:-4])
        test2 = "hola-1.1.1.zip"
        pos = test2.find("-")
        print(test2[:pos])
        item = "hola-1.1.1.zip"
        print("dig: " + item[item.find("-")+1:item.find("-") + 2])
        print(item[item.find("-")+1:item.find("-") + 2].isdigit())

    def testDate(self):
        print("time:" + time.strftime("%Y.%m.%d"))
        print("time:" + time.strftime("%Y.%m"))
        print("time:" + time.strftime("%Y"))
        print(time.strftime("%Y")[2:3])
        print(time.strftime("%Y")[3:4])

    def test_repoDiff(self):
        repo = Repo('/home/jroigfer/Documentos/gitemp')
        print("unt" + repr(repo.untracked_files))
        print("diff" + repr(repo.index.diff("HEAD")))
        print("test2" + repr(repo.index.diff(None)))
        #t = repo.head.commit.tree
        #repo.git.diff(t)

    def test_moreoneli(self):
        extraInfo = "<li><a href=\";\">"
        urlBase = "http://kodiadictos.org/kodiadictos/Addons%20Deportes/dependencias.1x2/"

        fp = urllib.request.urlopen("http://kodiadictos.org/kodiadictos/Addons%20Deportes/dependencias.1x2/")
        # fp = urllib.request.urlopen(urllib.parse.urlparse(element['addonFolder']))
        bytesPage = fp.read()
        pageStr = bytesPage.decode("utf8")
        fp.close()

        infoScrap = extraInfo.split(";")
        numOc = pageStr.find(infoScrap[0], 0)
        ini = 0
        while (numOc > 0):
            posIni = pageStr.find(infoScrap[0], ini)
            posFin = pageStr.find(infoScrap[1], posIni + len(infoScrap[0]))
            ini = pageStr.find("</a></li>",posFin) + len("</a></li>")
            href = urlBase + pageStr[posIni:posFin + len(infoScrap[1])].split('"')[1]
            numOc = pageStr.find(infoScrap[0], ini)
            print("dep: " + href)
