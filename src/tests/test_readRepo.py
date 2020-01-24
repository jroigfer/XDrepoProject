from unittest import TestCase
from src import updateRepo


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
