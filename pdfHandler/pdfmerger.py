from pypdf import PdfReader, PdfWriter


class PdfMerger():
    def __init__(self, pdf_list: list):
        self.pdf_list = pdf_list
        self.pdf_writer = PdfWriter()

    def _get_pages(self, pdf: str):
        return PdfReader(pdf).pages


    def _add_page(self, page):
        self.pdf_writer.add_page(page)


    def _write(self, file_path: str):
        self.pdf_writer.write(f"{file_path}.pdf")


    def merge(self, name: str, directory: str):
        for pdf in self.pdf_list:
            for page in self._get_pages(pdf):
                self._add_page(page)
        self._write(f"{directory}{name}")


if __name__ == '__main__':
    PdfMerger(["files/qwe/pdf.pdf", "files/qwe/pdf copy.pdf", "files/qwe/pdf copy 2.pdf"]).merge("mergedpdf", "files/qwe/")
