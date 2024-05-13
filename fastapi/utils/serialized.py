'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-16 00:31:58
LastEditors: Ryan Zhang
LastEditTime: 2024-04-25 04:17:06
'''
from datetime import date, datetime
import datetime
from sqlalchemy.orm import DeclarativeMeta


def to_dict(obj, fields=None):
    if fields:
        return {field: getattr(obj, field) if field not in ['login_time', 'datetime'] else getattr(obj, field).isoformat() for field in fields}
    else:
        return {attr: getattr(obj, attr) if attr not in ['login_time', 'datetime'] else getattr(obj, attr).isoformat() for attr in dir(obj) if not attr.startswith('_') and not callable(getattr(obj, attr))}




# 定义自定义编码器函数
def EncodeCustom(obj):
    if isinstance(obj, (date, datetime)):
        return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj, datetime) else obj.strftime("%Y-%m-%d")
    elif isinstance(obj.__class__, DeclarativeMeta):
        # If obj is an instance of a SQLAlchemy model
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    elif hasattr(obj, "to_dict"):
        return obj.to_dict()
    else:
        raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")
