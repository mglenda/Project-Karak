from GameEngine.PlaceableDefinition import PlaceableDefinition

PATH = '_Textures\\Minions\\Retextured\\'

class MinionDefinition(PlaceableDefinition):
    power: int
    agressive: bool

class Rat(MinionDefinition):
    power: int = 5
    path: str = PATH + 'Rat.png'
    agressive: bool = True

class Dragon(MinionDefinition):
    power: int = 15
    path:str = PATH + 'Dragon.png'
    agressive: bool = True

class Fiend(MinionDefinition):
    power: int = 12
    path:str = PATH + 'Fiend.png'
    agressive: bool = True

class GiantBat(MinionDefinition):
    power: int = 6
    path:str = PATH + 'GiantBat.png'
    agressive: bool = True

class GiantSpider(MinionDefinition):
    power: int = 6
    path:str = PATH + 'GiantSpider.png'
    agressive: bool = True

class ChestClosed(MinionDefinition):
    power: int = 0
    path:str = PATH + 'ChestClosed.png'
    agressive: bool = False

class Mummy(MinionDefinition):
    power: int = 7
    path:str = PATH + 'Mummy.png'
    agressive: bool = True

class SkeletonKeymaster(MinionDefinition):
    power: int = 8
    path:str = PATH + 'SkeletonKeymaster.png'
    agressive: bool = True

class SkeletonKing(MinionDefinition):
    power: int = 10
    path:str = PATH + 'SkeletonKing.png'
    agressive: bool = True

class SkeletonMage(MinionDefinition):
    power: int = 11
    path:str = PATH + 'SkeletonMage.png'
    agressive: bool = True

class SkeletonWarrior(MinionDefinition):
    power: int = 9
    path:str = PATH + 'SkeletonWarrior.png'
    agressive: bool = True