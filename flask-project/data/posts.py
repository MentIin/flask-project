import datetime
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase
import sqlalchemy as sa
from sqlalchemy.orm import relationship


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    create_time = sqlalchemy.Column(sqlalchemy.DateTime,
                                    default=datetime.datetime.now)
    title = sqlalchemy.Column(sqlalchemy.String)
    image_path = sqlalchemy.Column(sqlalchemy.String)


    user = orm.relation('User')
    liked_users = relationship("User", secondary="likes")


