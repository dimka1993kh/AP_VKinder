import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = sq.create_engine('postgresql+psycopg2://vk_admin_user:12345@localhost:5432/vkinder_result')
Session = sessionmaker(bind=engine)
