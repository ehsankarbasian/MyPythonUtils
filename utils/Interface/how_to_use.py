from __init__ import InterfaceBase
from __init__ import interface, concrete


@interface
class Human(InterfaceBase):
    def talk(self): pass
    def walk(self): ...


Human()


@interface
class MilitaryHuman(Human):
    def shoot(self): ...


# MilitaryHuman()


@concrete
class Commander(MilitaryHuman):
    def talk(self): print("talking")
    def walk(self): print("walking")
    def shoot(self): print("shooting")


c = Commander()
c.talk()
