from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class TaskForm(FlaskForm):
    subject = StringField("Предмет", validators=[InputRequired(message="Вы не заполнили это поле")])
    grade = StringField("Ваш класс", validators=[InputRequired(message="Вы не заполнили это поле")])
    submit = SubmitField("Скачать задания")
