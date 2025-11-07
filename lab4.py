from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)



@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error='На ноль делить нельзя')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')


@lab4.route('/lab4/sum', methods = ['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = '0'
    if x2 == '':
        x2 = '0'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult-form')
def mult_form():
    return render_template('/lab4/mult-form.html')


@lab4.route('/lab4/mult', methods = ['POST'])
def mult():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = '1'
    if x2 == '':
        x2 = '1'
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mult.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')


@lab4.route('/lab4/sub', methods = ['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/exp-form')
def exp_form():
    return render_template('/lab4/exp-form.html')


@lab4.route('/lab4/exp', methods = ['POST'])
def exp():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/exp.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/exp.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_trees = 10  

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, 
                                max_trees=max_trees)
    
    operation = request.form.get('operation')
    
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1
    
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Смит', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Бобер Бобоев', 'gender': 'male'},
    {'login': 'tuyalts', 'password': '2102', 'name': 'Туяна Ломбоцыренова', 'gender': 'female'},
    {'login': 'ivan', 'password': '0909', 'name': 'Иван Иванов', 'gender': 'male'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user_name = login
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
        else:
            authorized = False
            login=''
            user_name = '' 
        return render_template('lab4/login.html', authorized=authorized,
                                login=user_name, entered_login='')  

    login_input = request.form.get('login')  
    password = request.form.get('password')

    if login_input == '':
        return render_template('lab4/login.html', error='Не введён логин', 
                              authorized=False, entered_login=login_input)  
    if password == '':
        return render_template('lab4/login.html', error='Не введён пароль', 
                              authorized=False, entered_login=login_input)  

    for user in users:
        if login_input == user['login'] and password == user['password']:
            session['login'] = login_input
            return redirect('/lab4/login')
        
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, 
                            authorized=False, entered_login=login_input)  


@lab4.route('/lab4/logout', methods = ['GET', 'POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge')
def fridge():
    return render_template('lab4/fridge.html')


@lab4.route('/lab4/fridge', methods=['POST'])
def fridge_set():
    temperature = request.form.get('temperature')
    
    if temperature == '':
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    temp = int(temperature)
    
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = '❄️❄️❄️'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
    elif -8 <= temp <= -5:
        snowflakes = '❄️❄️'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)
    elif -4 <= temp <= -1:
        snowflakes = '❄️'
        message = f'Установлена температура: {temp}°C'
        return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)


@lab4.route('/lab4/grain')
def grain():
    return render_template('lab4/grain.html')


@lab4.route('/lab4/grain', methods=['POST'])
def grain_order():
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    prices = {
        'barley': 12000,  # ячмень
        'oats': 8500,     # овёс
        'wheat': 9000,    # пшеница
        'rye': 15000      # рожь
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if not grain_type:
        return render_template('lab4/grain.html', error='Выберите тип зерна')
    
    if weight == '':
        return render_template('lab4/grain.html', error='Введите вес')
    
    weight_num = int(weight)
    
    if weight_num <= 0:
        return render_template('lab4/grain.html', error='Вес должен быть больше 0')
    
    if weight_num > 100:
        return render_template('lab4/grain.html', error='Такого объёма сейчас нет в наличии')
    
    price_per_ton = prices[grain_type]
    total = weight_num * price_per_ton
    discount = 0
    discount_text = ''
    
    if weight_num > 10:
        discount = total * 0.1 
        total -= discount
        discount_text = f'Применена скидка 10% за большой объём. Размер скидки: {int(discount)} руб.'
    
    grain_name = grain_names[grain_type]
    
    message = f'Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight_num} т. Сумма к оплате: {int(total)} руб.'
    
    return render_template('lab4/grain.html', message=message, discount_text=discount_text)