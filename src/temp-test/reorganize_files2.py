import os
import os.path
import shutil
import sys
import datetime, time, timedelta
import os

from pip._vendor.distlib.compat import raw_input


def removeTfiles():
    # find REC -type f -name 't*.*' -delete
    print("hola")

def splitExistOrReover():
    source = sys.argv[1]
    destination = sys.argv[2]
    #source = "/media/jroigfer/discExtern250/RECINM42020"
    #destinationDeleted = "/media/jroigfer/temp/REC INM 2020/deleted"
    #destinationExisted = "/media/jroigfer/temp/REC INM 2020/existed"

    while not os.path.exists(source):
        source = raw_input('Enter a valid source directory\n')
    while not os.path.exists(destination):
        destination = raw_input('Enter a valid destination directory\n')

    if not os.path.exists(source + "/existed"):
        os.mkdir(source + "/existed")
    if not os.path.exists(source + "/deleted"):
        os.mkdir(source + "/deleted")
    if not os.path.exists(source + "/rep"):
        os.mkdir(source + "/rep")






if __name__ == '__main__':
    splitExistOrReover()