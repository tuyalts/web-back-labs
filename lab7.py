from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')


films = [
    {
        "title": "Superbad",
        "title_ru": "SuperПерцы",
        "year": 2007,
        "description": "Сквозь огонь и водку трое приятелей спешат на вечеринку года в честь прощания с девственностью. Как взять на абордаж красотку-одноклассницу, подорвать полицейскую машину и остаться в живых?.."
    },
    {
        "title": "Harry Potter and the Sorcerer's Stone",
        "title_ru": "Гарри Поттер и философский камень",
        "year":2001,
        "description": "Жизнь десятилетнего Гарри Поттера нельзя назвать сладкой: родители умерли, едва ему исполнился год, а от дяди и тёти, взявших сироту на воспитание, достаются лишь тычки да подзатыльники. Но в одиннадцатый день рождения Гарри всё меняется. Странный гость, неожиданно появившийся на пороге, приносит письмо, из которого мальчик узнаёт, что на самом деле он - волшебник и зачислен в школу магии под названием Хогвартс. А уже через пару недель Гарри будет мчаться в поезде Хогвартс-экспресс навстречу новой жизни, где его ждут невероятные приключения, верные друзья и самое главное — ключ к разгадке тайны смерти его родителей."
    },
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year":2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    }
]


def validate_film(film):
    """Валидация данных фильма"""
    errors = {}
    current_year = datetime.now().year
    
    # Проверка русского названия
    if not film.get('title_ru') or film['title_ru'].strip() == '':
        errors['title_ru'] = 'Заполните русское название'
    
    # Проверка оригинального названия
    # Если русское название пустое, то оригинальное должно быть заполнено
    if (not film.get('title') or film['title'].strip() == '') and (not film.get('title_ru') or film['title_ru'].strip() == ''):
        errors['title'] = 'Заполните хотя бы одно название (оригинальное или русское)'
    

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
    
    if not film.get('description') or film['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    elif len(film['description']) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(film["description"])})'
    
    return errors


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film_by_id(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(films[id])
    

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Фильм не найден"}), 404
    
    film = request.get_json()
    
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    films[id] = film
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    if (not film.get('title') or film['title'].strip() == '') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    films.append(film)
    return jsonify({"id": len(films) - 1})