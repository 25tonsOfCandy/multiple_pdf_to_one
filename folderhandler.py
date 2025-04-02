import os


class FolderHandler():
    def __init__(self):
        pass


    def is_folder_exist(self, path: str):
        return os.path.exists(path)


    def create_folder(self, path: str):
        os.mkdir(path)



if __name__ == '__main__':
    print(FolderHandler().is_folder_exist("pdf"))