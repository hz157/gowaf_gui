'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-16 00:31:57
LastEditors: Ryan Zhang
LastEditTime: 2024-05-14 00:32:37
'''
from io import StringIO
import time
import psutil
import csv

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import Response as rp
from sqlalchemy import func, desc
from sqlalchemy.orm import Session

from fastapi.responses import FileResponse
from tempfile import NamedTemporaryFile
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from utils.constant import HTTP, STATUS_CODE
from utils.token import CheckJWTToken
from api.Response import Response
from utils.logger import logger
from utils.waf_engine import WAFEGHeartbeat
from dependent.mysql import GetMySQL
from dependent.redis import GetRedis
from utils.token import CheckJWTToken
from models.attackRecord import AttackRecord
from api.Response import Response
from utils.serialized import to_dict
from models.log import Log
from models.loginLog import LoginLog

DataRouter = APIRouter()


CTOA = ['XSS', 'SQL', 'PATH', 'TROJAN', 'CVE', 'OTHER']

# 攻击类型数据接口，获取各种攻击类型的统计数据
@DataRouter.get("/attack/type")
async def GetAttackTypeData(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):
    try:
        # 初始化 CTOA 类型的计数为 0
        result = {key: 0 for key in CTOA}

        # 获取总记录数
        total_count = mysql.query(func.count(AttackRecord.id)).scalar()

        # 查询并更新 CTOA 类型的计数
        for attack_type in CTOA:
            count = mysql.query(func.count(AttackRecord.id)).filter(
                AttackRecord.rule_name.like(f"%{attack_type}%")
            ).scalar()
            result[attack_type] = count

        # 计算包含 CTOA 的总计数
        included_ctoa_count = sum(result.values())

        # OTHER 类别为总数减去所有 CTOA 类别的总和
        result['OTHER'] = total_count - included_ctoa_count
        result['TOTAL'] = total_count

        # 将结果转换为列表格式，每个元素为 {"name": type, "value": count}
        formatted_result = [{"name": name, "value": value} for name, value in result.items()]

        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", formatted_result)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# 访问地图数据接口，获取访问地图的数据
@DataRouter.get("/request/map")
async def GetVisitMap(redis: Session = Depends(GetRedis(2)), token: str = Depends(CheckJWTToken)):
    try:
        # 获取 'location' 哈希的所有键值对
        key_value_pairs = redis.hgetall('location')
        # 将字节字符串键值对转换为字符串，并尝试将值转换为整数
        decoded_dict = []
        for key, value in key_value_pairs.items():
            try:
                decoded_dict.append({"name": key, "value": int(value)})
            except ValueError:
                pass  # 忽略无法转换为整数的值

        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", decoded_dict)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# QPS 数据接口，获取每秒请求数
@DataRouter.get("/request/qps")
async def GetQPS(redis: Session = Depends(GetRedis(2)), token: str = Depends(CheckJWTToken)):
    try:
        result = {"QPS": 0}
        # 获取 'qps_count' 的值
        qps_count_value = redis.get('qps_count')
        # 检查 qps_count_value 是否存在
        if qps_count_value is not None:
            # 将 qps_count_value 从字节字符串转换为整数
            result['QPS'] = int(qps_count_value)

        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", result)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# 请求计数数据接口，获取请求计数数据
@DataRouter.get("/request/count")
async def GetRequestData(redis: Session = Depends(GetRedis(2)), token: str = Depends(CheckJWTToken)):
    try:
        result = {"Request": 0}
        # 获取 'request_count_value' 的值
        request_count_value = redis.get('request_count')
        # 检查 request_count_value 是否存在
        if request_count_value is not None:
            # 将 request_count_value 从字节字符串转换为整数
            result['Request'] = int(request_count_value)

        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", result)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")


# 路由,用于获取系统状态信息
@DataRouter.get("/status/sys")
async def GetSysStatus(token: str = Depends(CheckJWTToken)):
    try:
        # 测量开始时的网络IO计数
        net_start = psutil.net_io_counters()
        # 等待一秒钟
        time.sleep(1)
        # 测量结束时的网络IO计数
        net_end = psutil.net_io_counters()

        # 计算每秒的上传和下载（单位：MB/s）
        up_speed = (net_end.bytes_sent - net_start.bytes_sent) / 1000000.0
        down_speed = (net_end.bytes_recv - net_start.bytes_recv) / 1000000.0

        # 获取 CPU 和内存使用情况
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "disk_usage": disk_usage,
            "network_speed": {
                "sent": up_speed,
                "recv": down_speed
            }
        })
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

@DataRouter.get("/status/wafserver")
async def GetWafServerStatus(type: str,  
                             uuid: str, 
                             token: str = Depends(CheckJWTToken)): 
    try:
        if not WAFEGHeartbeat(type, uuid):
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "FAIL", "failed")
        else:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", "success")
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
    

from sqlalchemy import desc, and_

@DataRouter.get("/attack/record")
async def GetAttackRecord(
    mysql: Session = Depends(GetMySQL),
    token: str = Depends(CheckJWTToken), 
    current: int = Query(1, ge=1),  # 页数，默认为1，最小值为1
    pageSize: int = Query(10, ge=1),  # 每页条目数，默认为10，最小值为1
    ip: Optional[str] = Query(None),  # 可选的ip参数
    uuid: Optional[str] = Query(None),  # 可选的uuid参数
    attackTime: List[str] = Query([]),  # 可选的attackTime参数，默认为空列表
):
    try:
        query = mysql.query(AttackRecord)
        # 根据参数构建查询条件
        if ip:
            query = query.filter(AttackRecord.remoteAddr.like(f'%{ip}%'))
        if uuid:
            query = query.filter(AttackRecord.uuid == uuid)
        if len(attackTime) == 2:
            # 两个attackTime参数都存在时，构建时间范围查询条件
            query = query.filter(and_(
                AttackRecord.datetime >= attackTime[0],
                AttackRecord.datetime <= attackTime[1]
            ))
        total_count = query.count()
        # 计算跳过的记录数
        offset = (current - 1) * pageSize
        # 查询并返回指定页面的数据，并按照 datetime 降序排序
        attacks = query.order_by(desc(AttackRecord.datetime)).offset(offset).limit(pageSize).all()
        result = [to_dict(attack, fields=['id', 'uuid', 'domain', 'method', 'url', 'proto', 'header', 'body', 'remoteAddr', 'rule_name', 'rule_desc', 'datetime']) for attack in attacks]
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

@DataRouter.get("/attack/record/download")
async def DownloadAttackRecord(
    mysql: Session = Depends(GetMySQL),
    token: str = Depends(CheckJWTToken), 
    ip: Optional[str] = Query(None),  # 可选的ip参数
    uuid: Optional[str] = Query(None),  # 可选的uuid参数
    attackTime: List[str] = Query([]),  # 可选的attackTime参数，默认为空列表
):
    try:
        query = mysql.query(AttackRecord)
        # 根据参数构建查询条件
        if ip:
            query = query.filter(AttackRecord.remoteAddr.like(f'%{ip}%'))
        if uuid:
            query = query.filter(AttackRecord.uuid == uuid)
        if len(attackTime) == 2:
            # 两个attackTime参数都存在时，构建时间范围查询条件
            query = query.filter(and_(
                AttackRecord.datetime >= attackTime[0],
                AttackRecord.datetime <= attackTime[1]
            ))
        # 查询数据并将结果转换为列表
        attacks = query.all()
        data = [
            ['id', 'uuid', 'domain', 'method', 'url', 'proto', 'header', 'body', 'remoteAddr', 'rule_name', 'rule_desc', 'datetime']
        ]
        for attack in attacks:
            data.append([
                attack.id, attack.uuid, attack.domain, attack.method, attack.url, attack.proto,
                attack.header, attack.body, attack.remoteAddr, attack.rule_name, attack.rule_desc, attack.datetime
            ])
        # 创建临时文件并将数据写入 CSV 文件
        with NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
            writer = csv.writer(tmp_file)
            writer.writerows(data)
        # 返回文件响应
        return FileResponse(tmp_file.name, filename="attack_records.csv")
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
    
@DataRouter.get("/log/action/")
async def GetActionLog(
    mysql: Session = Depends(GetMySQL),
    token: str = Depends(CheckJWTToken), 
    current: int = Query(1, ge=1),  # 页数，默认为1，最小值为1
    pageSize: int = Query(10, ge=1),  # 每页条目数，默认为10，最小值为1
    uid: Optional[str] = Query(None),  # 可选的uid参数
    api: Optional[str] = Query(None),  # 可选的api参数
    createdTime: List[str] = Query([]),  # 可选的createTime参数，默认为空列表
):
    try:
        query = mysql.query(Log)
        # 根据参数构建查询条件
        if uid:
            query = query.filter(Log.user == uid)
        if api:
            query = query.filter(Log.location.like(f'%{api}%'))
        if len(createdTime) == 2:
            # 两个attackTime参数都存在时，构建时间范围查询条件
            query = query.filter(and_(
                Log.datetime >= createdTime[0],
                Log.datetime <= createdTime[1]
            ))
        total_count = query.count()
        # 计算跳过的记录数
        offset = (current - 1) * pageSize
        # 查询并返回指定页面的数据，并按照 datetime 降序排序
        attacks = query.order_by(desc(Log.datetime)).offset(offset).limit(pageSize).all()
        result = [to_dict(attack, fields=['id', 'type', 'location', 'message', 'user', 'datetime']) for attack in attacks]
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
    
@DataRouter.get("/log/login/")
async def GetLoginLog(
    mysql: Session = Depends(GetMySQL),
    token: str = Depends(CheckJWTToken), 
    current: int = Query(1, ge=1),  # 页数，默认为1，最小值为1
    pageSize: int = Query(10, ge=1),  # 每页条目数，默认为10，最小值为1
    ip: Optional[str] = Query(None),  # 可选的ip参数
    createdTime: List[str] = Query([]),  # 可选的createTime参数，默认为空列表
):
    try:
        query = mysql.query(LoginLog)
        # 根据参数构建查询条件
        if ip:
            query = query.filter(LoginLog.login_ip.like(f'%{ip}%'))
        if len(createdTime) == 2:
            # 两个createdTime参数都存在时，构建时间范围查询条件
            query = query.filter(and_(
                LoginLog.login_time >= createdTime[0],
                LoginLog.login_time <= createdTime[1]
            ))
        total_count = query.count()
        # 计算跳过的记录数
        offset = (current - 1) * pageSize
        # 查询并返回指定页面的数据，并按照 datetime 降序排序
        login_logs = query.order_by(desc(LoginLog.login_time)).offset(offset).limit(pageSize).all()
        result = [to_dict(login_log, fields=['id', 'user', 'status', 'login_ip', 'login_time']) for login_log in login_logs]
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
    

@DataRouter.get("/log/login/download")
async def download_login_log(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):
    try:
        query = mysql.query(LoginLog)
        # 查询所有数据
        login_logs = query.order_by(desc(LoginLog.login_time)).all()

        # 创建一个 CSV 输出流
        output = StringIO()
        writer = csv.writer(output)

        # 写入CSV头部
        writer.writerow(['id', 'user', 'status', 'ip', 'datetime'])

        # 写入数据
        for log in login_logs:
            print([log.id, log.user, log.status, log.login_ip, str(log.login_time)])
            writer.writerow([log.id, log.user, log.status, log.login_ip, str(log.login_time)])

        # 重置文件读取指针到开始位置
        # output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # 设置正确的headers
        headers = {
            'Content-Disposition': 'attachment; filename="login_logs.csv"'
        }

        return rp(content=csv_content, media_type="text/csv", headers=headers)

    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
    

@DataRouter.get("/log/action/download")
async def download_login_log(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):
    try:
        query = mysql.query(Log)
        # 查询所有数据
        logs = query.order_by(desc(Log.datetime)).all()

        # 创建一个 CSV 输出流
        output = StringIO()
        writer = csv.writer(output)

        # 写入CSV头部
        writer.writerow(['id', 'level', 'api', 'msg', 'user', 'datetime'])

        # 写入数据
        for log in logs:
            # print([log.id, log.type, log.location, log.message, log.user, str(log.datetime)])
            writer.writerow([log.id, log.type, log.location, log.message, log.user, str(log.datetime)])

        # output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # 设置正确的headers
        headers = {
            'Content-Disposition': 'attachment; filename="action_logs.csv"'
        }

        return rp(content=csv_content, media_type="text/csv", headers=headers)


    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
    
@DataRouter.get("/log/attack/download")
async def download_login_log(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):
    try:
        query = mysql.query(AttackRecord)
        # 查询所有数据
        logs = query.order_by(desc(AttackRecord.datetime)).all()

        # 创建一个 CSV 输出流
        output = StringIO()
        writer = csv.writer(output)

        # 写入CSV头部
        writer.writerow(['uuid', 'domain', 'url', 'method', 'proto', 'header', 'body', 'remoteAddr', 'rule_name', 'rule_desc', 'datetime'])

        # 写入数据
        for log in logs:
            writer.writerow([log.uuid, log.domain, log.url, log.method, log.proto, log.header, log.body, log.remoteAddr, log.rule_name, log.rule_desc, str(log.datetime)])
        # output.seek(0)
        csv_content = output.getvalue()
        output.close()

        # 设置正确的headers
        headers = {
            'Content-Disposition': 'attachment; filename="attack_logs.csv"'
        }

        return rp(content=csv_content, media_type="text/csv", headers=headers)


    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

