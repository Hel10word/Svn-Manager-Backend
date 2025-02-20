import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time


class LogManager:
    _logger_initialized = False

    @staticmethod
    def setup_logging():
        if not LogManager._logger_initialized:
            log_format = "[%(time)s][%(level)s][%(name)s][%(filename)s:%(lineno)d] - %(msg)s"

            # 创建日志目录
            log_directory = "log"
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            # 将日志 记录至文件
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(log_directory, 'info.log'),
                when="midnight",
                backupCount=7  # 可以根据需要调整历史日志保留数
            )
            file_handler.setFormatter(CustomFormatter(fmt=log_format))

            # 设置自定义的 CustomFormatter
            handler = logging.StreamHandler()
            handler.setFormatter(CustomFormatter(fmt=log_format))

            logger = logging.getLogger()
            logger.setLevel(logging.INFO)
            logger.addHandler(handler)

            # 标记为已初始化，防止再次初始化
            LogManager._logger_initialized = True

    @staticmethod
    def get_logger(name: str):
        LogManager.setup_logging()
        return logging.getLogger(name)


class CustomFormatter(logging.Formatter):
    _LEVEL_NAME_FORMAT = {
        'DEBUG': 'DEBUG',
        'INFO': 'INFO ',
        'WARNING': 'WARN ',  # 或者改为 'WARN'，如果你更喜欢全词的缩写
        'ERROR': 'ERROR',
        'CRITICAL': 'CRIT ',
    }
    _TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    _MSEC_FORMAT = '%s.%03d'

    def format(self, record):
        # 格式化 Log Level
        if record.levelname in self._LEVEL_NAME_FORMAT:
            record.level = self._LEVEL_NAME_FORMAT[record.levelname]
        # 格式化 时间
        ct = time.localtime(record.created)
        s = time.strftime(self._TIME_FORMAT, ct)
        s = self._MSEC_FORMAT % (s, record.msecs)
        record.time = s
        return self.formatMessage(record)
