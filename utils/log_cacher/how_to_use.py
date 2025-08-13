import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.test_tools.mocked_redis.mocked_redis import get_fake_client

from utils.log_cacher.simple_cacher import SimpleLogCacher
from utils.log_cacher.redis_cacher import RedisLogCacher


cacher = SimpleLogCacher(prefix='SimpleLogCacher test')
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


redis_client = get_fake_client()
cacher = RedisLogCacher(redis_client=redis_client,
                        cache_list_name='cached_logs', 
                        prefix='RedisLogCacher test')
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
