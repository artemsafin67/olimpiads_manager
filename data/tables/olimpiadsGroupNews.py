from data.database.all_for_session import SqlAlchemyBase
import sqlalchemy

import datetime


class OlimpiadsGroupNews(SqlAlchemyBase):
    __tablename__ = 'olimpiad_group_news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.String)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    olimpiad_group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpiads_groups.id'))

