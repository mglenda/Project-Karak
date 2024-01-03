import Ability

TYPE_KEY = 0
TYPE_WEAPON = 1
TYPE_SCROLL = 2
TYPE_CHEST = 4

class Item():
    _ability: Ability.Ability = None
    _type: int
    _bonus: float = None

    def __init__(self) -> None:
        pass

    def get_type(self) -> int:
        return self._type
    
    def get_ability(self) -> Ability.Ability:
        return self._ability
    
    def get_bonus(self) -> float:
        return self._bonus

class Dagger(Item):
    _type: int = TYPE_WEAPON
    _bonus: float = 1.0

    def __init__(self) -> None:
        super().__init__()

class Key(Item):
    _ability: Ability.Ability = Ability.UnlockChest()
    _type:int = TYPE_KEY

    def __init__(self) -> None:
        super().__init__()

class Chest(Item):
    _type:int = TYPE_CHEST
    _bonus:float = 1.0

    def __init__(self) -> None:
        super().__init__()

class DragonChest(Item):
    _type:int = TYPE_CHEST
    _bonus:float = 1.5

    def __init__(self) -> None:
        super().__init__()  