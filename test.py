from flask import Flask, request
from flask import redirect, url_for
from flask import render_template, send_file
import os
from werkzeug.utils import secure_filename
from utils import is_exist, create_files_folder
from utils import replace_whitespace, create_zip
from pdf_worker import split_pdf

# TODO сделать проверку формата файла
# TODO форматировать код до удобочитаемого
# TODO добавить надпись на странице splitpdf
# TODO написать тесты для всего

UPLOAD_FOLDER = 'files/'  # папка для загрузки файлов
# разрешенные типы файлов
ALLOWED_EXTENSIONS = set(['pdf', 'jpg', 'png', 'jpeg'])
SPLIT_PDF_HTML = '''
    <!doctype html>
    <title>Разделить pdf</title>
    <h1>Разделить pdf</h1>
    <form action="" method=post enctype=multipart/form-data>
        <input type=text name=folder_for_download required>
        <p><input type=file name="file[]" accept="application/pdf" multiple required >
            <input type=submit value=Upload>
    </form>
    '''

app = Flask(__name__)
# сообщаем flask куда загружать файлы
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):  # !NOT USING
    """Метод для проверки типа файла

    Args:
        filename (str): Название файла

    Returns:
        [type]: Что-то возвращает. не разобрался
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


# что проискходит когда переходим в корень сайта
@app.route('/splitpdf', methods=['GET', 'POST'])
def upload_file():
    """Этот метод работает когда заходим в корень сайта ('/')

    Returns:
        str: Возвращает страничку сайта
    """
    if request.method == 'POST':  # если файл загрузили и нажали кнопку upload
        file = request.files.getlist('file[]')  # проверяем загрузили ли файлы
        folder_for_download = request.form.get('folder_for_download')
        folder_for_download = replace_whitespace(folder_for_download, '_')

        # if allowed_file(file[0]):  # проверяем тип файла
        if not is_exist(folder_for_download):
            create_files_folder(folder_for_download)
        for f in file:
            # проверяем безопасность файла
            filename = secure_filename(f.filename)
            # сохраняем файл
            f.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER']
                    + '/' + folder_for_download, filename))
            # выводим файл в браузере
            split_pdf(
                UPLOAD_FOLDER + '/' + folder_for_download + '/', filename)
        create_zip(
            filename,
            UPLOAD_FOLDER + '/' + folder_for_download)
        return redirect(
            url_for(
                'uploaded_file',
                filename=filename + '.zip'))
        # если файл загружали
        return SPLIT_PDF_HTML
    if request.method == 'GET':  # первый вход на сайт
        return SPLIT_PDF_HTML


@app.route('/multiplepdftoone')  # заглушка
def multiple_pdf_to_one():
    return SPLIT_PDF_HTML


# !Скорее всего не будет юзатся
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Страница вывода загруженного файла

    Args:
        filename (str): Имя загруженного файла

    Returns:
        [type]: [description]
    """
    return send_file(
        filename, attachment_filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
