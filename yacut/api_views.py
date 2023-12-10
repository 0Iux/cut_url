from flask import jsonify, request

from .error_handlers import InvalidAPIUsage
from . import app, db
from .models import URLMap
from .views import is_valid_short_id, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()
    if data == {}:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'original' not in data:
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if 'short' not in data:
        data['short'] = get_unique_short_id()
    else:
        if not is_valid_short_id(data['short']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=data['short']).first() is not None:
            raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({'url_map': url_map.to_dict()}), 201


@app.route('/api/id/<int:id>/', methods=['GET'])
def get_opinion(id):
    url_map = URLMap.query.filter_by(id=id).first()
    if not url_map:
        raise InvalidAPIUsage('Указанный id не найден')
    return jsonify({'url': url_map.original}), 200
keys