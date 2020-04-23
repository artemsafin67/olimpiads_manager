from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, BooleanField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = StringField("Почта", validators=[InputRequired(message="Вы не заполнили это поле")])
    password = PasswordField("Пароль", validators=[InputRequired(message="Вы не заполнили это поле")])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
