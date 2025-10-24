from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route("/")
def start():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=uft-8'
        }

@app.errorhandler(404)
def not_found(err):
    return ''' 
<!doctype html>
<html>
    <head>
        <style>
            body {
                text-align: center;
            }
            h1 {
                color: #red;
                font-size: 48px;
            }
            img {
                max-width: 300px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <h1>404</h1>
        <h2>Такой страницы не существует</h2>
        <img src="''' + url_for('static', filename='okak.jpg') + '''" alt="Ошибка 404">
    </body>
</html>    
''', 404

@app.route("/clearcounter")
def clearcounter():
    global count
    count = 0
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
    </body>
</html>
'''

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <div>
            <ul>
                <li><a href="''' + url_for('web') + '''">Первая лабораторная</a></li>
            </ul>
        </div>
        
        <footer>
            <p>Ломбоцыренова Туяна Владимировна, ФБИ-33, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def b():
    return 'со слэшем'

flower_list = ['роза', 'тюльпан','незабудка','ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветков: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
'''
@app.route('/lab2/example')
def example():
    name = 'Ломбоцыренова  Туяна'
    number = '2'
    course = '3'
    group = '33'
    fruits = [
    {'name': 'яблоки', 'price': 100},
    {'name': 'апельсины', 'price': 120},
    {'name': 'мандарины', 'price': 95},
    {'name': 'манго', 'price': 321}]
    return render_template('example.html', name=name, 
    number=number, course=course, group=group, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')