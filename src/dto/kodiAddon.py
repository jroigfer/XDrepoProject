from dto.repo import Repo

class KodiAddon:
    def __init__(self, name, repo, addonFolder, addonRepoFolder, extraFolder):
        self.name = name
        self.repo = repo
        self.addonFolder = addonFolder
        self.addonRepoFolder = addonRepoFolder
        self.extraFolder = extraFolder