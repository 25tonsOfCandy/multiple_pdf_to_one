from pypdf import PdfReader, PdfWriter, PdfMerger


class PdfWorker():
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pdfreader = PdfReader(file_path)


    def _get_pages(self):
        return self.pdfreader.pages


    def _write(self, file_path, page):
        pdfwriter = PdfWriter(file_path)
        pdfwriter.add_page(page)
        pdfwriter.write(file_path)


    def split_pdf(self):
        for index, page in enumerate(self._get_pages()):
            self._write(f"result{index}.pdf", page)


if __name__ == '__main__':
    PdfWorker("files/qwe/pdf.pdf").split_pdf()
