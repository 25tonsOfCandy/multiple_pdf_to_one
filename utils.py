import os
import shutil
import configparser
# import time
# парсер конфига с путями до файлов
cfgparser = configparser.ConfigParser()
cfgparser.read('default_folders.ini')


def is_exist_in_files_folder(folder: str):
    return os.path.exists(get_files_folder() + folder)


def create_files_folder(folder: str):
    os.mkdir(get_files_folder() + str(folder))


def replace_whitespace(s: str, char_for_replace: str):
    return s.replace(' ', char_for_replace)


def create_zip(name_of_file: str, path_to_file: str):
    shutil.make_archive(
        'zip/' + name_of_file,
        'zip',
        path_to_file
        )


def get_files_folder():
    return cfgparser['UPLOAD']['Files']


def get_pdf_folder():
    return cfgparser['RESULT']['Pdf']


def get_zip_folder():
    return cfgparser['RESULT']['Zip']


def clean_folders():
    shutil.rmtree(get_files_folder())
    shutil.rmtree(get_pdf_folder())
    shutil.rmtree(get_zip_folder())

    os.mkdir(get_files_folder())
    os.mkdir(get_pdf_folder())
    os.mkdir(get_zip_folder())


def check_for_folders():
    if not os.path.exists(get_files_folder()):
        os.mkdir(get_files_folder())
    if not os.path.exists(get_pdf_folder()):
        os.mkdir(get_pdf_folder())
    if not os.path.exists(get_zip_folder()):
        os.mkdir(get_zip_folder())


if __name__ == '__main__':
    clean_folders()
