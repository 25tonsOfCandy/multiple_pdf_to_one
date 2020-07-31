from PyPDF2 import PdfFileReader, PdfFileWriter

# TODO создание pdf из картинок
# * TODO соединять два или более файлов в один
# TODO документация
# * TODO сохранение zip файла в отдельную папку а не в корень
# *     напимер можно в папку zip а не в ту где хранятся обработанные файлы
#  * TODO сделать кнопку назад
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


def multiple_pdf_to_one(pdf_list: list, name_of_result_file: str):

    result = PdfFileWriter()
    for pdf in pdf_list:
        reader = PdfFileReader(pdf)
        for page in range(reader.getNumPages()):
            result.addPage(reader.getPage(page))

    outputstream = open('pdf/' + name_of_result_file + '.pdf', 'wb')
    result.write(outputstream)
    outputstream.close()
