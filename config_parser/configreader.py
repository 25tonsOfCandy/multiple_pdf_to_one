from configparser import ConfigParser


class ConfigReader():
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.cfgparser = ConfigParser()
        self.cfgparser.read(self.config_path)



    def get_by_keys(self, category: str, element: str):
        return self.cfgparser[category][element]


    def get_files_folder(self):
        return self.cfgparser['UPLOAD']['Files']


    def get_pdf_folder(self):
        return self.cfgparser['RESULT']['Pdf']


    def get_zip_folder(self):
        return self.cfgparser['RESULT']['Zip']


if __name__ == '__main__':
    print(ConfigReader("default_folders.ini").get_files_folder())