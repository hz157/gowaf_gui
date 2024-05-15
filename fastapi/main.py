'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-05-13 23:28:47
LastEditors: Ryan Zhang
LastEditTime: 2024-05-15 16:14:55
'''
import uvicorn
import utils.config as config
import utils.waf_engine as waf

from utils.logger import logger
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from api.RuleApi import RuleRouter
from api.UserApi import UserRouter
from api.DataApi import DataRouter
from starlette.middleware.base import BaseHTTPMiddleware
from dependent.redis import RedisConnection
from models.platform import Platform
from utils.waf_engine import PlatformCheck, StartServer, StartGate

import uuid

app = FastAPI()
app.include_router(RuleRouter, prefix="/api/rule")
app.include_router(UserRouter, prefix="/api/user")
app.include_router(DataRouter, prefix="/api/data")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)


# 请求记录中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # 记录请求信息
    logger.info(f"Request received: {request.method} {request.url} | Request client: {request.client.host}:{request.client.port}")

    response = await call_next(request)

    return response


@app.get("/")
async def root():
    return {"message": "GoWAF GUI Start Successfully"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    platform = PlatformCheck()
    if platform.os_name == "Linux":
        rootPath = platform._linux_root_path
    elif platform.os_name == "Windows":
        rootPath = platform._windows_root_path
    else:
        print("Platform not supported")
        input()
        exit()
    StartServer()
    StartGate()
    c = config.read_config("./config/apiconf.yaml")
    uvicorn.run(app, host=c["server"]["host"], port=c["server"]["port"])
