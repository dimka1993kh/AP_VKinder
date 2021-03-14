import sqlalchemy as sq
from .main import Base

class Vkinder_result(Base):
    __tablename__ = 'vkinder_result'
    id = sq.Column(sq.Integer, primary_key=True)
    first_name = sq.Column(sq.String)
    last_name = sq.Column(sq.String)
    # country = sq.Column(sq.String)
    # city = sq.Column(sq.String)
    link = sq.Column(sq.String)
    photo_1 = sq.Column(sq.String)
    photo_2 = sq.Column(sq.String)
    photo_3 = sq.Column(sq.String)

