import platform
import os
import json
import requests
import subprocess
import threading
from datetime import datetime
from dateutil import parser
import pytz
import configparser
import shutil

from models.platform import Platform
from dependent.redis import RedisConnection
from utils.logger import logger
from dependent.redis import RedisConnection

# 常量定义
linux_start_command = "ifconfig"
windows_start_command = "ipconfig"
WAF_SERVER = "https://gowaf.bytesycn.com:2087/waf.json"

# 平台检查，获取当前运行的操作系统相关信息
def PlatformCheck():
    p = Platform()
    p.os_info = platform.platform()
    p.os_name = platform.system()
    p.os_version = platform.version()
    p.os_release = platform.release()
    p.architecture = platform.architecture()
    p.network_name = platform.node()
    p.processor = platform.processor()
    return p

# 根据操作系统获取根目录路径
runPlatform = PlatformCheck()
rootPath = runPlatform._linux_root_path if runPlatform.os_name == "Linux" else runPlatform._windows_root_path

# 从远程服务器获取引擎信息
def GetEGInfo():
    resp = requests.get(WAF_SERVER, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0"})
    data = json.loads(resp.text)
    return data

# 心跳检测函数，检查进程是否存活
def WAFEGHeartbeat(type, uuid):
    with RedisConnection(1) as redis:
        hashKey = f"{type.lower()}-{uuid}"
        time_value = redis.hget(hashKey, 'time')
        if time_value:
            stored_time = parser.parse(time_value)
            current_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            time_diff = abs(current_time - stored_time).total_seconds()
            return time_diff <= 1
    return False

# 监控进程状态，记录进程结束日志
def MonitorProcess(process):
    logger.info(f"开始监控进程 PID={process.pid}")
    process.wait()
    exit_code = process.returncode
    logger.info(f"进程 PID={process.pid} 已结束，退出代码 {exit_code}")

# 启动检测引擎
def StartEG(type, uuid):
    path = Path(type, uuid)
    logPath = LogPath(uuid)
    confPath = ConfigPath(type, uuid)
    hashKey = f"Waf{type}Config-{uuid}"

    with RedisConnection(0) as redis:
        if not redis.exists(hashKey) or not os.path.exists(path) or not os.access(path, os.X_OK):
            logger.error(f"无法启动引擎，路径：{path}")
            return None

        command = [str(path), '-l', logPath, '-c', confPath]
        print(command)
        process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        redis.hset(hashKey, "PID", process.pid)
        monitor_thread = threading.Thread(target=MonitorProcess, args=(process,))
        monitor_thread.start()
        return process.pid

# 根据类型和UUID构造路径
def Path(type, uuid):
    savePath = os.path.join(rootPath, uuid, f"{type}.exe" if runPlatform.os_name == "Windows" else type)
    return savePath

# 配置文件路径构造
def ConfigPath(type, uuid):
    savePath = os.path.join(rootPath, uuid, f"waf_{type.lower()}.conf")
    return savePath

def LogPath(uuid):
    return os.path.join(rootPath, uuid, 'log')

# 下载并设置引擎文件
def CreateWAFEGFile(type, uuid):
    savePath = Path(type, uuid)
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    if os.path.exists(savePath):
        os.remove(savePath)
    print(os.getcwd())
    sourcePath = os.path.join(os.getcwd(), 'EG', f'{type}.exe' if runPlatform.os_name == "Windows" else type)
    shutil.copy(sourcePath, savePath)
    os.chmod(savePath, 0o755)

# 检查引擎文件是否存在
def CheckWAFEGFileExist(type, uuid):
    savePath = Path(type, uuid)
    return os.path.exists(savePath)

# 写服务端配置文件
def WriteServerConfig(uuid):
    file = ConfigPath("Server", uuid)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.exists(file):
        os.remove(file)
    try:
        with RedisConnection(0) as r:
            serverConfig = r.hgetall(f"WafServerConfig-{uuid}")
            sysConfig = r.hgetall("SysConfig")            
            config = configparser.ConfigParser()
            if serverConfig:
                config['Server'] = {key: f'"{value}"' for key, value in serverConfig.items()}
            if sysConfig:
                config['Redis'] = {
                    'Host': f'"{sysConfig.get("Redis-Host", "default_host")}"',
                    'Port': f'"{sysConfig.get("Redis-Port", "6379")}"',
                    'Password': f'"{sysConfig.get("Redis-Password", "default_password")}"'
                }
        with open(file, 'w') as configfile:
            config.write(configfile)
        logger.info("服务器配置文件写入成功")
    except Exception as e:
        logger.error(f"写入配置文件失败：{str(e)}")

# 写网关配置文件
def WriteGateConfig(uuid):
    file = ConfigPath("Gate", uuid)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.exists(file):
        os.remove(file)
    try:
        with RedisConnection(0) as r:
            sysConfig = r.hgetall("SysConfig")
            config = configparser.ConfigParser()
            config['Gate'] = {'GateId': f'"{uuid}"'}
        if sysConfig:
                config['Redis'] = {
                    'Host': f'"{sysConfig.get("Redis-Host", "default_host")}"',
                    'Port': f'"{sysConfig.get("Redis-Port", "6379")}"',
                    'Password': f'"{sysConfig.get("Redis-Password", "default_password")}"'
                }
        with open(file, 'w') as configfile:
            config.write(configfile)
        logger.info("网关配置文件写入成功")
    except Exception as e:
        logger.error(f"写入配置文件失败：{str(e)}")


def StartServer():
    serverId = '8000'
    redis_key = f"WafServerConfig-{serverId}"
    # 写入 Redis 哈希表
    data_dict = {'WafServerAddress': '127.0.0.1:8000', 'HttpAPIAddress': '127.0.0.1:8001', 'ServerId': serverId}
    with RedisConnection(0) as redis:
        redis.hset(redis_key, mapping=data_dict)
    CreateWAFEGFile('Server', serverId)
    WriteServerConfig(serverId)
    StartEG('Server', serverId)


def WriteGateConfig(uuid):
    file = ConfigPath("Gate", uuid)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    if os.path.exists(file):
        os.remove(file)
    try:
        with RedisConnection(0) as r:
            sysConfig = r.hgetall("SysConfig")
            config = configparser.ConfigParser()
            config['Gate'] = {'GateId': f'"{uuid}"'}
        if sysConfig:
                config['Redis'] = {
                    'Host': f'"{sysConfig.get("Redis-Host", "default_host")}"',
                    'Port': f'"{sysConfig.get("Redis-Port", "6379")}"',
                    'Password': f'"{sysConfig.get("Redis-Password", "default_password")}"'
                }
        with open(file, 'w') as configfile:
            config.write(configfile)
        logger.info("网关配置文件写入成功")
    except Exception as e:
        logger.error(f"写入配置文件失败：{str(e)}")

def StartGate():
    gateId = '8001'
    if not os.path.exists(r'/usr/local/gowaf/gate.lock'):
        redis_key = f"WafGateConfig-{gateId}"
        domain = input("访问域名，留空使用ip")
        ssl = input('是否启用HTTPS(Y/N)')
        if (ssl.upper() == 'Y'):
            pem = input('证书路径: /usr/local/cert/waf.pem')
            key = input('证书路径: /usr/local/cert/waf.key')
            ssl = 'true'
            domain= domain +":443"
        else:
            pem = key = ''
            ssl = 'false'
            domain= domain +":80"
        upstream = input('上游服务器(http协议):')
        data_dict = {'GateHttpAddress': '0.0.0.0:80', 
                 'StartHttps': ssl, 
                 'GateHttpsAddress': '0.0.0.0:443',
                 'CertFile': pem,
                 'KeyFile': key,
                 'GateAPIAddress': '0.0.0.0:2081',
                 'UpstreamList': upstream,
                 'wafrpc_CheckSwitch': 'true',
                 'Domain': domain,
                 'wafrpc_CheckList_Check': 'true',
                 'wafrpc_Check_Include': '',
                 'wafrpc_ServerAddr_Address': '127.0.0.1:8000',
                 'CertKeyList': '',
                 'Gateld': gateId}
        with RedisConnection(0) as redis:
            redis.hset(redis_key, mapping=data_dict)
        with open(r'/usr/local/gowaf/gate.lock','w') as f:
            f.write('lock')
        f.close()
    CreateWAFEGFile('Gate', gateId)
    WriteGateConfig(gateId)
    StartEG('Gate', gateId)