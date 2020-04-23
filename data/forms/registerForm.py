from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, FileField
from wtforms.validators import InputRequired, EqualTo, Email, NumberRange


class RegisterForm(FlaskForm):
    photo = FileField("")
    name = StringField("Имя", validators=[InputRequired(message="Вы не заполнили это поле")])
    surname = StringField("Имя", validators=[InputRequired(message="Вы не заполнили это поле")])
    fatherhood = StringField("Имя", validators=[InputRequired(message="Вы не заполнили это поле")])
    grade = IntegerField("Класс обучения", validators=[NumberRange(1, 11, message="Неправильно указан класс")])
    email = StringField("Почта", validators=[InputRequired(message="Вы не заполнили это поле"),
                                             Email(message="Неправильно указана почта")])
    password = PasswordField("Пароль", validators=[InputRequired(message="Вы не заполнили это поле")])
    password_again = PasswordField("Пароль ещё раз", validators=[InputRequired(message="Вы не заполнили это поле"), EqualTo("password", "Пароли не совпадают")])
    submit = SubmitField("Зарегистрироваться")
