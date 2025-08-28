from functools import cached_property


# Dynamic solution: Modify the decorator @cached_property

class __InputTypeException(Exception):
    pass


class _DependentCachedProperty(cached_property):
    def __init__(self, func, depends_on):
        # Validate that depends_on is a list
        if not type(depends_on) is list:
            raise __InputTypeException('depends_on Must be a list')
        self.depends_on = depends_on
        
        super().__init__(func)


def dependent_cached_property(depends_on):
    def wrapper(func):
        return _DependentCachedProperty(func, depends_on)
    return wrapper


class CachedPropertyDependencyMixin:
    
    def __setattr__(self, attr_name, value):
        super().__setattr__(attr_name, value)

        # Invalidate all dependent cached_propertis
        for key, attr_value in type(self).__dict__.items():
            is_dependent_property = isinstance(attr_value, _DependentCachedProperty)
            
            if is_dependent_property:
                is_depended = attr_name in attr_value.depends_on
                
                if is_depended:
                    if key in self.__dict__:
                        self.__dict__.pop(key, None)
    
    
    def invalidate_cache(self, *names):
        # Invalidate cached propeties manually
        for attr_name in names:
            if attr_name not in type(self).__dict__:
                raise Exception(f'AttibuteError: {self.__class__} has no attribute: "{attr_name}"')
            attr_value = type(self).__dict__[attr_name]
            if isinstance(attr_value, _DependentCachedProperty) or isinstance(attr_value, cached_property):
                self.__dict__.pop(attr_name, None)


print("\nWarning: Any class uses the decorator @dependent_cached_property, MUST inherit CachedPropertyDependencyMixin")
print("Make sure to do that, the dependency functionality won't work if you don't.\n")
