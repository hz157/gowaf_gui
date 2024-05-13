from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class DomainInfo(Base):
    __tablename__ = 'ws_domain_info'

    id = Column(Integer, primary_key=True)
    address = Column(Integer)
    upstream = Column(String)
    method = Column(String)
    port = Column(String)
    ssl = Column(Integer, default=0)
    cert_pem = Column(String)
    cert_key = Column(String)
    status = Column(Integer, default=1)
    datetime = Column(DateTime)
