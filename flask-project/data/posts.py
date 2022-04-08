import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    create_time = sa.Column(sa.DateTime,
                            default=datetime.datetime.now)
    title = sa.Column(sa.String)
    image_path = sa.Column(sa.String)

    user_id = sa.Column(sa.Integer,
                        sa.ForeignKey("users.id"))
    user = orm.relation('User')
