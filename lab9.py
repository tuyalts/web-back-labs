from flask import Blueprint, render_template, request, session, jsonify
import random
import time

lab9 = Blueprint('lab9', __name__)

# Хранилище в памяти
opened_boxes = {}
user_open_counts = {}
user_auth = {}  # session_id -> username
# Пользователи для авторизации
users = {
    'admin': '123',
    'user': 'password',
    'santa': 'santa2024'
}

congratulations = [
    "С Новым годом!",
    "Желаю счастья!",
    "Пусть сбудутся мечты!",
    "Здоровья и удачи!",
    "Процветания в новом году!",
    "Мира и добра!",
    "Любви и тепла!",
    "Успехов во всем!",
    "Радости каждый день!",
    "Исполнения желаний!"
]

# Какие коробки доступны только авторизованным (8,9,10 - только для авторизованных)
auth_only_boxes = {8, 9, 10}

@lab9.route('/lab9/')
def main():
    if 'session_id' not in session:
        session['session_id'] = str(int(time.time())) + str(random.randint(1000, 9999))
    
    session_id = session['session_id']
    if session_id not in user_open_counts:
        user_open_counts[session_id] = 0
    
    # Проверяем, авторизован ли пользователь
    is_authenticated = session_id in user_auth
    
    return render_template('lab9/index.html', 
                         is_authenticated=is_authenticated,
                         username=user_auth.get(session_id))

@lab9.route('/lab9/api/boxes', methods=['GET'])
def get_boxes():
    session_id = session.get('session_id', '')
    is_authenticated = session_id in user_auth
    
    # Фиксируем позиции на основе session_id
    random.seed(session_id)
    boxes = []
    for i in range(1, 11):
        box_data = {
            'id': i,
            'x': random.randint(20, 900),
            'y': random.randint(20, 500),
            'opened': i in opened_boxes,
            'requires_auth': i in auth_only_boxes
        }
        boxes.append(box_data)
    
    return jsonify({
        'boxes': boxes,
        'user_opened': user_open_counts.get(session_id, 0),
        'total_opened': len(opened_boxes),
        'authenticated': is_authenticated,
        'username': user_auth.get(session_id, '')
    })

@lab9.route('/lab9/api/open', methods=['POST'])
def open_box():
    data = request.json
    box_id = data.get('box_id')
    session_id = session.get('session_id', '')
    is_authenticated = session_id in user_auth
    
    if not box_id or box_id not in range(1, 11):
        return jsonify({'error': 'Некорректная коробка'}), 400
    
    # Проверяем лимит
    if user_open_counts.get(session_id, 0) >= 3:
        return jsonify({'error': 'Вы уже открыли 3 коробки!'}), 400
    
    # Проверяем, не открыта ли уже
    if box_id in opened_boxes:
        return jsonify({'error': 'Эта коробка уже пуста!'}), 400
    
    # Проверяем, требуется ли авторизация для этой коробки
    if box_id in auth_only_boxes and not is_authenticated:
        return jsonify({'error': 'Эта коробка только для авторизованных пользователей!'}), 403
    
    # Открываем коробку
    opened_boxes[box_id] = {
        'session_id': session_id,
        'timestamp': time.time(),
        'username': user_auth.get(session_id, 'Гость')
    }
    user_open_counts[session_id] = user_open_counts.get(session_id, 0) + 1
    
    return jsonify({
        'success': True,
        'message': congratulations[box_id - 1],
        'image': f'/static/lab9/images/{box_id}.jpg',
        'user_opened': user_open_counts[session_id],
        'remaining': 10 - len(opened_boxes)
    })

@lab9.route('/lab9/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Введите логин и пароль'}), 400
    
    if username in users and users[username] == password:
        session_id = session.get('session_id', '')
        user_auth[session_id] = username
        return jsonify({
            'success': True,
            'username': username,
            'message': f'Добро пожаловать, {username}!'
        })
    
    return jsonify({'error': 'Неверный логин или пароль'}), 401

@lab9.route('/lab9/api/logout', methods=['POST'])
def logout():
    session_id = session.get('session_id', '')
    if session_id in user_auth:
        username = user_auth.pop(session_id)
        return jsonify({
            'success': True,
            'message': f'До свидания, {username}!'
        })
    return jsonify({'error': 'Вы не авторизованы'}), 400

@lab9.route('/lab9/api/refill', methods=['POST'])
def refill():
    """Дед Мороз наполняет коробки заново (только для авторизованных)"""
    session_id = session.get('session_id', '')
    
    if session_id not in user_auth:
        return jsonify({'error': 'Только для авторизованных пользователей!'}), 403
    
    # Очищаем все открытые коробки
    opened_boxes.clear()
    # Сбрасываем счетчики для всех пользователей
    user_open_counts.clear()
    
    return jsonify({
        'success': True,
        'message': '🎅 Дед Мороз наполнил все коробки подарками заново!'
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset():
    """Сброс игры (для теста, без авторизации)"""
    opened_boxes.clear()
    user_open_counts.clear()
    session.pop('session_id', None)
    return jsonify({'success': True})