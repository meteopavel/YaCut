import random
import string

from flask import abort, flash, render_template, redirect, url_for

from .forms import UrlCutForm
from .models import URLMap
from settings import RANDOM_LINK_LENGHT

from . import app, db


def get_random_link(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = UrlCutForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short = get_random_link(RANDOM_LINK_LENGHT)
        else:
            short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        link_pair = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(link_pair)
        db.session.commit()
        short_url = url_for('index_view', _external=True) + str(short)
        flash('Ваша новая ссылка готова: '
              f'<a href="{short_url}" target="_blank">{short_url}</a>')
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = URLMap.query.filter_by(short=short_id).first()
    if original_url is None:
        abort(404)
    return redirect(original_url.original)


@app.route('/error')
def error():
    abort(500)


if __name__ == '__main__':
    app.run()