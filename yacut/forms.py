from flask_wtf import FlaskForm
from wtforms import URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class UrlCutForm(FlaskForm):
    original_link = URLField(
        'Введите оригинальную ссылку',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    custom_id = URLField(
        'Введите свой вариант ссылки не более 16 символов',
        validators=[Length(1, 16), Optional()]
    )
    submit = SubmitField('Создать')
