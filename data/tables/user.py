from data.database.all_for_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    surname = sqlalchemy.Column(sqlalchemy.String)
    fatherhood = sqlalchemy.Column(sqlalchemy.String)
    grade = sqlalchemy.Column(sqlalchemy.Integer)
    photo = sqlalchemy.Column(sqlalchemy.String)
    olimpiads = orm.relationship('Olimpiad', secondary='user_to_olimpiad')
    email = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)