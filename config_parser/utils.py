import os
import shutil
from configreader import ConfigReader


cfgreader = ConfigReader("default_folders.ini")


def is_exist_in_files_folder(folder: str):
    return os.path.exists(cfgreader.get_files_folder() + folder)


def create_files_folder(folder: str):
    os.mkdir(cfgreader.get_files_folder() + str(folder))


def replace_whitespace(s: str, char_for_replace: str):
    return s.replace(' ', char_for_replace)


def create_zip(name_of_file: str, path_to_file: str):
    shutil.make_archive(
        cfgreader.get_zip_folder() + name_of_file,
        'zip',
        path_to_file
        )


def clean_folders():
    shutil.rmtree(cfgreader.get_files_folder())
    shutil.rmtree(cfgreader.get_pdf_folder())
    shutil.rmtree(cfgreader.get_zip_folder())

    os.mkdir(cfgreader.get_files_folder())
    os.mkdir(cfgreader.get_pdf_folder())
    os.mkdir(cfgreader.get_zip_folder())


def check_for_folders():
    if not os.path.exists(cfgreader.get_files_folder()):
        os.mkdir(cfgreader.get_files_folder())
    if not os.path.exists(cfgreader.get_pdf_folder()):
        os.mkdir(cfgreader.get_pdf_folder())
    if not os.path.exists(cfgreader.get_zip_folder()):
        os.mkdir(cfgreader.get_zip_folder())


def listdir(directory: str):
    return os.listdir(directory)


if __name__ == '__main__':
    clean_folders()
