from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AddOlimpiadsGroupForm(FlaskForm):
    name = StringField("Имя группы", validators=[InputRequired(message="Вы не заполнили это поле")])
    organizer = StringField("Организатор", validators=[InputRequired(message="Вы не заполнили это поле")])
    description = TextAreaField("Описание", validators=[InputRequired(message="Вы не заполнили это поле")])
    subjects = StringField("Предметы (через символы ', ')", validators=[InputRequired(message="Вы не заполнили это поле")])
    grades = StringField("Классы (через символы ', ')", validators=[InputRequired(message="Вы не заполнили это поле")])
    grades_description = StringField("Красивое описание классов", validators=[InputRequired(message="Вы не заполнили это поле")])
    link = StringField("Ссылка на официальный сайт", validators=[InputRequired(message="Вы не заполнили это поле")])
    cities = StringField("Города (через символы ', ')", validators=[InputRequired(message="Вы не заполнили это поле")])
    photo = FileField("Фотография")
    submit = SubmitField("Добавить")
