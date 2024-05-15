from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from datetime import datetime
from utils.constant import HTTP, STATUS_CODE

# class ResponseModel(BaseModel):
#     status: str
#     message: str
#     data: dict = {}


def Response(httpCode: HTTP, statusCode: STATUS_CODE, message: str, data: dict = None):
    return JSONResponse(status_code=httpCode, content={
        'code': statusCode,
        'message': message,  # 状态码，例如 "success" 或 "error"
        'data': data,      # 数据内容
        'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 响应时间
    })