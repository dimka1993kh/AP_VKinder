import sqlalchemy as sq
from sqlalchemy.orm import relationship
from .main import Base

class User(Base):
    __tablename__ = 'user'

    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    link = sq.Column(sq.String, unique=True)

class VkinderResult(Base):
    __tablename__ = 'vkinder_result'

    id = sq.Column(sq.Integer, primary_key=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey('user.id'))
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    link = sq.Column(sq.String)
    photo_1 = sq.Column(sq.String)
    photo_2 = sq.Column(sq.String)
    photo_3 = sq.Column(sq.String)

    user = relationship(User)