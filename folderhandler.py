import os


class FolderHandler():
    def __init__(self):
        pass


    def is_folder_exists(self, path: str):
        return os.path.exists(path)


    def create_folder(self, path: str):
        os.mkdir(path)


    def ensure_directory_exists(self, path: str):
        if self.is_folder_exists(path) is False:
            self.create_folder(path)

if __name__ == '__main__':
    print(FolderHandler().is_folder_exists("pdf"))