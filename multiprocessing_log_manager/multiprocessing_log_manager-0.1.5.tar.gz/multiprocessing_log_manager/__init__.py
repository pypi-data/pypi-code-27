#coding=utf8

# name = 'multiprocessing_log_manager'
__all__ = ['LogManager','simple_root_logger']
from .log_manager import LogManager
simple_root_logger = LogManager().get_logger_and_add_handlers()