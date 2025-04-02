import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader
from folderhandler import FolderHandler
from pdfHandler.pdfsplitter import PdfSplitter
from ziphandler import ZipHandler


app = Flask(__name__)
config = ConfigReader("default_folders.ini")
folder_handler = FolderHandler()
FILES_FOLDER = config.get_files_folder()
PDF_FOLDER = config.get_pdf_folder()


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/splitpdf")
def split_pdf_page():
    return render_template("splitpdf.html")


@app.route("/getsplitedpdf", methods=["POST"])
def get_splited_pdf():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        folder = request.form.get("folder_for_download")
        folder_to_save = f"{FILES_FOLDER}{folder}/"

        folder_handler.ensure_directory_exists(folder_to_save)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(f"{FILES_FOLDER}{folder}/{uploaded_file.filename}")
            uploaded_file.save(file_path)

        pdfsplitter = PdfSplitter(file_path)
        folder_handler.ensure_directory_exists(f"{PDF_FOLDER}{folder}/")
        pdfsplitter.split(name=folder, directory=f"{PDF_FOLDER}{folder}/")

        pdf_results_file = f"{PDF_FOLDER}{folder}/{folder}"
        for i in range(pdfsplitter.get_number_pages()):
            ZipHandler(f"{pdf_results_file}.zip").add_file(f"{pdf_results_file}{str(i)}.pdf")

        return send_file(f"{pdf_results_file}.zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
