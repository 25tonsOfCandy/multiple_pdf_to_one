import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader
from folderhandler import FolderHandler
from pdfHandler.pdfsplitter import PdfSplitter
from pdfHandler.pdfmerger import PdfMerger 
from ziphandler import ZipHandler


app = Flask(__name__)
config = ConfigReader("default_folders.ini")
folder_handler = FolderHandler()
FILES_FOLDER = config.get_files_folder()
PDF_FOLDER = config.get_pdf_folder()


def get_files_list(html_element: str):
    return request.files.getlist(html_element)


def get_form_element(html_element: str):
    return request.form.get(html_element)

def save_files():
    uploaded_files = get_files_list("file")
    folder = get_form_element("folder_for_download")
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
        save_files()
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
        save_files()
        folder = get_form_element("folder_for_download")
        folder_to_save = f"{PDF_FOLDER}{folder}/"
        files = get_files_list("file")
        pdf_list = [f"{FILES_FOLDER}{folder}/{i.filename}" for i in files]
        pdfMerger = PdfMerger(pdf_list)
        folder_handler.ensure_directory_exists(f"{PDF_FOLDER}{folder}/")
        pdfMerger.merge(folder, folder_to_save)

        pdf_results_file = f"{PDF_FOLDER}{folder}/{folder}"

        return send_file(f"{pdf_results_file}.pdf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
