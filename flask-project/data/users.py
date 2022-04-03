import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    avatar_im_path = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.datetime.now)
    posts = orm.relation("User", back_populates='user')
    likes = relationship("Post", secondary="likes")
