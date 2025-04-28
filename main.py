import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader
from folderhandler import FolderHandler
from pdfHandler.pdfsplitter import PdfSplitter
from pdfHandler.pdfmerger import PdfMerger 
from ziphandler import ZipHandler
from pdfHandler.pdftablegetter import PDFTableGetter
from tablestocsvtransformer import TablesToCSVTransformer


app = Flask(__name__)
config = ConfigReader("default_folders.ini")
folder_handler = FolderHandler()
FILES_FOLDER = config.get_files_folder()
PDF_FOLDER = config.get_pdf_folder()


def get_files_list(html_element: str):
    return request.files.getlist(html_element)


def get_form_element(html_element: str):
    return request.form.get(html_element)

def save_files(file_element: str, folder_element: str):
    uploaded_files = get_files_list(file_element)
    folder = get_form_element(folder_element)
    folder_to_save = f"{FILES_FOLDER}{folder}/"
    folder_handler.ensure_directory_exists(folder_to_save)
    
    for uploaded_file in uploaded_files:
        file_path = os.path.join(f"{folder_to_save}{uploaded_file.filename}")
        uploaded_file.save(file_path)


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/splitpdf")
def split_pdf_page():
    return render_template("splitpdf.html")


@app.route("/getsplitedpdf", methods=["POST"])
def get_splited_pdf():
    if request.method == 'POST':
        save_files("file", "folder_for_download")
        folder = get_form_element("folder_for_download")
        folder_to_save = f"{FILES_FOLDER}{folder}/"
        files = get_files_list("file")
        file_path = os.path.join(f"{folder_to_save}{files[0].filename}")

        pdfsplitter = PdfSplitter(file_path)
        folder_handler.ensure_directory_exists(f"{PDF_FOLDER}{folder}/")
        pdfsplitter.split(name=folder, directory=f"{PDF_FOLDER}{folder}/")

        pdf_results_file = f"{PDF_FOLDER}{folder}/{folder}"
        for i in range(pdfsplitter.get_number_pages()):
            ZipHandler(f"{pdf_results_file}.zip").add_file(f"{pdf_results_file}{str(i)}.pdf")

        return send_file(f"{pdf_results_file}.zip", as_attachment=True)


@app.route("/mergepdf")
def merge_pdf_page():
    return render_template("mergepdf.html")


@app.route("/getmergedpdf", methods=["POST"])
def get_merged_pdf():
    if request.method == "POST":
        save_files("file", "folder_for_download")
        folder = get_form_element("folder_for_download")
        folder_to_save = f"{PDF_FOLDER}{folder}/"
        files = get_files_list("file")
        pdf_list = [f"{FILES_FOLDER}{folder}/{i.filename}" for i in files]
        pdfMerger = PdfMerger(pdf_list)
        folder_handler.ensure_directory_exists(f"{PDF_FOLDER}{folder}/")
        pdfMerger.merge(folder, folder_to_save)

        pdf_results_file = f"{PDF_FOLDER}{folder}/{folder}"
        
        return send_file(f"{pdf_results_file}.pdf", as_attachment=True)


@app.route("/tablefrompdf")
def table_from_pdf_page():
    return render_template("tablefrompdf.html")


@app.route("/getcsvfrompdffile", methods=["POST"])
def get_csv_from_pdf_file():
        save_files("file", "folder_for_download")
        folder = get_form_element("folder_for_download")
        folder_to_save = f"{PDF_FOLDER}{folder}/"
        files = get_files_list("file")
        pdf_list = [f"{FILES_FOLDER}{folder}/{i.filename}" for i in files]
        
        folder_handler.ensure_directory_exists(f"{PDF_FOLDER}{folder}/")

        file_list = TablesToCSVTransformer(PDFTableGetter(pdf_list[0]).get_tables(), folder_to_save).transform(is_return_file_list=True)
        zip_result = f"{PDF_FOLDER}{folder}/{folder}"
        for i in file_list:
            ZipHandler(f"{zip_result}.zip").add_file(i)

        return send_file(f"{zip_result}.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
