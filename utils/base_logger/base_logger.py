from inspect import currentframe
import logging

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute())
sys.path.append(path)


class MetaSingletonMonoStateByLogfilePattern(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        log_file = kwargs['log_file']
        cls_key = f'{cls} {log_file}'
        if cls_key not in cls._instance:
            cls._instance[cls_key] = super().__call__(*args, **kwargs)
        return cls._instance[cls_key]


class Logger(metaclass=MetaSingletonMonoStateByLogfilePattern):
    
    def __init__(self, name='default_logger', log_file='sys', project='template', log_type=None, console_logger_enable=False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        """Save on file"""
        handler = logging.FileHandler(f"{log_file}")
        """Logging format"""
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        if console_logger_enable:
            self.logger.addHandler(logging.StreamHandler())

        self.information = {"project": project, "type": log_type}


    def _lin_number(self):
        cf = currentframe()
        return cf.f_back.f_back.f_back.f_lineno


    def _path(self):
        cf = currentframe()
        return cf.f_back.f_back.f_back.f_code.co_filename


    def handle_info(self, info, error=None, pid=None):
        if info:
            info.update(self.information)
        else:
            info = self.information

        if pid:
            info["pid"] = pid

        info["lin_number"] = self._lin_number()
        info["path"] = self._path()
        if error:
            info["lin_error"] = error.__traceback__.tb_lineno
            info["error"] = str(error)

        return info

    def debug(self, msg=None, info=None, error=None, pid=None):
        info = self.handle_info(info=info, error=error, pid=pid)
        self.logger.debug(msg=msg, extra=info, exc_info=False)

    def info(self, msg=None, info=None, error=None, pid=None):
        info = self.handle_info(info=info, error=error, pid=pid)
        self.logger.info(msg=msg, extra=info, exc_info=False)

    def warning(self, msg=None, info=None, error=None, pid=None):
        info = self.handle_info(info=info, error=error, pid=pid)
        self.logger.warning(msg=msg, extra=info, exc_info=False)

    def error(self, msg=None, info=None, error=None, pid=None):
        info = self.handle_info(info=info, error=error, pid=pid)
        self.logger.error(msg=msg, extra=info, exc_info=False)

    def critical(self, msg=None, info=None, error=None, pid=None):
        info = self.handle_info(info=info, error=error, pid=pid)
        self.logger.critical(msg=msg, extra=info, exc_info=False)


# App Logger
# logger = Logger(
#     name="user_bot",
#     log_file="sys",
#     project="bale_bot",
#     log_type="app_log",
# )
