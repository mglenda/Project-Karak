import GameLogic.Items as Items
from GameLogic.Placeable import Placeable

PATH = '_Textures\\Minions\\Retextured\\'

class Minion(Placeable):
    _power: int
    _reward: Items.Item
    _agressive: bool

    def __init__(self) -> None:
        pass

    def get_power(self) -> int:
        return self._power
    
    def get_reward(self) -> Items.Item:
        return self._reward
    
    def kill(self) -> Items.Item:
        return self._reward
    
    def is_aggresive(self) -> bool:
        return self._agressive

class Rat(Minion):
    _power: int = 5
    _reward: Items.Item = Items.Dagger()
    _background:str = PATH + 'Rat.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class Dragon(Minion):
    _power: int = 15
    _reward: Items.Item = Items.DragonChest()
    _background:str = PATH + 'Dragon.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class Fiend(Minion):
    _power: int = 12
    _reward: Items.Item = Items.Chest()
    _background:str = PATH + 'Fiend.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class GiantBat(Minion):
    _power: int = 6
    _reward: Items.Item = Items.ThornOfDarkness()
    _background:str = PATH + 'GiantBat.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class GiantSpider(Minion):
    _power: int = 6
    _reward: Items.Item = Items.HealingPortal()
    _background:str = PATH + 'GiantSpider.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class ChestClosed(Minion):
    _power: int = 0
    _reward: Items.Item = Items.Chest()
    _background:str = PATH + 'ChestClosed.png'
    _agressive: bool = False

    def __init__(self) -> None:
        super().__init__()

class Mummy(Minion):
    _power: int = 7
    _reward: Items.Item = Items.MagicBolt()
    _background:str = PATH + 'Mummy.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class SkeletonKeymaster(Minion):
    _power: int = 8
    _reward: Items.Item = Items.Key()
    _background:str = PATH + 'SkeletonKeymaster.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class SkeletonKing(Minion):
    _power: int = 10
    _reward: Items.Item = Items.Axe()
    _background:str = PATH + 'SkeletonKing.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class SkeletonMage(Minion):
    _power: int = 11
    _reward: Items.Item = Items.FrostFist()
    _background:str = PATH + 'SkeletonMage.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()

class SkeletonWarrior(Minion):
    _power: int = 9
    _reward: Items.Item = Items.Sword()
    _background:str = PATH + 'SkeletonWarrior.png'
    _agressive: bool = True

    def __init__(self) -> None:
        super().__init__()