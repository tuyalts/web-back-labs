from flask import Blueprint, url_for, request, redirect
import datetime

lab1 = Blueprint('lab1', __name__)

@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа 1</title>
    </head>
    <body>
        <h1>web-сервер на flask</h1>
        <p>Flask — фреймворк для создания веб-приложений на языке 
        программирования Python, использующий набор инструментов 
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории 
        так называемых микрофреймворков — минималистичных каркасов 
        веб-приложений, сознательно предоставляющих лишь самые 
        базовые возможности.</p>

        <a href="/">Меню</a>

        <h2>Список роутов:</h2>
        <ul>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">/lab1/author</a></li>
            <li><a href="/lab1/oak">/lab1/oak</a></li>
            <li><a href="/lab1/counter">/lab1/counter</a></li>
            <li><a href="/lab1/clearcounter">/lab1/clearcounter</a></li>
        </ul>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return '''
<!doctype html>
<html>
   <body>
       <h1>web-сервер на flask</h1>
       <a href="/lab1/author">author</a>
   </body>
</html>
'''


@lab1.route("/lab1/author")
def author():
    name = "Ломбоцыренова Туяна Владимировна"
    group = "ФБИ-33"
    faculty = "ФБ"
    return f'''
<!doctype html>
<html>
   <body>
       <p>Студент: {name}</p>
       <p>Группа: {group}</p>
       <p>Факультет: {faculty}</p>
       <a href="/lab1/web">web</a>
   </body>
</html>
'''


@lab1.route("/lab1/oak")
def oak():
    return '''
<!doctype html>
<html>
   <body>
       <h1>Дуб</h1>
       <img src="''' + url_for('static', filename='oak.jpg') + '''">
   </body>
</html>
'''


count = 0


@lab1.route("/lab1/counter")
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
   <body>
       <p>Сколько раз вы сюда заходили: ''' + str(count) + '''</p>
       <a href="/lab1/clearcounter">Очистить счётчик</a>
   </body>
</html>
'''


@lab1.route("/lab1/clearcounter")
def clearcounter():
    global count
    count = 0
    return redirect('/lab1/counter')


@lab1.route("/lab1/info")
def info():
    return redirect('/lab1/author')


@lab1.route("/lab1/created")
def created():
    return "Страница создана", 201


@lab1.route("/lab1/zero")
def zero():
    return 1/0