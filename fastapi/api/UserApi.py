import time
from pydantic import BaseModel
from sqlalchemy import and_, func



from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse


from datetime import datetime
from dependent.mysql import GetMySQL
from dependent.redis import GetRedis
from utils.constant import HTTP, STATUS_CODE
from utils.serialized import EncodeCustom
from models.loginLog import NewLoginLog
from models.log import NewLog
from models.user import User
from utils.hash import DataHash
from utils.token import CreateJWTToken
from utils.token import CheckJWTToken
from api.Response import Response
from utils.logger import logger
from utils.serialized import to_dict
from models.log import LogRecord

UserRouter = APIRouter()

# 登录接口请求体
class LoginRequest(BaseModel):
    username: str
    password: str
    timestamp: int

# 登录接口
@UserRouter.post("/login")
async def Login(res: LoginRequest, request: Request, mysql: Session = Depends(GetMySQL), redis: Session = Depends(GetRedis(15))):  
    try:
        requestBody = res
        # 获取当前的Unix时间戳
        current_timestamp = int(time.time())
        # 检查时间戳的偏差超过10s或用户名或密码为空
        if abs(current_timestamp - int(requestBody.timestamp)) > 10 or requestBody.username is None or requestBody.password is None:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS", "Illegal data")
        # 密码哈希计算
        hashed_password = DataHash(requestBody.password, salt="gowaf")
        userData = mysql.query(User).filter(User.username == requestBody.username).first()
        if not userData or userData.password != hashed_password or userData.status != 1:
            mysql.add(NewLoginLog(userData.id, "Success", datetime.now(), request.client.host))
            mysql.commit()
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", "Invalid username or password")
        
        resp = [userData.last_login_time, userData.last_login_ip]
        # 更新登录时间和IP
        userData.last_login_time = datetime.now()
        userData.last_login_ip = request.client.host  # 使用request.client.host获取用户IP
        mysql.add(NewLoginLog(userData.id, "Success", datetime.now(), request.client.host))
        mysql.commit()  # 提交更改到数据库
        
        access_token = CreateJWTToken(data={"uid": userData.id})
        redis.set(userData.id, access_token, ex=600)
        print(access_token)
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", {
                                         "token": access_token,
                                         "userInfo": {
                                             "username": userData.username,
                                             "last_login_time": str(resp[0]),
                                             "last_login_ip": resp[1]
                                         }
                                     })
    except Exception as e:
        logger.error(e)
        mysql.add(NewLoginLog(userData.id, "error", datetime.now(), request.client.host))
        mysql.commit()
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# 新增用户接口请求体
class AddUserRequest(BaseModel):
    username: str
    password: str
    timestamp: int

# 新增用户接口
@UserRouter.post("/add")
async def AddUser(res: AddUserRequest, mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):  
    location = '/api/user/add'
    try:
        requestBody = res
        # 获取当前的Unix时间戳
        current_timestamp = int(time.time())
        # 检查时间戳的偏差超过10s或用户名或密码为空
        if abs(current_timestamp - requestBody.timestamp) > 10 or requestBody.username is None or requestBody.password is None:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS", "Illegal data")
        if token['uid'] != 10000000:
            return Response(HTTP.HTTP_403_FORBIDDEN, STATUS_CODE.TOKEN_0_OK,  "FORBIDDEN")
        # 密码哈希计算
        hashed_password = DataHash(requestBody.password, salt="gowaf")
        user = User()
        user.username = requestBody.username
        user.password = hashed_password
        mysql.add(user)
        mysql.commit()
        LogRecord(mysql, 'INFO', location, f'增加用户{requestBody.username}-成功', token['uid'])
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS", {"username": user.username})
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'增加用户{requestBody.username}-失败', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# 修改密码接口请求体
class ChangePwdRequest(BaseModel):
    username: str
    new_password: str
    timestamp: int

