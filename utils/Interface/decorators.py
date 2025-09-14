
def interface(cls):
    cls.__interface__ = True
    return cls


def concrete(cls):
    cls.__interface__ = False
    return cls
