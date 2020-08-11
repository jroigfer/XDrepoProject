import os
import os.path
import shutil
import sys
import datetime, time, timedelta

def removeTfiles():
    # find REC -type f -name 't*.*' -delete
    print("hola")

def splitExistOrReover():
    #source = sys.argv[1]
    #destination = sys.argv[2]
    source = "/media/jroigfer/discExtern250/RECINM42020"
    destinationDeleted = "/media/jroigfer/temp/REC INM 2020/deleted"
    destinationExisted = "/media/jroigfer/temp/REC INM 2020/existed"

    #while not os.path.exists(source):
    #    source = raw_input('Enter a valid source directory\n')
    #while not os.path.exists(destination):
    #    destination = raw_input('Enter a valid destination directory\n')

    for root, dirs, files in os.walk(source, topdown=False):
        for file in files:
            extension = os.path.splitext(file)[1][1:].upper()
            try:
                mtime = os.path.getmtime(file)
            except OSError:
                mtime = 0
            last_modified_date = datetime.datetime.fromtimestamp(mtime)

            time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(file)))
            print("Last Modified Time 1 : ", last_modified_date)

            timeNow = datetime.datetime.now() - datetime.timedelta(days=7)
            if last_modified_date < timeNow:
                print("file " + file + " ORIGINAL " + repr(last_modified_date))
            else:
                print("RECUPERADA " + repr(last_modified_date))


            #modificationTime = last_modified_date.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
           # print("Last Modified Time 2 : ", modificationTime)

                #shutil.copy2(os.path.join(root, file), destinationPath)

# OJO - priemr se debe crear carpeta deleted existed y rep
def splitExistOrReover():
    #source = "/media/jroigfer/temp/REC INM 2020"
    source = "/media/jroigfer/temp_part/REC2/"

    #destinationDeleted = "/media/jroigfer/temp/REC INM 2020/deleted"
    #destinationExisted = "/media/jroigfer/temp/REC INM 2020/existed"

    destinationDeleted = source + "deleted"
    destinationExisted = source + "existed"
    destinationRepe = source + "rep"

    if not os.path.exists(source + "/existed"):
        os.mkdir(source + "/existed")
    if not os.path.exists(source + "/deleted"):
        os.mkdir(source + "/deleted")
    if not os.path.exists(source + "/rep"):
        os.mkdir(source + "/rep")

    countBasicFold = 0
    for addonFolder in os.listdir(source):
        print("fold: " + addonFolder)
        if addonFolder == "deleted" or addonFolder == "existed" or addonFolder == "rep":
            countBasicFold = countBasicFold + 1

    if countBasicFold == 3:
        for addonFolder in os.listdir(source):
            print("fold: " + addonFolder)
            if addonFolder == "deleted" or addonFolder == "existed" or addonFolder == "rep":
                print("no " + addonFolder)
            else:
                for fileRec in os.listdir(source + "/" + addonFolder):
                    print("file rec " + addonFolder + "/" + fileRec)
                    fileOrigComp = source + "/" + addonFolder + "/" + fileRec

                    last_modified_date = time.gmtime(os.path.getmtime(fileOrigComp))
                    last_modified_date_str = time.strftime('%d/%m/%Y', last_modified_date)
                    #last_modified_date = datetime.datetime.fromtimestamp(last_modified_date)
                    print("Last Modified Time 1 : ", last_modified_date_str)
                    fileDateM = datetime.datetime.fromtimestamp(os.path.getmtime(fileOrigComp)).date()

                    timeLastWeek = datetime.datetime.now() - datetime.timedelta(days=7)
                    if fileDateM < timeLastWeek.date():
                        print("EXIS: " + fileRec + " ORIGINAL " + repr(last_modified_date))
                        if not os.path.isfile(destinationExisted + "/" + fileRec):
                            shutil.move(fileOrigComp, destinationExisted)
                        else:
                            shutil.move(fileOrigComp, destinationRepe)
                    else:
                        print("BORR: " + fileRec + " ORIGINAL " + repr(last_modified_date))
                        if not os.path.isfile(destinationDeleted + "/" + fileRec):
                            shutil.move(fileOrigComp, destinationDeleted)
                        else:
                            shutil.move(fileOrigComp, destinationRepe)
    else:
        print("no estan las carpetas basicas!")

# OJO - priemr se debe crear carpeta deleted existed y rep
def organizeInYears():
    source = "/media/jroigfer/temp_part/REC2/"

    origin = source + "existed"
    destinationExisted = source + "existed/years"

    if not os.path.exists(destinationExisted):
        os.mkdir(destinationExisted)
        print("created %s" % (destinationExisted))

    for fileRec in os.listdir(origin):
        if fileRec.endswith("years"):
            print("descarted year folder")
        else:
            fileOrigComp = origin + "/" + fileRec

            last_modified_date = time.gmtime(os.path.getmtime(fileOrigComp))
            year = time.strftime('%Y', last_modified_date)
            pathyear = destinationExisted + "/" + year

            if not os.path.exists(pathyear):
                os.mkdir(pathyear)
                print("created %s" % (pathyear))

            print("move from %s to %s" % (fileOrigComp,pathyear))
            shutil.move(fileOrigComp, pathyear)

if __name__ == '__main__':
    splitExistOrReover()
    organizeInYears()