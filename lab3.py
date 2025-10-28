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
    # Удаляем все куки настроек
    resp.delete_cookie('color')
    resp.delete_cookie('back_color')
    resp.delete_cookie('text_size')
    return resp