from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import Const


class UrlCutForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(Const.ORIGINAL_LINK_LIMITS['lower'],
                           Const.ORIGINAL_LINK_LIMITS['upper'])]
    )
    custom_id = URLField(
        'Введите свой вариант ссылки не более 16 символов',
        validators=[Length(Const.CUSTOM_ID_LIMITS['lower'],
                           Const.CUSTOM_ID_LIMITS['upper']),
                    Regexp(Const.CUSTOM_ID_REGEXP,
                           message='Разрешены только большие латинские буквы, '
                                   'маленькие латинские буквы, '
                                   'цифры в диапазоне от 0 до 9.'),
                    Optional()]
    )
    submit = SubmitField('Создать')
