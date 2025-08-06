from utils.time_tools.abstract_time_formatter import AbstractTimeFormatter


TIME_LOGS_FOLDER_NAME = 'time_logs'
DEFAULT_LOGFILE_NAME = 'func_runtimes.log'
DEFAULT_EXACTNESS = 3

class TimeFormatter(AbstractTimeFormatter):
    
    # The default dimention to report duration if dimention not defined
    DEFAULT_DIMENSION = 'millisecond'

    def convert_duration(self, duration, _format):
        """
            duration is a float
            the dimension of duration is (second)
            to define a new custom dimensions for duration, multiply duration with a number as below
        """
        
        if _format == 'second':
            return duration
        elif _format == 'millisecond':
            return duration * 10**3
        elif _format == 'microsecond':
            return duration * 10**6
        elif _format == 'minute':
            return duration / 60
        elif _format == 'hour':
            return duration / 60**2
        # elif _format == 'day':
        #     return duration / (24*60**2)
        else:
            self.set_format(self.DEFAULT_DIMENSION)
            return duration * 10**3
