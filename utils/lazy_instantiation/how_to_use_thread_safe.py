import math

from __init__ import ThreadSafe


class Circle(ThreadSafe.CachedPropertyDependencyThreadSafeMixin):
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        self._radius = value
    
    @ThreadSafe.dependent_cached_property_thread_safe(depends_on=['radius'])
    @ThreadSafe.thread_safe_inside_method
    def area(self):
        print('Calculating the @cached_property ...')
        return math.pi * self.radius ** 2


c = Circle(radius=5)
print(c.area)
print(c.area)
c.radius = 4
print('\nradious changed')
print(c.area)
print(c.area)
c.invalidate_cache('area')
print('\narea cache invalidated')
print(c.area)
print(c.area)
