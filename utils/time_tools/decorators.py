from functools import wraps
import time
import os

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.time_tools.setup import TimeFormatter, DEFAULT_LOGFILE_NAME, DEFAULT_EXACTNESS, TIME_LOGS_FOLDER_NAME
from utils.base_logger import Logger

# No need to modify this file


__formatter = TimeFormatter()


def __get_logger(logfile_name):
    try:
        os.mkdir(f'logs/{TIME_LOGS_FOLDER_NAME}')
    except:
        pass
    
    if '.log' not in logfile_name:
        logfile_name += '.log'
    
    logger = Logger.setup_logger(
        name = logfile_name,
        log_file = f'logs/{TIME_LOGS_FOLDER_NAME}/{logfile_name}',
        project = "template_tools",
        log_type = "app_log",
    )
    
    return logger


def print_time(duration_format=None, exactness=DEFAULT_EXACTNESS, enable=True):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enable:
                tic = time.time()
                func_result = func(*args, **kwargs)
                toc = time.time()
                duration = toc - tic
                
                function_name = func.__name__
                __formatter.set_format(duration_format)
                formatted_duration = __formatter.format_duration(duration, duration_format, exactness)
                duration_report = f'{function_name}: {formatted_duration} ({__formatter.format})'
                print(duration_report)
            
            return func_result
        return wrapper
    return decorate


def log_time(duration_format=None, exactness=DEFAULT_EXACTNESS, logfile_name=DEFAULT_LOGFILE_NAME, use_func_name_as_logfile_name=False, enable=True):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enable:
                tic = time.time()
                func_result = func(*args, **kwargs)
                toc = time.time()
                duration = toc - tic
                
                function_name = func.__name__
                __formatter.set_format(duration_format)
                formatted_duration = __formatter.format_duration(duration, duration_format, exactness)
                duration_report = f'{function_name}: {formatted_duration} ({__formatter.format})'
                
                logger_name = logfile_name
                if use_func_name_as_logfile_name:
                    logger_name = function_name
                __get_logger(logger_name).debug(duration_report)
            
            return func_result
        return wrapper
    return decorate
