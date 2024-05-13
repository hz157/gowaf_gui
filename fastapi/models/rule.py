from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Rule(Base):
    __tablename__ = 'eg_rule'

    id = Column(Integer, primary_key=True)
    type = Column(String, default='Group')
    status = Column(String, default='valid')
    rule_name = Column(String)
    desc = Column(String)
    reg = Column(String)
    custom = Column(Integer, default='valid')
    datetime = Column(DateTime)
