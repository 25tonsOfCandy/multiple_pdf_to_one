import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader
from folderhandler import FolderHandler
from pdfHandler.pdfsplitter import PdfSplitter
from ziphandler import ZipHandler


app = Flask(__name__)
config_reader = ConfigReader("default_folders.ini")
folder_handler = FolderHandler()


@app.route("/")
def main_page():
    return render_template("index.html")


@app.route("/splitpdf")
def splitpdf():
    return render_template("splitpdf.html")


@app.route("/getsplitedpdf", methods=["POST"])
def test():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("file")
        filename = request.form.get("folder_for_download")

        if folder_handler.is_folder_exist(config_reader.get_files_folder() + filename) == False:
            FolderHandler().create_folder(config_reader.get_files_folder() + filename)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(f"{config_reader.get_files_folder()}{filename}/{uploaded_file.filename}")
            uploaded_file.save(file_path)

        # TODO: Return all files in zip archive maybe?
        pdfsplitter = PdfSplitter(file_path)
        folder_handler.create_folder(config_reader.get_pdf_folder()+filename+"/")
        pdfsplitter.split(name=filename, directory=config_reader.get_pdf_folder()+filename+"/")

        for i in range(pdfsplitter.get_number_pages()):
            ZipHandler(config_reader.get_pdf_folder()+filename+"/"+filename+".zip").add_file(config_reader.get_pdf_folder()+filename+"/"+filename+str(i)+".pdf")

        return send_file(config_reader.get_pdf_folder()+filename+"/"+filename+".zip", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
