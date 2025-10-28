from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or "Аноним"
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age') or "21"

    return render_template('lab3/lab3.html', name=name, name_color=name_color,
    age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():

    card = request.args.get('card')
    name = request.args.get('name')
    cvv = request.args.get('cvv')

    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price, card=card, name=name, cvv=cvv)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    back_color = request.args.get('back_color')
    text_size = request.args.get('text_size')
    if color or back_color or text_size:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if back_color:
            resp.set_cookie('back_color', back_color)
        if text_size:
            resp.set_cookie('text_size', text_size)
        return resp
    
    color = request.cookies.get('color', '')
    back_color = request.cookies.get('back_color', '')
    text_size = request.cookies.get('text_size', '')
    
    return render_template('lab3/settings.html', color=color, back_color=back_color, text_size=text_size)


@lab3.route('/lab3/del_settings')
def del_display_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('back_color') 
    resp.delete_cookie('text_size')
    return resp


@lab3.route('/lab3/train')
def train():
    errors = {}
    
    # Получаем данные из формы
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    departure = request.args.get('departure')
    destination = request.args.get('destination')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    if fio is not None:
        if not fio:
            errors['fio'] = 'Заполните ФИО'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not age:
            errors['age'] = 'Заполните возраст'
        elif not age.isdigit() or not (1 <= int(age) <= 120):
            errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        if not departure:
            errors['departure'] = 'Заполните пункт выезда'
        if not destination:
            errors['destination'] = 'Заполните пункт назначения'
        if not date:
            errors['date'] = 'Выберите дату'
    
    price = None
    ticket_type = None
    if fio and not errors and request.args.get('fio') is not None:
        # Базовая цена
        if int(age) < 18:
            price = 700
            ticket_type = "Детский билет"
        else:
            price = 1000
            ticket_type = "Взрослый билет"
        
        # Доплаты
        if shelf in ['нижняя', 'нижняя боковая']:
            price += 100
        if linen == 'on':
            price += 75
        if luggage == 'on':
            price += 250
        if insurance == 'on':
            price += 150
    
    return render_template('lab3/train.html', 
                         fio=fio, shelf=shelf, linen=linen, luggage=luggage,
                         age=age, departure=departure, destination=destination,
                         date=date, insurance=insurance, errors=errors,
                         price=price, ticket_type=ticket_type)


@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('back_color')
    resp.delete_cookie('text_size')
    return resp


@lab3.route('/lab3/search')
def search():
    books = [
            {'name': 'Норвежский лес', 'price': 650, 'author': 'Харуки Мураками', 'genre': 'Роман', 'year': 1987},
            {'name': 'Кафка на пляже', 'price': 720, 'author': 'Харуки Мураками', 'genre': 'Магический реализм', 'year': 2002},
            {'name': 'Охота на овец', 'price': 580, 'author': 'Харуки Мураками', 'genre': 'Роман', 'year': 1982},
            {'name': '1Q84', 'price': 890, 'author': 'Харуки Мураками', 'genre': 'Антиутопия', 'year': 2009},
            {'name': 'Хроники Заводной Птицы', 'price': 750, 'author': 'Харуки Мураками', 'genre': 'Роман', 'year': 1994},
            {'name': 'Мастер и Маргарита', 'price': 450, 'author': 'Михаил Булгаков', 'genre': 'Классика', 'year': 1967},
            {'name': 'Преступление и наказание', 'price': 380, 'author': 'Фёдор Достоевский', 'genre': 'Классика', 'year': 1866},
            {'name': '1984', 'price': 520, 'author': 'Джордж Оруэлл', 'genre': 'Антиутопия', 'year': 1949},
            {'name': 'Три товарища', 'price': 490, 'author': 'Эрих Мария Ремарк', 'genre': 'Роман', 'year': 1936},
            {'name': 'Маленький принц', 'price': 320, 'author': 'Антуан де Сент-Экзюпери', 'genre': 'Притча', 'year': 1943},
            {'name': 'Сто лет одиночества', 'price': 680, 'author': 'Габриэль Гарсиа Маркес', 'genre': 'Магический реализм', 'year': 1967},
            {'name': 'Улисс', 'price': 950, 'author': 'Джеймс Джойс', 'genre': 'Модернизм', 'year': 1922},
            {'name': 'Война и мир', 'price': 780, 'author': 'Лев Толстой', 'genre': 'Классика', 'year': 1869},
            {'name': 'Анна Каренина', 'price': 560, 'author': 'Лев Толстой', 'genre': 'Классика', 'year': 1877},
            {'name': 'Лолита', 'price': 510, 'author': 'Владимир Набоков', 'genre': 'Роман', 'year': 1955},
            {'name': 'Братья Карамазовы', 'price': 710, 'author': 'Фёдор Достоевский', 'genre': 'Классика', 'year': 1880},
            {'name': 'Гарри Поттер и философский камень', 'price': 420, 'author': 'Джоан Роулинг', 'genre': 'Фэнтези', 'year': 1997},
            {'name': 'Властелин колец', 'price': 880, 'author': 'Дж. Р. Р. Толкин', 'genre': 'Фэнтези', 'year': 1954},
            {'name': 'Атлант расправил плечи', 'price': 920, 'author': 'Айн Рэнд', 'genre': 'Философский роман', 'year': 1957},
            {'name': 'Шантарам', 'price': 670, 'author': 'Грегори Дэвид Робертс', 'genre': 'Роман', 'year': 2003}
        ]

    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    search_clicked = request.args.get('search')
    reset_clicked = request.args.get('reset')
    
    if reset_clicked:
        resp = make_response(redirect('/lab3/search'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    if search_clicked:
        resp = make_response(redirect('/lab3/search'))
        resp.set_cookie('min_price', min_price or '')
        resp.set_cookie('max_price', max_price or '')
        return resp
    
    if not min_price and not max_price:
        min_price = request.cookies.get('min_price') or ''
        max_price = request.cookies.get('max_price') or ''
    
    all_prices = [p['price'] for p in books]
    min_all_price = min(all_prices)
    max_all_price = max(all_prices)
    
    filtered_books = books
    has_filters = (min_price and min_price.strip()) or (max_price and max_price.strip())
    
    if has_filters:
        filtered_books = []
        
        min_val = int(min_price) if min_price and min_price.strip() else 0
        max_val = int(max_price) if max_price and max_price.strip() else float('inf')
        
        if (min_price and min_price.strip() and max_price and max_price.strip() and 
            min_val > max_val):
            min_val, max_val = max_val, min_val
        
        for book in books:
            price = book['price']
            min_condition = not min_price or not min_price.strip() or price >= min_val
            max_condition = not max_price or not max_price.strip() or price <= max_val
            
            if min_condition and max_condition:
                filtered_books.append(book)
    
    return render_template('lab3/search.html',
                         products=filtered_books,
                         min_price=min_price or '',
                         max_price=max_price or '',
                         min_all_price=min_all_price,
                         max_all_price=max_all_price,
                         products_count=len(filtered_books),
                         all_products_count=len(books))


@lab3.route('/lab3/del_book_search')
def del_book_search():
    resp = make_response(redirect('/lab3/search'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp