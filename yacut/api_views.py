from flask import jsonify, request

from .error_handlers import InvalidAPIUsage, NonExistingShortId
from . import app, db
from .models import URLMap
from .views import is_valid_short_id, get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_id()
    else:
        if not is_valid_short_id(data['custom_id']):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if URLMap.query.filter_by(
            short=data['custom_id']
        ).first() is not None:
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_opinion(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if not url_map:
        raise NonExistingShortId('Указанный id не найден')
    return jsonify({'url': url_map.original}), 200
