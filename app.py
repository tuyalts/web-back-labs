from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)


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
