from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional


class LinkForm(FlaskForm):
    original = URLField(
        'Длинная ссылка"',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 256)]
    )
    short = URLField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')
