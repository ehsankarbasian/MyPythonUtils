import inspect


def get_caller_file_name(backward_count=1):
    frame = inspect.currentframe()
    for i in range(backward_count):
        frame = frame.f_back
        
    caller_file_name = frame.f_code.co_filename.split('/')[-1]
    return caller_file_name
    
    
def get_caller_function_name(backward_count=1):
    frame = inspect.currentframe()
    for i in range(backward_count):
        frame = frame.f_back
        
    caller_function_name = frame.f_code.co_name
    return caller_function_name
    
    
def get_caller_file_line(backward_count=1):
    frame = inspect.currentframe()
    for i in range(backward_count):
        frame = frame.f_back
        
    caller_file_line = frame.f_lineno
    return caller_file_line
