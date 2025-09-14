from __init__ import InterfaceBase
from __init__ import interface, concrete


@interface
class Human(InterfaceBase):
    def talk(self): ...
    def walk(self): ...


@interface
class MilitaryHuman(Human):
    def shoot(self): ...


# try:
#     @concrete
#     class Soldier(MilitaryHuman):
#         def talk(self): print("talk")
# except TypeError as e:
#     print("Expected error:", e)


# @concrete
# class Commander(MilitaryHuman):
#     def talk(self): print("talk")
#     def walk(self): print("walk")
#     def shoot(self): print("shoot")


# cmd = Commander()
# cmd.shoot()
