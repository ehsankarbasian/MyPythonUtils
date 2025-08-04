from decorators import protected, private


@private
def print_running(name):
    print(f'is running: {name}')


class A:
    
    def public(self):
        print_running('A.public')
        self.protected(src='A.public')      # Runs without warning and error    (Because is called in the owner class)
        self.__private(src='A.public')      # Runs without warning and error    (Because is called in the owner class)
    
    @protected
    def protected(self, src=None):
        if src:
            print_running(f'A.protected from {src}')
        else:
            print_running('A.protected')
        self.__private(src='A.protected')   # Runs without warning and error    (Because is called in the owner class)
    
    @private
    def __private(self, src=None):
        print_running(f'A.private from {src}')


if __name__ == '__main__':
    print_running('how_to_use.py') # Runs without warning and error            (Because is called in the owner file)
    
    a = A()
    a.public()                  # Runs without warning and error               (Because has no access modifier, it's public)
    a.protected()               # Runs with printing protected warning
    a._A__private()             # Raises _PrivateFunctionCalledException
