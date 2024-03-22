import GameLogic.Ability as Ability
from GameLogic.Placeable import Placeable
from Game import GAME

PATH = '_Textures\\Items\\Retextured\\'

TYPE_KEY = 0
TYPE_WEAPON = 1
TYPE_SCROLL = 2
TYPE_CHEST = 4

class Item(Placeable):
    _ability: Ability.Ability
    _type: int
    _damage_base: int
    _background: str
    _stacks: int

    def __init__(self) -> None:
        self._hero = None
        if self.__class__._ability is not None:
            self._ability = self.__class__._ability(self)
            self._stacks = 1

    def get_type(self) -> int:
        return self._type
    
    def get_ability(self) -> Ability.Ability:
        return self._ability
    
    def get_damage_base(self) -> int:
        return self._damage_base
    
    def get_icon(self) -> str:
        return self._background
    
    def get_stacks(self) -> int:
        return self._stacks
    
    def get_power_wheel_value(self) -> str:
        if self._type == TYPE_WEAPON:
            return str(self.get_damage_base())
        elif self._type in (TYPE_SCROLL,TYPE_KEY):
            if self.get_stacks() > 1:
                return str(self.get_stacks())
            else:
                return None
        return None
    
    def set_stacks(self, stacks: int):
        self._stacks = stacks
        if stacks <= 0 and self._hero is not None:
            self._hero.remove_item(self)
            GAME.get_castle().refresh_player_panels()

    def set_hero(self, hero):
        self._hero = hero

    def get_hero(self):
        return self._hero


class Dagger(Item):
    _type: int = TYPE_WEAPON
    _damage_base: int = 1
    _ability: Ability.Ability = None
    _background: str = PATH + 'Daggers.png'

    def __init__(self) -> None:
        super().__init__()

class Sword(Item):
    _type: int = TYPE_WEAPON
    _damage_base: int = 2
    _ability: Ability.Ability = None
    _background: str = PATH + 'Sword.png'

    def __init__(self) -> None:
        super().__init__()

class Axe(Item):
    _type: int = TYPE_WEAPON
    _damage_base: int = 3
    _ability: Ability.Ability = None
    _background: str = PATH + 'Axe.png'

    def __init__(self) -> None:
        super().__init__()

class Key(Item):
    _ability: Ability.Ability = Ability.UnlockChest
    _type:int = TYPE_KEY
    _background: str = PATH + 'Key.png'

    def __init__(self) -> None:
        super().__init__()

class Chest(Item):
    _type:int = TYPE_CHEST
    _ability: Ability.Ability = None
    _background: str = PATH + 'ChestOpened.png'

    def __init__(self) -> None:
        super().__init__()

class DragonChest(Item):
    _type:int = TYPE_CHEST
    _ability: Ability.Ability = None
    _background: str = PATH + 'ChestDragon.png'

    def __init__(self) -> None:
        super().__init__()  

class MagicBolt(Item):
    _ability: Ability.Ability = Ability.MagicBolt
    _type:int = TYPE_SCROLL
    _background: str = PATH + 'MagicBolt.png'

    def __init__(self) -> None:
        super().__init__()

class ThornOfDarkness(Item):
    _ability: Ability.Ability = Ability.ThornOfDarkness
    _type:int = TYPE_SCROLL
    _background: str = PATH + 'ThornOfDarkness.png'

    def __init__(self) -> None:
        super().__init__()

class HealingPortal(Item):
    _ability: Ability.Ability = Ability.HealingPortal
    _type:int = TYPE_SCROLL
    _background: str = PATH + 'HealingPortal.png'

    def __init__(self) -> None:
        super().__init__()

class FrostFist(Item):
    _ability: Ability.Ability = Ability.FrostFist
    _type:int = TYPE_SCROLL
    _background: str = PATH + 'FrostFist.png'

    def __init__(self) -> None:
        super().__init__()