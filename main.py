import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader
from folderhandler import FolderHandler
from pdfHandler.pdfsplitter import PdfSplitter

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
        # TODO: File Exist Error
        if folder_handler.is_folder_exist(config_reader.get_files_folder() + filename) == None:
            FolderHandler().create_folder(config_reader.get_files_folder() + filename)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(f"{config_reader.get_files_folder()}{filename}/{uploaded_file.filename}")
            uploaded_file.save(file_path)

        # TODO: Return all files in zip archive maybe?
        folder_handler.create_folder(config_reader.get_pdf_folder()+filename+"/")
        PdfSplitter(file_path).split(name=filename, directory=config_reader.get_pdf_folder()+filename+"/")

        return send_file(config_reader.get_pdf_folder()+filename+"/"+filename+"0.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
