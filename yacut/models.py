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

    @staticmethod
    def get_random_link(length):
        letters = string.ascii_letters + string.digits
        short_id = ''.join(random.choice(letters) for _ in range(length))
        if not URLMap.get_by_short_id(short_id):
            return short_id

    @staticmethod
    def get_by_short_id(short_id):
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def get_by_short_id_or_404(short_id):
        return URLMap.query.filter_by(short=short_id).first_or_404()

    @staticmethod
    def add_url_map(original, short):
        if not short:
            short = URLMap.get_random_link(Const.RANDOM_LINK_LENGHT)
        elif not re.match(Const.CUSTOM_ID_REGEXP, short):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.get_by_short_id(short):
            raise ShortExistsException('Предложенный вариант короткой ссылки уже существует.')
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
