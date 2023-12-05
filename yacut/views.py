from random import randrange

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import LinkForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = LinkForm()
    if form.validate_on_submit():
        short = form.short.data
        if URLMap.query.filter_by(short=short).first():
            flash('Такая короткая ссылка уже существует!')
            return render_template('index.html', form=form)
        url = URLMap(
            original=form.original.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def opinion_view(short):
    link = URLMap.query.get_or_404(short)
    return redirect(link.original)
