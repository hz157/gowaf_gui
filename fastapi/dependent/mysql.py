"""
Module/Script Name: MySQL Dependent
Author: RyanZhang
Date: 1/12/2023

Description: MySQL数据库依赖
Interface_List:

Dependencies:
- sqlalchemy

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import utils.config as config
from utils.logger import logger


def ConnectSQL():
    try:
        c = config.read_config("./config/apiconf.yaml")
        # MySQL数据库
        sqlserver = f'{c["database"]["drive"]}+pymysql://{c["database"]["user"]}:{c["database"]["password"]}@{c["database"]["host"]}/{c["database"]["db"]}'
        engine = create_engine(sqlserver)
        # 创建会话
        session = Session(engine)
        return session
    except Exception as e:
        logger.error(f'DBconnectError: {e}')


def CloseSQL(session):
    # 关闭MySQL数据库
    session.close()

def GetMySQL():
    db = ConnectSQL()
    try:
        yield db
    finally:
        db.close()