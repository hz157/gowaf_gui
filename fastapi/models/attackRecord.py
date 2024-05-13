from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class AttackRecord(Base):
    __tablename__ = 'eg_attack_record'

    id = Column(Integer, primary_key=True)
    uuid = Column(Integer)
    domain = Column(String)
    method = Column(String)
    url = Column(String)
    proto = Column(String)
    header = Column(String)
    body = Column(String)
    remoteAddr = Column(String)
    rule_name = Column(String)
    rule_desc = Column(String)
    datetime = Column(DateTime)