# 修改密码接口
@UserRouter.post("/changepwd")
async def ChangePwd(res: ChangePwdRequest, mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):  
    location = '/api/user/changepwd'
    try:
        requestBody = res
        # 获取当前的Unix时间戳
        current_timestamp = int(time.time())
        # 检查时间戳的偏差超过10s或用户名或密码为空
        if abs(current_timestamp - requestBody.timestamp) > 10:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS", "Illegal data")
        if token['uid'] != 10000000 and token['uid'] != userData.id:
            return Response(HTTP.HTTP_403_FORBIDDEN, STATUS_CODE.TOKEN_0_OK,  "FORBIDDEN")
        userData = mysql.query(User).filter(User.username == requestBody.username).first()
        if token['uid'] == 10000000:
            # 密码哈希计算
            hashed_password = DataHash(requestBody.new_password, salt="gowaf")
            userData.username = requestBody.username
            userData.password = hashed_password
            LogRecord(mysql, 'INFO', location, f'修改{requestBody.username}密码-成功', token['uid'])
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK,  "SUCCESS")
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'修改{requestBody.username}密码-失败', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")
        

# 获取个人信息
@UserRouter.get("/info")
async def GetInfo(mysql: Session = Depends(GetMySQL), token: str = Depends(CheckJWTToken)):  
    try:
        userData = mysql.query(User).filter(User.id == token['uid']).first()
        if token['uid'] == 10000000:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", {"username": userData.username,
                                                                                  "role": "admin"})
        else:
            return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", {"username": userData.username,
                                                                                  "role": "user"})
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR", str(e))


# 获取用户列表
@UserRouter.get("/get")
async def GetUsers(mysql: Session = Depends(GetMySQL),
                      token: str = Depends(CheckJWTToken), 
                      page: int = Query(1, ge=1),  # 页数，默认为1，最小值为1
                      page_size: int = Query(10, ge=1)  # 每页条目数，默认为10，最小值为1
):
    try:
        if token['uid'] != 10000000:
            return Response(HTTP.HTTP_403_FORBIDDEN, STATUS_CODE.TOKEN_0_OK,  "FORBIDDEN")
        total_count = mysql.query(func.count(User.id)).scalar()
        # 计算跳过的记录数
        offset = (page - 1) * page_size
        # 查询并返回指定页面的用户数据
        users = mysql.query(User)\
                     .offset(offset)\
                     .limit(page_size)\
                     .all()
        result = [to_dict(user, fields=['id', 'username', 'status']) for user in users]
        # 包装分页信息
        page_info = {
            "page": page,
            "size": page_size,
            "total": total_count,
            "users": result
        }
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS", page_info)
    except Exception as e:
        logger.error(e)
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")

# 停用账户
@UserRouter.get("/disable")
async def DisableUser(mysql: Session = Depends(GetMySQL),
                     token: str = Depends(CheckJWTToken), 
                     uid: int = Query()
):
    location = '/api/user/disable'
    try:
        if token['uid'] != 10000000 or uid == 10000000:
            return Response(HTTP.HTTP_403_FORBIDDEN, STATUS_CODE.TOKEN_0_OK,  "FORBIDDEN")
        userData = mysql.query(User).filter(User.id == uid).first()
        userData.status = 0
        mysql.commit()
        LogRecord(mysql, 'INFO', location, f'停用用户{userData.username}-成功', token['uid'])
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS")
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'停用用户{userData.username}-失败', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR")


# 启用账户
@UserRouter.get("/enable")
async def EnableUser(mysql: Session = Depends(GetMySQL),
                     token: str = Depends(CheckJWTToken), 
                     uid: int = Query()
):
    location = '/api/user/enable'
    try:
        if token['uid'] != 10000000 or uid == 10000000:
            return Response(HTTP.HTTP_403_FORBIDDEN, STATUS_CODE.TOKEN_0_OK,  "FORBIDDEN")
        userData = mysql.query(User).filter(User.id == uid).first()
        userData.status = 1
        mysql.commit()
        LogRecord(mysql, 'INFO', location, f'启用用户{userData.username}-成功', token['uid'])
        return Response(HTTP.HTTP_200_OK, STATUS_CODE.TOKEN_0_OK, "SUCCESS")
    except Exception as e:
        logger.error(e)
        LogRecord(mysql, 'INFO', location, f'启用用户{userData.username}-失败', token['uid'])
        return Response(HTTP.HTTP_500_INTERNAL_SERVER_ERROR, STATUS_CODE.SERVER_2_ERROR, "ERROR", str(e))
