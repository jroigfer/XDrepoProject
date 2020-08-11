"""
Please bump the version number one decimal point and add your name to credits when making changes.

This is an:
- addons.xml generator
- addons.xml.md5 generator
- optional auto-compressor (including handling of icons, fanart and changelog)

Compression of addons in repositories has many benefits, including:
 - Protects addon downloads from corruption.
 - Smaller addon filesize resulting in faster downloads and less space / bandwidth used on the repository.
 - Ability to "roll back" addon updates in XBMC to previous versions.

To enable the auto-compressor, set the compress_addons setting to True
NOTE: the settings.py of repository aggregator will override this setting.
If you do this you must make sure the "datadir zip" parameter in the addon.xml of your repository file is set to "true".
"""
import os
import shutil, logging, logging.config
from hashlib import md5
import zipfile
import re

# Logging config from file
file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, '../resources/logging.conf'), disable_existing_loggers=False)
logger = logging.getLogger('dev')
logger.info('Logging actived in xmlAddonGenerator!')

########## SETTINGS
# Set whether you want your addons compressed or not. Values are True or False
# NOTE: the settings.py of repository aggregator will override this
compress_addons = True

# Optional set a custom directory of where your addons are. False will use the current directory.
# NOTE: the settings.py of repository aggregator will override this
repo_root = False
########## End SETTINGS

## this function returns true if the object passed is a folder and ins't .git folder
def check_is_addon_dir(nameFolder):
    # this function is used by both classes.
    # very very simple and weak check that it is an addon dir.
    # intended to be fast, not totally accurate.
    # skip any file or .svn folder
    if not os.path.isdir(nameFolder) or nameFolder.endswith(".git"):
        logging.info("excluded folder %s" % nameFolder)
        return False
    else:
        return True

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.md5 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.is_addon_dir
    """

    def __init__(self,rootFolderAddons):
        # paths
        self.addons_xml = os.path.join(rootFolderAddons, "addons.xml")
        self.addons_xml_md5 = os.path.join(rootFolderAddons, "addons.xml.md5")
        self.root_folder_addons = rootFolderAddons

        # call master function
        #self._generate_addons_files()

    def _generate_addons_files(self):

        # addon list
        addons = os.listdir(self.root_folder_addons)

        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n<addons>\n"

        # set to false by fault, and if a addons.xml will be finded in a addon folder, will be changed to true
        found_an_addon = False

        # loop thru and add each addons addon.xml file
        for addon in addons:
            try:
                # skip any file or .svn folder
                if check_is_addon_dir(self.root_folder_addons + addon):

                    # create path
                    _path = os.path.join(self.root_folder_addons + addon, "addon.xml")

                    if os.path.exists(_path): found_an_addon = True

                    # split lines for stripping
                    xml_lines = open(_path, "r").read().splitlines()

                    # new addon
                    addon_xml = ""

                    # loop thru cleaning each line
                    for line in xml_lines:
                        # skip encoding format line
                        if (line.find("<?xml") >= 0): continue
                        # add line
                        #addon_xml += unicode(line.rstrip() + "\n", "UTF-8")
                        addon_xml += line.rstrip() + "\n"

                    # we succeeded so add to our final addons.xml text
                    addons_xml += addon_xml.rstrip() + "\n\n"

            except Exception as e:
                # missing or poorly formatted addon.xml
                logger.info("Excluding %s for %s" % (_path, e,))

        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"

        # only generate files if we found an addon.xml
        if found_an_addon:
            # save files
            self._save_file(addons_xml.encode("UTF-8"), self.addons_xml)
            self._generate_md5_file()

            # notify user
            logger.info("Updated addons xml and addons.xml.md5 files")
        else:
            logger.info("Could not find any addons, so script has done nothing.")

    def _generate_md5_file(self):
        try:
            # create a new md5 hash
            m = md5.new(open(self.addons_xml).read()).hexdigest()

            # save file
            self._save_file(m, self.addons_xml_md5)

        except Exception as e:
            # oops
            logger.info("An error occurred creating addons.xml.md5 file!\n%s" % (e,))

    def _save_file(self, data, the_path):
        try:

            # write data to the file
            open(the_path, "wb").write(data)

        except Exception as e:
            # oops
            logger.info("An error occurred saving %s file!\n%s" % (the_path, e,))

