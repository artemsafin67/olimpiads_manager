from data.database. all_for_session import SqlAlchemyBase
import sqlalchemy
from sqlalchemy import orm


class Olimpiad(SqlAlchemyBase):
    __tablename__ = 'olimpiads'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    subject = sqlalchemy.Column(sqlalchemy.String)
    grade = sqlalchemy.Column(sqlalchemy.String)
    city = sqlalchemy.Column(sqlalchemy.String)
    tasks = sqlalchemy.Column(sqlalchemy.String)
    results = sqlalchemy.Column(sqlalchemy.String)
    olimpiads_group_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpiads_groups.id'))
    registration_data = orm.relation("OlimpiadRegistration", backref='olimpiad', uselist=False)

    def __repr__(self):
        return f"<Olimpiad> {self.subject}, {self.grade}, {self.city}"
