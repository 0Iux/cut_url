from random import randrange, choice
import string
from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm
from .models import URLMap


def get_unique_short_id(length=8):
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(choice(characters) for _ in range(length))
        if URLMap.query.filter_by(short=short_id).count() == 0:
            return short_id


def is_valid_short_id(short):
    if len(short) > 16:
        return False
    valid_symbols = string.ascii_letters + string.digits
    for letter in short:
        if letter not in valid_symbols:
            return False
    return True


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        original = form.original_link.data
        short = form.custom_id.data
        if not short:
            short = get_unique_short_id()
            url_map = URLMap(
                original=original,
                short=short
            )
            db.session.add(url_map)
            db.session.commit()
            flash(f'Ваша ссылка: {"http://127.0.0.1:5000/"+short}')
            return render_template('index.html', form=form)
        if not is_valid_short_id(short):
            flash('Ваша ссылка некорректна')
            return render_template('index.html', form=form)
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже существует!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=original,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        flash(f'Ваша ссылка: {"http://127.0.0.1:5000/"+short}')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def mapper_view(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
