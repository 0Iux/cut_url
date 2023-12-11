from flask import flash, redirect, render_template


from . import app, db
from .forms import LinkForm
from .models import URLMap
from .utils import is_valid_short_id, get_unique_short_id


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
            flash(f'{"http://127.0.0.1:5000/"+short}')
            return render_template('index.html', form=form)
        if not is_valid_short_id(short):
            flash('Ваша ссылка некорректна')
            return render_template('index.html', form=form)
        if URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
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
