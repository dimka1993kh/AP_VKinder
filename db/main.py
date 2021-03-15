from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sq

Base = declarative_base()
engine = sq.create_engine('postgresql+psycopg2://vk_admin_user:12345@localhost:5432/vkinder_result')


