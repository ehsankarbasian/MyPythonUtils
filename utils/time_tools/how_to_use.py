
import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.append(path)

from time_tools.decorators import print_time, log_time
from time import sleep


@print_time('second', exactness=6)
def the_function_1(t):
    sleep(t)


@log_time('microsecond', exactness=5, logfile_name='the_function2_runtimes')
@print_time('spam', exactness=2)
def the_function_2(t):
    sleep(t)


@log_time('second')
@print_time('millisecond')
@log_time('microsecond', logfile_name='new_log')
@log_time('minute', logfile_name='new_log.log')
@log_time('hour', use_func_name_as_logfile_name=True, exactness=10, logfile_name='spamm')
@log_time('day', logfile_name='day_log')
def the_function_3(t):
    sleep(t)


the_function_1(1.2)
the_function_2(1.5)
the_function_3(0.1)
