from datetime import timedelta

import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.parent.absolute())
sys.path.append(path)

from utils.extended_logger import AbstractExtendedLogger
from utils.backward_inspector import BackwardInspector


NOTIFY_DICT_PERIOD_SECONDS = 2
NOTIFY_DICT_PERIOD_DAYS = 3


class NotifyDictCacheLogger(AbstractExtendedLogger):
    
    def get_logger_time_period(self):
        return timedelta(seconds=NOTIFY_DICT_PERIOD_SECONDS, days=NOTIFY_DICT_PERIOD_DAYS)
    
    def format_log_text(self, text, **kwargs):
        pid = self.pid
        formatted_text = f'pid: {pid}, {text}'
        
        return formatted_text
    
    def format_code_address(self):
        backward_depth = 4
        caller_file_line = BackwardInspector.get_caller_file_line(backward_depth)
        caller_file_name = BackwardInspector.get_caller_file_name(backward_depth)
        
        code_address = f'line:{caller_file_line}, file:{caller_file_name}'
        return code_address
    
    def format_final_log(self, code_address, log_text):
        final_log = f'[{code_address}] | {log_text}'
        return final_log


def setup_logger(logfile_name, pid):
    if not logfile_name[-4:] == '.log':
        logfile_name = f'{logfile_name}.log'
    
    logger = NotifyDictCacheLogger(log_file=f'logs/{logfile_name}', periodic_folder_base_name='NotifyDict', pid_required=True)
    logger.set_pid(pid)
    return logger
