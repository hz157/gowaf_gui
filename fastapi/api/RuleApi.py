from io import StringIO
import json
import math
import os
import csv
import uuid
from typing import Optional


from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session
from datetime import datetime
from starlette.responses import JSONResponse, FileResponse
from sqlalchemy import literal_column
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, FileResponse
from utils.constant import HTTP, STATUS_CODE
from dependent.mysql import GetMySQL
from dependent.redis import GetRedis
from fastapi import APIRouter, Depends
from api.Response import Response
from utils.waf_sys import CheckPortUse
from utils.token import CheckJWTToken
from models.log import LogRecord
from models.rule import Rule
from utils.logger import logger
from utils.serialized import to_dict
from utils.waf_engine import StartServer

RuleRouter = APIRouter()

class ResRule(BaseModel):
    name: str
    desc: str
    reg: str
    field: str

@RuleRouter.post("/add")
async def AddRule(res: ResRule, token: str = Depends(CheckJWTToken), mysql: Session = Depends(GetMySQL), redis: Session = Depends(GetRedis(0))): 
    location = '/api/rule/add'
    try:
        requestBody = res
        rule = Rule()
        rule.rule_name = requestBody.name
        rule.desc = requestBody.desc
        reg = {"op":"is", "val": requestBody.reg, "empty": False, "field": requestBody.field}
        rule.reg = json.dumps(reg)
        rule.custom = 0
        rule.datetime = datetime.now()
        mysql.add(rule)
        mysql.commit()
        LogRecord(mysql, 'INFO', location, f'增加规则{requestBody.name}-成功', token['uid'])
        server = redis.hgetall('WafServerConfig-8000')
        print(f"kill -9 {server['PID']}")
        os.system(f"kill -9 {server['PID']}")
        StartServer()
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS")
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'增加规则{requestBody.name}-失败 | Write cache failed error: {str(e)}', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")


class ResSwitchRule(BaseModel):
    rule_id: int

@RuleRouter.post("/switch")
async def SwitchRule(res: ResSwitchRule, token: str = Depends(CheckJWTToken), mysql: Session = Depends(GetMySQL), redis: Session = Depends(GetRedis(0))): 
    location = '/api/rule/switch'
    try:
        rule = mysql.query(Rule).filter(Rule.id == res.rule_id).first()
        if rule.status == 'invalid':
            rule.status = "valid"
        else:
            rule.status = "invalid"
        mysql.commit()
        LogRecord(mysql, 'INFO', location, f'切换规则状态{rule.rule_name}-成功', token['uid'])
        server = redis.hgetall('WafServerConfig-8000')
        print(f"kill -9 {server['PID']}")
        os.system(f"kill -9 {server['PID']}")
        StartServer()
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS")
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'切换规则状态{rule.rule_name}-失败 | Write cache failed error: {str(e)}', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

@RuleRouter.get("/get")
async def GetRule(
    mysql: Session = Depends(GetMySQL),
    token: str = Depends(CheckJWTToken), 
    current: int = Query(1, ge=1),  # 页数，默认为1，最小值为1
    pageSize: int = Query(10, ge=1),  # 每页条目数，默认为10，最小值为1
    name: Optional[str] = Query(None),  # 可选的名字参数
    number: Optional[str] = Query(None),  # 可选的number参数
    status: Optional[str] = Query(None),  # 可选的status参数
):
    try:
        query = mysql.query(Rule)
        # 根据参数构建查询条件
        if name:
            query = query.filter(Rule.rule_name.like(f'%{name}%'))
        if number:
            query = query.filter(Rule.id == number)
        if status:
            query = query.filter(Rule.status == status)
        total_count = query.count()
        # 计算跳过的记录数
        offset = (current - 1) * pageSize
        # 查询并返回指定页面的用户数据
        rules = query.offset(offset).limit(pageSize).all()
        result = [to_dict(rule, fields=['id', 'status', 'rule_name', 'desc', 'reg', 'datetime']) for rule in rules]
        # 包装分页信息
        page_info = {
            "current": current,
            "pageSize": pageSize,
            "total": total_count,
            "data": result
        }
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", page_info)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
    
@RuleRouter.get("/download")
async def download_login_log(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):
    try:
        query = mysql.query(Rule)
        # 查询所有数据
        rules = query.all()

        # 创建一个 CSV 输出流
        output = StringIO()
        writer = csv.writer(output)

        # 写入CSV头部
        writer.writerow(['id', 'status', 'rule_name', 'desc', 'reg'])

        # 写入数据
        for rule in rules:
            writer.writerow([rule.id, rule.status, rule.rule_name, rule.desc, rule.reg])

        # 重置文件读取指针到开始位置
        output.seek(0)
        return Response(content=output.read(), media_type="text/csv")

    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

