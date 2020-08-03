from flask import Flask, request
from flask import redirect, url_for
from flask import render_template, send_file
import os
from werkzeug.utils import secure_filename
import utils as ut
from pdf_worker import split_pdf, multiple_pdf_to_one


UPLOAD_FOLDER = 'files/'  # папка для загрузки файлов
# разрешенные типы файлов
ALLOWED_EXTENSIONS = set(['pdf', 'jpg', 'png', 'jpeg'])
SPLIT_PDF_HTML = '''
    <!doctype html>
    <title>Разделить pdf</title>
    <a href='/'><input type="button" value="Назад"></a>
    <h1>Разделить pdf</h1>
    <form action="" method=post enctype=multipart/form-data>
        <input type=text name=folder_for_download required>
<p><input type=file name="file[]" accept="application/pdf" multiple required >
            <input type=submit value=Upload>
    </form>
    '''
MULTIPLE_PDF = '''
    <!doctype html>
    <title>Соединить pdf</title>
    <a href='/'><input type="button" value="Назад"></a>
    <h1>Соединить pdf</h1>
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
        folder_for_download = ut.replace_whitespace(folder_for_download, '_')

        # if allowed_file(file[0]):  # проверяем тип файла
        if not ut.is_exist(folder_for_download):
            ut.create_files_folder(folder_for_download)
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
        ut.create_zip(
            filename,
            UPLOAD_FOLDER + '/' + folder_for_download)
        return redirect(
            url_for(
                'return_zip',
                filename=filename + '.zip'))
        # если файл загружали
        return SPLIT_PDF_HTML
    if request.method == 'GET':  # первый вход на сайт
        return SPLIT_PDF_HTML


@app.route('/multiplepdftoone', methods=['GET', 'POST'])  # заглушка
def multiple_pdf_to_one_page():
    if request.method == 'GET':
        return MULTIPLE_PDF
    if request.method == 'POST':
        files = request.files.getlist("file[]")
        folder_for_download = request.form.get('folder_for_download')
        folder_for_download = ut.replace_whitespace(folder_for_download, '_')

        if not ut.is_exist(folder_for_download):
            ut.create_files_folder(folder_for_download)
        for f in files:
            # проверяем безопасность файла
            filename = secure_filename(f.filename)
            # сохраняем файл
            f.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER']
                    + '/' + folder_for_download, filename))
        multiple_pdf_to_one(files, folder_for_download)
        return redirect(url_for(
            'return_result_pdf', filename=folder_for_download + '.pdf'))

        return MULTIPLE_PDF


# !Скорее всего не будет юзатся
@app.route('/return_zip/<filename>')
def return_zip(filename):
    """Страница вывода загруженного файла

    Args:
        filename (str): Имя загруженного файла

    Returns:
        [type]: [description]
    """
    return send_file(
        'zip/' + filename, attachment_filename=filename)


@app.route('/return_result_pdf/<filename>')
def return_result_pdf(filename):
    """Страница вывода загруженного файла

    Args:
        filename (str): Имя загруженного файла

    Returns:
        [type]: [description]
    """
    return send_file(
        'pdf/' + filename, attachment_filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
