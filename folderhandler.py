import os


class FolderHandler():
    def __init__(self):
        pass


    def is_folder_exist(self, path: str):
        os.path.exists(path)


    def create_folder(self, path: str):
        os.mkdir(path)
