from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class LoginLog(Base):
    __tablename__ = 'ws_restriction_ip'

    id = Column(Integer, primary_key=True)
    ip = Column(String)
    user = Column(Integer)
    datetime = Column(DateTime)
