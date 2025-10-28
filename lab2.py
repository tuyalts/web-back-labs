from flask import Blueprint, url_for, redirect, abort, render_template

lab2 = Blueprint('lab2', __name__)

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@lab2.route('/lab2/a')
def a():
    return 'без слэша'

@lab2.route('/lab2/a/')
def b():
    return 'со слэшем'

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок: " + flower_list[flower_id]

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)  # исправлено: было lab2end, должно быть append
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Всего цветков: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@lab2.route('/lab2/example')
def example():
    name = 'Ломбоцыренова Туяна'
    number = '2'
    course = '3'
    group = '33'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'апельсины', 'price': 120},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html', name=name, 
                          number=number, course=course, 
                          group=group, fruits=fruits)

@lab2.route('/lab2/')
def lab2_page(): 
    return render_template('lab2/lab2.html')