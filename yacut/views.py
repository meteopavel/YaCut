from flask import abort, flash, render_template, redirect, url_for

from .forms import UrlCutForm
from .models import URLMap
from settings import RANDOM_LINK_LENGHT

from . import app, db


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = UrlCutForm()
    if form.validate_on_submit():
        if not form.custom_id.data:
            short_id = URLMap.get_random_link(RANDOM_LINK_LENGHT)
        else:
            short_id = form.custom_id.data
        if URLMap.get_url_map(short_id):
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)
        link_pair = URLMap(
            original=form.original_link.data,
            short=short_id,
        )
        db.session.add(link_pair)
        db.session.commit()
        short_url = url_for('index_view', _external=True) + str(short_id)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = URLMap.get_url_map_or_404(short_id)
    return redirect(original_url.original)


@app.route('/error')
def error():
    abort(500)


if __name__ == '__main__':
    app.run()