from tabula import read_pdf


class PDFTableGetter():
    def __init__(self, pdf_file: str):
        self.pdf_file = pdf_file


    def get_tables(self):
        return read_pdf(self.pdf_file, pages="all")
