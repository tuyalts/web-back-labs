import os
from dotenv import load_dotenv
from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
from flask_sqlalchemy import SQLAlchemy
from db import db
from os import path
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'другой-секретный-секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

db_name = 'tuyana_lombocyrenova_orm'
db_user = 'tuyana_lombocyrenova_orm' 
db_password = 'passwors'  
host_ip = '127.0.0.1' 
host_port = 5432

if app.config['DB_TYPE'] == 'postgres':
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "tuyana_lombocyrenova_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.route("/")
def start():
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
                <li><a href="/lab1">Первая лабораторная</a></li>
                <li><a href="/lab2">Вторая лабораторная</a></li>
                <li><a href="/lab3">Третья лабораторная</a></li>
                <li><a href="/lab4">Четвертая лабораторная</a></li>
                <li><a href="/lab5">Пятая лабораторная</a></li>
                <li><a href="/lab6">Шестая лабораторная</a></li>
                <li><a href="/lab7">Седьмая лабораторная</a></li>
                <li><a href="/lab8">Восьмая лабораторная</a></li>
            </ul>
        </div>
        
        <footer>
            <p>&copy; Ломбоцыренова Туяна, ФБИ-33, 3 курс, 2025</p>
        </footer>
    </body>
</html>
'''


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
                color: red;
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