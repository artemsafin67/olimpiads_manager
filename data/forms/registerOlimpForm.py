from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired


class RegisterOlimpForm(FlaskForm):
    subject = StringField("Предмет", validators=[InputRequired(message="Вы не заполнили это поле")])
    grade = StringField("Ваш класс", validators=[InputRequired(message="Вы не заполнили это поле")])
    city = StringField("Ваш город", validators=[InputRequired(message="Вы не заполнинили это поле")])
    submit = SubmitField("Участвовать")
