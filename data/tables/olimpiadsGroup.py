from data.database.all_for_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class OlimpiadsGroup(SqlAlchemyBase):
    __tablename__ = 'olimpiads_groups'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    organizer = sqlalchemy.Column(sqlalchemy.String)
    subjects = sqlalchemy.Column(sqlalchemy.String)
    grades = sqlalchemy.Column(sqlalchemy.String)
    cities = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String)
    news = orm.relationship('OlimpiadsGroupNews', backref='olimpiads_group_news')
    olimpiads = orm.relationship('Olimpiad', backref='olimpiads_group')

    def __repr__(self):
        return f"<OlimpiadsGroup> {self.name}"
