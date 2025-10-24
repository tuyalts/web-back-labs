from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab2', __name__)


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