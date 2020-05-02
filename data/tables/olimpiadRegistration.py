from data.database.all_for_session import SqlAlchemyBase
import sqlalchemy


class OlimpiadRegistration(SqlAlchemyBase):
    __tablename__ = 'olimpiads_registration'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    documents = sqlalchemy.Column(sqlalchemy.String)
    olimpiad_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('olimpiads.id'))

    def __repr__(self):
        return f"<OlimpiadRegistration> {self.date}, {self.documents}, {self.address}"
