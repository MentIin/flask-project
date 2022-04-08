import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from data.db_session import SqlAlchemyBase


class Likes(SqlAlchemyBase):
    __tablename__ = 'likes'
    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    post_id = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))

    user = relationship("User", backref=backref("likes", cascade="all, delete-orphan"))
    post = relationship("Post", backref=backref("likes", cascade="all, delete-orphan"))
