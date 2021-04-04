from flask import Flask, request
from . import parsix

ALLOWED_EXTENSIONS = {'txt', 'log'}
MAX_LENGTH_OF_LINE = 10000

app = Flask(__name__)

def allowed_file(filename):
    '''Проверка допустимого расширения файла.

    Данный метод ограничивает возможность загрузки файлов с любым расширением на сервер.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Для отправки файла можно использовать следующую команду
# curl -F "file=@logs/text1.log" http://localhost:8080
@app.route("/", methods=('GET', 'POST'))
def home():
    '''View домашней страницы приложения.

    Выводит простое приветственное сообщение, обрабатывает GET, POST запросы.
    '''
    if request.method == 'POST':
        # Выражения if проверяют, что был отправлен непустой файл с допустимым расширением
        if 'file' not in request.files:
            return "File is not found"
        
        file = request.files['file']

        if file.filename == '':
            return "File is not found"

        if file and allowed_file(file.filename):
            # После всех проверок начинает работу парсер, 
            # который возвращает количество обработанных и ошибочных строк
            parser = parsix.Parsix(MAX_LENGTH_OF_LINE)
            parsed_lines, not_parsed_lines = parser.parse_file(file, 'output.jsonl', 'wronglines.log')
            return f"Number of processed lines:\t{parsed_lines}\nNumber of lines with mistakes:\t{not_parsed_lines}"

    return "This is a simple app for parsing logs"
