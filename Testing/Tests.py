class test():
    def __init__(self) -> None:
        self.x = 0

class t(test):
    def __init__(self) -> None:
        super().__init__()

class x(test):
    def __init__(self) -> None:
        super().__init__()

l = [x,x(),t(),x(),t(),x(),test()]

weapons = {}
for w in l:
    if w.__class__ not in weapons.keys():
        weapons[w.__class__] = 1
    else:
        weapons[w.__class__] += 1

print (1 % -1)