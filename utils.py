import os
UPLOAD_FOLDER = 'files/'


def is_exist(folder: str):
    return os.path.exists(UPLOAD_FOLDER + folder)


def create_files_folder(folder: str):
    os.mkdir(UPLOAD_FOLDER + str(folder))


def replace_whitespace(s: str, char_for_replace: str):
    return s.replace(' ', char_for_replace)


if __name__ == '__main__':
    print(is_exist('pdf'))
