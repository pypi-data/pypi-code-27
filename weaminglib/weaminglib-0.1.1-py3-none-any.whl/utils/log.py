import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
from .decorator import run_once


@run_once
def setup_logger(app_name,
                 enable_console=True,
                 enable_file=True,
                 timed_file_when='S',
                 log_dir='./log/',
                 app_level=logging.DEBUG,
                 root_level=logging.INFO):
    """
    :param app_name: any string you like
    :param enable_file: global flag to enable log file
    :param timed_file_when: if true, use timed log file handler, else use single file. allow S, M, H, D, W0-W6, midnight
    :param enable_console: enable app logger console handler
    :param app_level: control which log with level will be handle by logger with app name
    :param root_level: control which log with level will be save to log file
    """
    if not os.path.exists("log"):
        os.makedirs("log")

    recfmt = '(%(threadName)s) %(asctime)s.%(msecs)03d %(levelname)s %(name)s %(filename)s:%(lineno)d %(funcName)s > %(message)s'
    datefmt = '%Y-%m-%d %X'
    formatter = logging.Formatter(recfmt, datefmt=datefmt)

    # add handler for root logger
    if enable_file:
        if timed_file_when:
            root_logger = logging.getLogger()

            file_name = time.strftime("{}.log".format(app_name))
            file_path = os.path.join(log_dir, file_name)
            timed_file_handler = TimedRotatingFileHandler(
                file_path,
                when=timed_file_when,
                backupCount=30,
                encoding='utf-8')
            timed_file_handler.setFormatter(formatter)
            timed_file_handler.setLevel(root_level)

            root_logger.addHandler(timed_file_handler)
        else:
            file_name = time.strftime("{}.%y%m%d.log".format(app_name))
            file_path = os.path.join(log_dir, file_name)
            logging.basicConfig(
                filename=file_path,
                level=root_level,
                format=recfmt,
                datefmt=timefmt)

    if enable_console:
        app_logger = logging.getLogger(app_name)
        app_logger.setLevel(level=app_level)

        console = logging.StreamHandler()
        console.setFormatter(formatter)

        app_logger.addHandler(console)
