
import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.notify_dict.notify_dict import NotifyDict


d = NotifyDict('logfile', 2, enable_default_value=True, default_value='__DEFAULT__')
d['a'] = 'A'
d['a'] = 'B'
d['c'] = 'C'
d['c'] = 'D'
p = d['a']
p = d['NNN']
del d['a']
d.write_all_cached_logs()
