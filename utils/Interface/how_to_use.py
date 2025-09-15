from __init__ import InterfaceBase, interface, concrete


@interface
class Human(InterfaceBase):
    def talk(self): pass
    def walk(self): ...


@interface
class MilitaryHuman(Human):
    def shoot(self): ...


@concrete
class Commander(MilitaryHuman):
    def talk(self): print("talking")
    def walk(self): print("walking")
    def shoot(self): print("shooting")


# Human()
# MilitaryHuman()

c = Commander()
c.talk()
