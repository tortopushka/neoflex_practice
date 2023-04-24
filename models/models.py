from sqlalchemy import Column, String, DateTime, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Cache(Base):
    __tablename__ = 'cache'
    id_cache = Column(Integer, primary_key=True)
    date_of_activity = Column(DateTime)
    text_of_message = Column(Text)
    language_code = Column(String)