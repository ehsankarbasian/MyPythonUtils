
import pathlib
import sys
path = str(pathlib.Path(__file__).parent.parent.parent.absolute())
sys.path.append(path)

from utils.notify_dict.notify_dict import NotifyDict


d = NotifyDict(logfile_name='logfile',
               logger_pid=2,
               enable_default_value=True,
               default_value='__DEFAULT__')
d['a'] = 'A'
d['a'] = 'B'
d['c'] = 'C'
d['c'] = 'D'
p = d['a']
p = d['NNN']
del d['a']
d.write_and_clear_cached_logs()

d['a'] = 'B'
d['E'] = 'F'
d.clear_cached_logs()
print('\nbuiltin functiuons:\n')
p = d.copy()
p = d.keys()
p = d.values()
p = d.items()
p = d.fromkeys('T')
p = d.get('c', 'default')
p = d.pop('c')
p = d.get('c', 'default')
p = d.popitem()
p = d.setdefault('R', '_DEF_')
p = d.get('R')
p = d.get('R', 'diff')
p = d.update(N='NEW')
p = d.get('N')
p = d.clear()
d.write_and_clear_cached_logs()
print(d)
