import zipfile


class ZipHandler():
    def __init__(self, file_path):
        self.file_path = file_path


    def add_file(self, filename: str):
        with zipfile.ZipFile(self.file_path, 'a') as filezip:
            filezip.write(filename)


    def add_file_list(self, filenames: list):
        with zipfile.ZipFile(self.file_path, 'a') as filezip:
            for filename in filenames:
                filezip.write(filename)


    def create_file_list(self, filenames: list):
        with zipfile.ZipFile(self.file_path, 'a') as filezip:
            for filename in filenames:
                filezip.write(filename)
