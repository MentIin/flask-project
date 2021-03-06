import datetime
from pathlib import Path
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash
from .db_session import SqlAlchemyBase

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
    hashed_password = sa.Column(sa.String)

    avatar_im_path = sa.Column(sa.String)
    create_time = sa.Column(sa.DateTime,
                            default=datetime.datetime.now)

    posts = relationship("Post", secondary=association_table, backref="liked")
    is_deleted = sa.Column(sa.Boolean)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def get_avatar_full_path(self):
        if self.avatar_im_path:
            avatar_path = Path("static", "avatars", self.avatar_im_path)
            return avatar_path
        else:
            return Path("static", "static-images", "default.png")
