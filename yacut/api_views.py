from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage, ShortExistsException
from .models import URLMap


@app.route('/api/id/', methods=('POST',))
def add_url_map():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    try:
        url_map = URLMap.add_url_map(data.get('url'), data.get('custom_id'))
    except ShortExistsException as exception:
        raise InvalidAPIUsage(str(exception))
    return jsonify(url_map.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_original_url(short_id):
    original_url = URLMap.get_by_short_id(short_id)
    if original_url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': original_url.original}), 200
