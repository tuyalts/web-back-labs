from flask import Blueprint, render_template, request, session, jsonify
import random
import time

lab9 = Blueprint('lab9', __name__)

# Хранилище в памяти
opened_boxes = {}  # id -> данные о том, кто открыл и когда
user_open_counts = {}  # session_id -> количество открытых

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

@lab9.route('/lab9/')
def main():
    if 'session_id' not in session:
        session['session_id'] = str(int(time.time())) + str(random.randint(1000, 9999))
    
    session_id = session['session_id']
    if session_id not in user_open_counts:
        user_open_counts[session_id] = 0
    
    return render_template('lab9/index.html')

@lab9.route('/lab9/api/boxes', methods=['GET'])
def get_boxes():
    session_id = session.get('session_id', '')
    
    # Фиксируем позиции на основе session_id
    random.seed(session_id)
    boxes = []
    for i in range(1, 11):
        boxes.append({
            'id': i,
            'x': random.randint(20, 900),
            'y': random.randint(20, 500),
            'opened': i in opened_boxes
        })
    
    return jsonify({
        'boxes': boxes,
        'user_opened': user_open_counts.get(session_id, 0),
        'total_opened': len(opened_boxes)
    })

@lab9.route('/lab9/api/open', methods=['POST'])
def open_box():
    data = request.json
    box_id = data.get('box_id')
    session_id = session.get('session_id', '')
    
    if not box_id or box_id not in range(1, 11):
        return jsonify({'error': 'Некорректная коробка'}), 400
    
    # Проверяем лимит
    if user_open_counts.get(session_id, 0) >= 3:
        return jsonify({'error': 'Вы уже открыли 3 коробки!'}), 400
    
    # Проверяем, не открыта ли уже
    if box_id in opened_boxes:
        return jsonify({'error': 'Эта коробка уже пуста!'}), 400
    
    # Открываем коробку
    opened_boxes[box_id] = {
        'session_id': session_id,
        'timestamp': time.time()
    }
    user_open_counts[session_id] = user_open_counts.get(session_id, 0) + 1
    
    return jsonify({
        'success': True,
        'message': congratulations[box_id - 1],
        'image': f'/static/lab9/images/{box_id}.jpg',
        'user_opened': user_open_counts[session_id],
        'remaining': 10 - len(opened_boxes)
    })

@lab9.route('/lab9/api/reset', methods=['POST'])
def reset():
    opened_boxes.clear()
    user_open_counts.clear()
    session.pop('session_id', None)
    return jsonify({'success': True})