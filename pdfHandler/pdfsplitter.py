from pypdf import PdfReader, PdfWriter


class PdfSplitter():
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pdfreader = PdfReader(self.file_path)


    def _get_pages(self):
        return self.pdfreader.pages


    def _write(self, file_path, page):
        pdfwriter = PdfWriter(file_path)
        pdfwriter.add_page(page)
        pdfwriter.write(file_path)


    def split(self, name: str, directory: str):
        for index, page in enumerate(self._get_pages()):
            self._write(f"{directory}{name}{index}.pdf", page)


    def get_number_pages(self):
        return len(self.pdfreader.pages)

if __name__ == '__main__':
    PdfSplitter("files/qwe/pdf.pdf").split("pdfsplited", "files/qwe")
