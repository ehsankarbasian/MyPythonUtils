from __init__ import NotThreadSafe


def _make_connection(config):
    print('Connecting ...')
    return f'Connection with config: {config}'


class DatabaseClient(NotThreadSafe.CachedPropertyDependencyMixin):
    
    def __init__(self, config):
        self._config = config
    
    @NotThreadSafe.dependent_cached_property(depends_on=['_config'])
    def connection(self):
        return _make_connection(self._config)


c = DatabaseClient(config={'user': 'user_1', 'pass': 'pass_1'})
print(c.connection)
print(c.connection)
c._config = {'user': 'user_2', 'pass': 'pass_2'}
print('\nconfig changed')
print(c.connection)
print(c.connection)
c.invalidate_cache('connection')
print('\nconfig cache invalidated')
print(c.connection)
print(c.connection)
