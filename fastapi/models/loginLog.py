from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class LoginLog(Base):
    __tablename__ = 'ws_login_log'

    id = Column(Integer, primary_key=True)
    user = Column(Integer)
    status = Column(String)
    login_ip = Column(String)
    login_time = Column(DateTime)

def NewLoginLog(id, status, login_time, login_ip):
    loginLog = LoginLog()
    loginLog.user = id
    loginLog.status = status
    loginLog.login_time = login_time
    loginLog.login_ip = login_ip  # 使用request.client.host获取用户IP
    return loginLog