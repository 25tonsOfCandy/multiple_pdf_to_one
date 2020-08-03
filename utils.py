import os
import shutil
import configparser
UPLOAD_FOLDER = 'files/'


def is_exist(folder: str):
    return os.path.exists(UPLOAD_FOLDER + folder)


def create_files_folder(folder: str):
    os.mkdir(UPLOAD_FOLDER + str(folder))


def replace_whitespace(s: str, char_for_replace: str):
    return s.replace(' ', char_for_replace)


def create_zip(name_of_file: str, path_to_file: str):
    shutil.make_archive(
        'zip/' + name_of_file,
        'zip',
        path_to_file
        )


def get_files_folder():
    cfgparser = configparser.ConfigParser()
    cfgparser.read('default_folders.ini')
    return cfgparser['UPLOAD']['Files']


def get_pdf_folder():
    cfgparser = configparser.ConfigParser()
    cfgparser.read('default_folders.ini')
    return cfgparser['RESULT']['Pdf']


def get_zip_folder():
    cfgparser = configparser.ConfigParser()
    cfgparser.read('default_folders.ini')
    return cfgparser['RESULT']['Zip']


if __name__ == '__main__':
    get_files_folder()
