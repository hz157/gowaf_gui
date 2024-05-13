'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-14 21:58:20
LastEditors: Ryan Zhang
LastEditTime: 2024-04-14 22:12:22
'''
import utils.config as config

from fastapi import Depends, FastAPI, HTTPException
from dependent.redis import GetRedis
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

c = config.read_config("./config/apiconf.yaml")
SECRET_KEY = c["jwt"]["key"]
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = c["jwt"]["expire"]


# 生成 Token 的函数
def CreateJWTToken(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2PasswordBearer 是 FastAPI 内置的一个类，用于处理获取 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 解析 Token 的函数
def CheckJWTToken(token: str = Depends(oauth2_scheme), redis = Depends(GetRedis(15))):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 检查 Redis 是否有此 token
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("uid")
        if uid is None:
            raise credentials_exception
        rToken = redis.get(uid)
        if rToken != token:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")
        redis.expire(uid, 300)  # 设置或刷新 token 的 TTL 为 600 秒（10分钟）
        redis.close()
        return payload  # 返回验证后的用户信息
    except JWTError:
        raise credentials_exception


# # 被保护的资源，只有在请求中包含有效 Token 时才能访问
# @app.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     return {"message": "You have access to this protected route!"}
