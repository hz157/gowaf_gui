'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-11 13:21:28
LastEditors: Ryan Zhang
LastEditTime: 2024-04-13 23:25:08
'''
from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class Log(Base):
    __tablename__ = 'ws_log'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    location = Column(String)
    message = Column(String)
    user = Column(String)
    datetime = Column(DateTime)

def NewLog(type, location, message, user):
    log = Log()
    log.type = type
    log.location = location
    log.message = message
    log.user = user
    log.datetime = datetime.now()
    return log

def LogRecord(mysql_session, level, location, message, user_id):
    log = NewLog(level, location, message, user_id)
    mysql_session.add(log)
    mysql_session.commit()