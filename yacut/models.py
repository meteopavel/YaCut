import random
import re
import string

from datetime import datetime

from flask import url_for

from . import db
from .constants import Const
from .error_handlers import InvalidAPIUsage, ShortExistsException


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256))
    short = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(Const.MAIN_PAGE_VIEW, _external=True) + str(self.short))

    # def from_dict(self, data):
    #     if 'url' in data:
    #         setattr(self, 'original', data['url'])
    #     if 'custom_id' in data:
    #         setattr(self, 'short', data['custom_id'])

    @staticmethod
    def get_random_link(length):
        letters = string.ascii_letters + string.digits
        short_id = ''.join(random.choice(letters) for _ in range(length))
        if not URLMap.get_url_map(short_id):
            return short_id

    @staticmethod
    def get_url_map(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_url_map_or_404(short_id):
        return URLMap.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def add_url_map(original, short):
        if not short or short is None or len(short) == 0:
            short = URLMap.get_random_link(Const.RANDOM_LINK_LENGHT)
        else:
            if not re.match(Const.CUSTOM_ID_REGEXP, short):
                raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.get_url_map(short):
            raise ShortExistsException('Предложенный вариант короткой ссылки уже существует.')
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
