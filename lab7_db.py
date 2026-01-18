from flask import Blueprint, render_template, request, jsonify, g
from datetime import datetime
import sqlite3
import os

lab7 = Blueprint('lab7', __name__)

DATABASE = 'films.db'

def get_db():
    """Получение соединения с базой данных"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Для возврата словарей вместо кортежей
    return db

@lab7.teardown_appcontext
def close_connection(exception):
    """Закрытие соединения с базой данных"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def validate_film(film):
    """Валидация данных фильма"""
    errors = {}
    current_year = datetime.now().year
    
    # Проверка русского названия
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Заполните русское название'
    
    # Проверка оригинального названия
    if (not film.get('title') or film['title'].strip() == '') and (not film.get('title_ru') or film['title_ru'].strip() == ''):
        errors['title'] = 'Заполните хотя бы одно название (оригинальное или русское)'
    
    # Проверка года
    if 'year' not in film:
        errors['year'] = 'Укажите год выпуска'
    else:
        try:
            year = int(film['year'])
            if year < 1895:
                errors['year'] = f'Год не может быть раньше 1895 (первый фильм)'
            elif year > current_year:
                errors['year'] = f'Год не может быть больше текущего ({current_year})'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    if not film.get('description') or film['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    elif len(film['description']) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(film["description"])})'
    
    return errors

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM films ORDER BY id")
    films = [dict(row) for row in cursor.fetchall()]
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cursor.fetchone()
    
    if film is None:
        return jsonify({"error": "Фильм не найден"}), 404
    
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    db = get_db()
    cursor = db.cursor()
    
    # Проверяем существование фильма
    cursor.execute("SELECT id FROM films WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        return jsonify({"error": "Фильм не найден"}), 404
    
    cursor.execute("DELETE FROM films WHERE id = ?", (id,))
    db.commit()
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    db = get_db()
    cursor = db.cursor()
    
    # Проверяем существование фильма
    cursor.execute("SELECT id FROM films WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        return jsonify({"error": "Фильм не найден"}), 404
    
    film = request.get_json()
    
    # Валидация данных
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    # Логика: если оригинальное название пустое, а русское задано, 
    # то в оригинальное записываем русское
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    # Обновление фильма в БД
    cursor.execute("""
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ?
        WHERE id = ?
    """, (film['title'], film['title_ru'], film['year'], film['description'], id))
    db.commit()
    
    # Возвращаем обновленный фильм
    cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
    updated_film = cursor.fetchone()
    return jsonify(dict(updated_film))

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    db = get_db()
    cursor = db.cursor()
    
    film = request.get_json()
    
    # Валидация данных
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    # Логика: если оригинальное название пустое, а русское задано, 
    # то в оригинальное записываем русское
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    # Добавление фильма в БД
    cursor.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?)
    """, (film['title'], film['title_ru'], film['year'], film['description']))
    db.commit()
    
    # Получаем ID нового фильма
    new_id = cursor.lastrowid
    
    # Возвращаем новый фильм
    cursor.execute("SELECT * FROM films WHERE id = ?", (new_id,))
    new_film = cursor.fetchone()
    return jsonify({"id": new_id, **dict(new_film)})