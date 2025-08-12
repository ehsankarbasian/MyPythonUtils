import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.log_cacher.simple_cacher import SimpleLogCacher


cacher = SimpleLogCacher(prefix='my_test_')
cacher.cache_log('line_1')
cacher.cache_log('line_2')
cacher.cache_log('line_3')
cacher.show_all_cached_logs()
cacher.cache_log('line_4')
cacher.cache_log('line_5')
cacher.clear_cache()
cacher.cache_log('line_6')
cacher.cache_log('line_7')
cacher.show_all_cached_logs()
