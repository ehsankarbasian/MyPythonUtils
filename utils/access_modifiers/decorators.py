import sys, functools


class _PrivateFunctionCalledException(Exception):
    def __init__(self, error_message):
        super().__init__(error_message)


def __get_is_access_limit_met(func, args, caller_name, func_name, caller_file):
    #TODO: Make sure has not bugs, (write test if necessary)
    
    is_file_method = type(args[0]).__name__ == 'str'
    owner_file_name = func.__module__
    called_in_the_same_file = owner_file_name == '__main__' or caller_file in ['__main__', owner_file_name]
    
    called_by_owner_file = is_file_method and called_in_the_same_file
    called_by_owner_class = caller_name in dir(args[0])
    called_by_owner = called_by_owner_file or called_by_owner_class
    
    recursive_call = caller_name is func_name
    
    is_private_limit_met = called_by_owner or recursive_call
    return is_private_limit_met


def private(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        caller_name = sys._getframe(1).f_code.co_name
        caller_file = sys._getframe(1).f_code.co_filename.split('/')[-1].split('.')[0]
        
        is_private_limit_met = __get_is_access_limit_met(func, args, caller_name, func_name, caller_file)
        if not is_private_limit_met:
            error_message = f'private function {func_name} called by {caller_name}'
            raise _PrivateFunctionCalledException(error_message)
        
        return func(*args, **kwargs)
    return wrapper


def protected(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        caller_name = sys._getframe(1).f_code.co_name
        caller_file = sys._getframe(1).f_code.co_filename.split('/')[-1].split('.')[0]
        
        is_protected_limit_met = __get_is_access_limit_met(func, args, caller_name, func_name, caller_file)
        if not is_protected_limit_met:
            warning_message = f'protected function {func_name} called by {caller_name}'
            print(f'ProtectedMessageCalledWarning: {warning_message}')
        
        return func(*args, **kwargs)
    return wrapper
