from PyPDF2 import PdfFileReader, PdfFileWriter
import shutil

# TODO создание pdf из картинок
# TODO соединять два или более файлов в один
# TODO документация
# TODO сохранение zip файла в отдельную папку а не в корень
# *     напимер можно в папку zip а не в ту где хранятся обработанные файлы
# TODO сделать кнопку назад
# TODO вынести создание архива в utils


def split_pdf(path_to_file: str, name_of_file: str):
    reader = PdfFileReader(path_to_file + name_of_file)
    num_of_pages = reader.getNumPages()

    for i in range(num_of_pages):
        output = PdfFileWriter()
        output.addPage(reader.getPage(i))
        output_stream = open(
            path_to_file + name_of_file + str(i) + ".pdf", "wb")
        output.write(output_stream)
        output_stream.close()

    shutil.make_archive(
        name_of_file,
        'zip',
        path_to_file
        )
