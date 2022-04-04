import datetime
import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from .db_session import SqlAlchemyBase
from flask_login import UserMixin

association_table = sa.Table(
    'PostToUsers',
    SqlAlchemyBase.metadata, sa.Column('users', sa.Integer,
                                       sa.ForeignKey('users.id')),
    sa.Column('posts', sa.Integer,
              sa.ForeignKey('posts.id'))

)


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    login = sa.Column(sa.String)
    password = sa.Column(sa.String)
    avatar_im_path = sa.Column(sa.String)
    create_time = sa.Column(sa.DateTime,
                            default=datetime.datetime.now)

    posts = relationship("Post", secondary=association_table, backref="liked")

    def check_password(self, pas):
        return pas == self.password
