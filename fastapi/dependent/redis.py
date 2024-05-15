'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-05-13 23:28:47
LastEditors: Ryan Zhang
LastEditTime: 2024-05-15 16:13:43
'''
import redis
import utils.config as config
from utils.logger import logger
from contextlib import contextmanager

def ConnectRedis(db_num):
    """连接到Redis数据库"""
    try:
        c = config.read_config("./config/apiconf.yaml")
        # 连接到Redis
        r = redis.Redis(
            host=c['redis']['host'],
            port=c['redis']['port'],
            db=db_num,
            password=c['redis']['password'],
            decode_responses=True  # 自动解码返回结果
        )
        # 测试连接是否成功
        r.ping()
        logger.info("Connected to Redis successfully.")
        return r
    except Exception as e:
        logger.error(f'Redis connect error: {e}')
        return None

def CloseRedis(redis_client):
    """关闭Redis连接"""
    try:
        redis_client.close()
        logger.info("Redis connection closed successfully.")
    except Exception as e:
        logger.error(f'Redis close error: {e}')
    

def GetRedis(db_num):
    def dependency():
        db = ConnectRedis(db_num)
        try:
            yield db
        finally:
            db.close()
    return dependency

@contextmanager
def RedisConnection(db_num):
    client = ConnectRedis(db_num)
    try:
        yield client
    finally:
        client.close()