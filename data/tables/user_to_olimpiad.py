from data.database.all_for_session import SqlAlchemyBase
import sqlalchemy

user_to_olimpiad = sqlalchemy.Table('user_to_olimpiad', SqlAlchemyBase.metadata,
                                    sqlalchemy.Column('user', sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id')),
                                    sqlalchemy.Column('olimpiad', sqlalchemy.Integer,
                                                      sqlalchemy.ForeignKey('olimpiads.id')))

