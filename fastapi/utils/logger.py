import logging
import utils.config as config
from logging.handlers import TimedRotatingFileHandler

def get_logger():
    # 读取配置文件
    c = config.read_config("./config/apiconf.yaml")
    log_level = ""
    if c["log"]["level"] == "debug":
        log_level = logging.DEBUG
    elif c["log"]["level"] == "info":
        log_level = logging.INFO
    elif c["log"]["level"] == "warning":
        log_level = logging.WARNING
    elif c["log"]["level"] == "error":
        log_level = logging.ERROR
    elif c["log"]["level"] == "critical":
        log_level = logging.CRITICAL

    # 创建日志记录器
    logger = logging.getLogger('syslog')
    logger.setLevel(log_level)

    # 创建 TimedRotatingFileHandler
    file_handler = TimedRotatingFileHandler(c["log"]["path"], when='midnight', interval=1, backupCount=c["log"]["max_days"])  # 每天轮转
    file_handler.suffix = "%Y-%m-%d.log"  # 文件名后缀格式为日期
    file_handler.maxBytes = c["log"]["max_size"] * 1024 * 1024  # 设置单个日志文件最大值
    file_handler.setLevel(log_level)

    # 创建输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 添加处理器到记录器
    logger.addHandler(file_handler)

    return logger

logger = get_logger()