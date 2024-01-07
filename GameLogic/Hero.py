from GameLogic.Inventory import Inventory
import GameLogic.Ability as Ability
import GameLogic.Items as Items
from GUI.GraphicComponents import TileInterface

MAX_HP = 5
DEF_MOVE_POINTS = 4
PATH = '_Textures\\Heroes\\Retextured\\'

class Hero():
    _inventory: Inventory
    _abilities: list
    _cursed: bool
    _hit_points: int
    _alive: bool
    _move_points: int
    _chests: float
    _background: str
    _tile: TileInterface

    def __init__(self) -> None:
        self._inventory = Inventory()
        self._cursed = False
        self._hit_points = MAX_HP
        self._alive = True
        self._chests = 0
        self._move_points = DEF_MOVE_POINTS
        self.reload_abilities()

    def set_tile(self, tile: TileInterface):
        self._tile = tile

    def get_tile(self) -> TileInterface:
        return self._tile

    def reload_abilities(self):
        self._abilities = []
        a:Ability.Ability
        for a in self.__class__._abilities:
            self._abilities.append(a())

    def add_ability(self,ability:Ability.Ability):
        if ability not in self._abilities:
            self._abilities.append(ability)

    def remove_ability(self,ability:Ability.Ability):
        a: Ability.Ability
        for a in reversed(self._abilities):
            if isinstance(a,ability):
                self._abilities.remove(a)

    def has_ability(self,ability:Ability.Ability):
        if not self._cursed:
            for a in self._abilities:
                if type(a) == ability:
                    return True
        i:Items.Item
        for i in self._inventory.get_items():
            if type(i.get_ability()) == ability:
                return True            
        return False

    def add_item(self,item:Items.Item) -> bool:
        if item.get_type() == Items.TYPE_CHEST:
            self._chests += item.get_bonus()
            return True
        return self._inventory.add(item)
    
    def get_item(self,item_type:Items.Item):
        return self._inventory.get(item_type=item_type)
    
    def remove_item(self,item:Items.Item):
        self._inventory.remove(item)

    def is_cursed(self) -> bool:
        return self._cursed
    
    def get_abilities(self) -> list:
        return self._abilities
    
    def is_alive(self) -> bool:
        return self._alive
    
    def heal(self,amnt:int):
        if self._hit_points + amnt > MAX_HP:
            self._hit_points = MAX_HP
        else:
            self._hit_points += amnt

    def hurt(self):
        self._hit_points -= 1

    def kill(self):
        self._alive = False

    def ressurect(self,amnt:int):
        self._hit_points = amnt

    def move(self):
        self._move_points -= 1

    def get_move_points(self) -> int:
        return self._move_points

class Wizard(Hero):
    _background = PATH + 'Wizard.png'
    _abilities = [Ability.AstralWalking
                  ,Ability.MagicalAffinity]
    def __init__(self) -> None:
        super().__init__()

class Warrior(Hero):
    _background = PATH + 'Warrior.png'
    _abilities = [Ability.Reincarnation
                  ,Ability.DoubleAttack]
    def __init__(self) -> None:
        super().__init__()

class Warlock(Hero):
    _background = PATH + 'Warlock.png'
    _abilities = [Ability.Sacrifice
                  ,Ability.MagicSwap]
    def __init__(self) -> None:
        super().__init__()

class Thief(Hero):
    _background = PATH + 'Thief.png'
    _abilities = [Ability.Backstab
                  ,Ability.Stealth]
    def __init__(self) -> None:
        super().__init__()
        
class Swordsman(Hero):
    _background = PATH + 'Swordsman.png'
    _abilities = [Ability.Unstoppable
                  ,Ability.CombatTraining]
    def __init__(self) -> None:
        super().__init__()

class Ranger(Hero):
    _background = PATH + 'Ranger.png'
    _abilities = [Ability.Eavesdropping
                  ,Ability.BearAttack]
    def __init__(self) -> None:
        super().__init__()

class Oracle(Hero):
    _background = PATH + 'Oracle.png'
    _abilities = [Ability.Fateweaver
                  ,Ability.Foresight]
    def __init__(self) -> None:
        super().__init__()

class LordOfKarak(Hero):
    _background = PATH + 'LordOfKarak.png'
    _abilities = []
    def __init__(self) -> None:
        super().__init__()

class BattleMage(Hero):
    _background = PATH + 'BattleMage.png'
    _abilities = [Ability.SwordMaster
                  ,Ability.BlitzAttack]
    def __init__(self) -> None:
        super().__init__()

class Barbarian(Hero):
    _background = PATH + 'Barbarian.png'
    _abilities = [Ability.Berserk
                  ,Ability.Perseverance]
    def __init__(self) -> None:
        super().__init__()

class Acrobat(Hero):
    _background = PATH + 'Acrobat.png'
    _abilities = [Ability.ThrowingDaggers
                  ,Ability.Sprint]
    def __init__(self) -> None:
        super().__init__()