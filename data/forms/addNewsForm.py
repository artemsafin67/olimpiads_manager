from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, BooleanField, TextAreaField
from wtforms.validators import InputRequired


class AddNewsForm(FlaskForm):
    is_group_news = BooleanField("Для группы олимпиад")
    group_name = StringField("Имя группы")
    title = StringField("Заголовок", validators=[InputRequired(message="Вы не заполнили это поле")])
    description = TextAreaField("Описание", validators=[InputRequired(message="Вы не заполнили это поле")])
    text = TextAreaField("Текст", validators=[InputRequired(message="Вы не заполнили это поле")])
    photo = FileField("Фотография")
    submit = SubmitField("Добавить")
