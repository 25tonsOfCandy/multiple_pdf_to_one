from PyPDF2 import PdfFileReader, PdfFileWriter
import utils as ut


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

    outputstream = open(
        ut.get_pdf_folder() + name_of_result_file + '.pdf', 'wb')

    result.write(outputstream)
    outputstream.close()
