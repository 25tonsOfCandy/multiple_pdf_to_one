import os

from flask import Flask
from flask import render_template
from flask import send_file, request
from config_parser.configreader import ConfigReader

app = Flask(__name__)
config_reader = ConfigReader("default_folders.ini")

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
        folder = request.form.get("folder_for_download")
        for uploaded_file in uploaded_files:
            file_path = os.path.join(f"{config_reader.get_files_folder()}{folder}/{uploaded_file.filename}")
            uploaded_file.save(file_path)
        return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
