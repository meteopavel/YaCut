from flask import abort, flash, render_template, redirect, url_for

from .error_handlers import ShortExistsException
from .forms import UrlCutForm
from .models import URLMap
from .constants import Const

from . import app


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = UrlCutForm()
    if form.validate_on_submit():
        try:
            url_map = URLMap.add_url_map(original=form.original_link.data,
                                         short=form.custom_id.data)
        except ShortExistsException as exception:
            flash(str(exception))
            return render_template('index.html', form=form)
        short_url = url_for(Const.MAIN_PAGE_VIEW, _external=True) + str(url_map.short)
        return render_template('index.html', form=form, short_url=short_url)
    return render_template('index.html', form=form)


@app.route('/<short_id>')
def redirect_to_original(short_id):
    original_url = URLMap.get_by_short_id_or_404(short_id)
    return redirect(original_url.original)


@app.route('/error')
def error():
    abort(500)


if __name__ == '__main__':
    app.run()