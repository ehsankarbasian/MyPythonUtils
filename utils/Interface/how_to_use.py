from __init__ import InterfaceBase


class MyInterface(InterfaceBase):
    
    def foo(self):
        pass

    @property
    def bar(self):
        pass

    @staticmethod
    def s():
        ...

    @classmethod
    def c(cls):
        pass


class MyConcrete(MyInterface):
    
    def foo(self):
        print('foo')
    
    @property
    def bar(self):
        print('bar')
        return 'bar'
    
    @staticmethod
    def s():
        print('s')

    @classmethod
    def c(cls):
        print('c')


MyConcrete()


try:
    class BadInterface1(InterfaceBase):
        def foo(self):
            print("not allowed")
except TypeError as e:
    print("BadInterface1:", e)

try:
    class BadInterface2(InterfaceBase):
        some_value = 123
except TypeError as e:
    print("BadInterface2:", e)

try:
    class BadInterface3(InterfaceBase):
        @property
        def baz(self):
            return 42
except TypeError as e:
    print("BadInterface3:", e)
