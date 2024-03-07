import re

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_random_link
from settings import RANDOM_LINK_LENGHT


@app.route('/api/id/', methods=('POST',))
def add_url_map():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None or len(data['custom_id']) == 0:
        data['custom_id'] = get_random_link(RANDOM_LINK_LENGHT)
    else:
        if not re.match(r'^[A-Za-z0-9]{1,6}$', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage('Предложенный вариант короткой ссылки уже существует.')
    url_map = URLMap()
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_original_url(short_id):
    original_url = URLMap.get_url_map(short_id)
    if original_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_url.original}), 200