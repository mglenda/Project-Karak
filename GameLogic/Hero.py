from GameLogic.Inventory import Inventory
import GameLogic.Ability as Ability
import GameLogic.Items as Items
from GameLogic.Minion import ChestClosed
from GUI.GraphicComponents import TileInterface
from GameLogic.Combatiant import Combatiant
from Game import GAME

MAX_HP = 5
DEF_MOVE_POINTS = 4
PATH = '_Textures\\Heroes\\Retextured\\'
ICON_PATH = '_Textures\\Heroes\\MyIcons\\'

class Hero(Combatiant):
    _inventory: Inventory
    _abilities: list[Ability.Ability]
    _cursed: bool
    _hit_points: int
    _alive: bool
    _move_points: int
    _background: str
    _icon: str
    _tile: TileInterface
    _previous_tile: TileInterface

    def __init__(self,player) -> None:
        self._inventory = Inventory(self)
        self._cursed = False
        self._hit_points = MAX_HP
        self._alive = True
        self._move_points = DEF_MOVE_POINTS
        self._tile = None
        self._previous_tile = None
        self.reload_abilities()
        self._player = player

    def get_player(self):
        return self._player

    def get_abilities(self) -> list[Ability.Ability]:
        abilities = []

        if not self.is_cursed():
            for a in self._abilities:
                abilities.append(a)
        
        for i in self._inventory.get_weapons():
            if i is not None:
                if i.get_ability() != None:
                    abilities.append(i.get_ability())

        for i in self._inventory.get_keys():
            if i is not None:
                if i.get_ability() != None:
                    abilities.append(i.get_ability())
        
        for i in self._inventory.get_scrolls():
            if i is not None:
                if i.get_ability() != None:
                    abilities.append(i.get_ability())

        return abilities
    
    def refresh_abilities(self):
        for a in self._abilities:
                a.set_active(True)
        
        for i in self._inventory.get_weapons():
            if i is not None:
                if i.get_ability() != None:
                    i.get_ability().set_active(True)

        for i in self._inventory.get_keys():
            if i is not None:
                if i.get_ability() != None:
                    i.get_ability().set_active(True)
        
        for i in self._inventory.get_scrolls():
            if i is not None:
                if i.get_ability() != None:
                    i.get_ability().set_active(True)

    def get_icon(self) -> str:
        return self._icon

    def get_power(self) -> int:
        power = 0
        for w in self.get_weapons():
            if w is not None:
                power += w.get_damage_base()
        return power   

    def pick_item_from_tile(self):
        key = self.get_keys()[0]
        if isinstance(self.get_tile().get_placeable(),ChestClosed) and key is not None:
            if self.add_item(Items.Chest()):
                self.remove_item(key)
                self.get_tile().remove_placeable()
                GAME.get_castle().player_turn_end()
        elif isinstance(self.get_tile().get_placeable(),Items.Item):
            if self.add_item(self.get_tile().get_placeable()):
                self.get_tile().remove_placeable()
                GAME.get_castle().player_turn_end()
            else:
                GAME.get_reward_screen().load(self)

    def get_weapons(self) -> list[Items.Item]:
        return self._inventory.get_weapons()
    
    def get_scrolls(self) -> list[Items.Item]:
        return self._inventory.get_scrolls()
    
    def get_keys(self) -> list[Items.Item]:
        return self._inventory.get_keys()
    
    def get_chests(self) -> list[Items.Item]:
        return self._inventory.get_chests()
    
    def get_items(self) -> list[Items.Item]:
        return self._inventory.get_items()
    
    def has_item(self, item_class: Items.Item) -> bool:
        for i in self._inventory.get_items():
            if isinstance(i,item_class):
                return True
        return False
    
    def move(self,tile: TileInterface):
        self._move_points -= 1
        self.set_tile(tile)

    def set_tile(self, tile: TileInterface):
        if self._tile is not None:
            self._tile.remove_hero(self)
            self._previous_tile = self._tile
        self._tile = tile
        tile.add_hero(self)

    def get_tile(self) -> TileInterface:
        return self._tile
    
    def get_previous_tile(self) -> TileInterface:
        return self._previous_tile

    def reload_abilities(self):
        self._abilities = []
        self._abilities.append(Ability.RollDice(self))
        for a in self.__class__._abilities:
            self._abilities.append(a(self))

    def add_ability(self,ability:Ability.Ability):
        if ability not in self._abilities:
            self._abilities.append(ability)

    def remove_ability(self,ability:Ability.Ability):
        a: Ability.Ability
        for a in reversed(self._abilities):
            if isinstance(a,ability):
                self._abilities.remove(a)

    def has_ability(self,ability:Ability.Ability) -> bool:
        if not self.is_cursed():
            for a in self._abilities:
                if isinstance(a,ability):
                    return True
        
        for i in self._inventory.get_keys():
            if i is not None:
                if isinstance(i.get_ability(),ability):
                    return True
        
        for i in self._inventory.get_weapons():
            if i is not None:
                if isinstance(i.get_ability(),ability):
                    return True
            
        for i in self._inventory.get_scrolls():
            if i is not None:
                if isinstance(i.get_ability(),ability):
                    return True
            
        return False
            
    def add_item(self,item:Items.Item) -> bool:
        return self._inventory.add(item)
    
    def remove_item(self, item:Items.Item):
        self._inventory.remove(item)

    def is_cursed(self) -> bool:
        return self._cursed
    
    def is_alive(self) -> bool:
        return self._alive
    
    def heal(self,amnt:int):
        if self._hit_points + amnt > MAX_HP:
            self._hit_points = MAX_HP
        else:
            self._hit_points += amnt

    def hurt(self):
        if self._hit_points == 1:
            self._hit_points = 0
            self.kill()
        else:
            self._hit_points -= 1

    def get_hit_points(self) -> int:
        return self._hit_points

    def kill(self):
        self._alive = False

    def ressurect(self,amnt:int):
        if amnt > 0:
            self._alive = True    
            self._hit_points = amnt

    def get_move_points(self) -> int:
        return self._move_points
    
    def refresh_move_points(self):
        self._move_points = DEF_MOVE_POINTS

    def set_move_points(self, points: int):
        self._move_points = points

class Wizard(Hero):
    _background = PATH + 'Wizard.png'
    _icon = ICON_PATH + 'Wizard.png'
    _abilities = [Ability.AstralWalking
                  ,Ability.MagicalAffinity]
    def __init__(self,player) -> None:
        super().__init__(player)

class Warrior(Hero):
    _background = PATH + 'Warrior.png'
    _icon = ICON_PATH + 'Warrior.png'
    _abilities = [Ability.Reincarnation
                  ,Ability.DoubleAttack]
    def __init__(self,player) -> None:
        super().__init__(player)

class Warlock(Hero):
    _background = PATH + 'Warlock.png'
    _icon = ICON_PATH + 'Warlock.png'
    _abilities = [Ability.Sacrifice
                  ,Ability.MagicSwap]
    def __init__(self,player) -> None:
        super().__init__(player)

class Thief(Hero):
    _background = PATH + 'Thief.png'
    _icon = ICON_PATH + 'Thief.png'
    _abilities = [Ability.Backstab
                  ,Ability.Stealth]
    def __init__(self,player) -> None:
        super().__init__(player)
        
class Swordsman(Hero):
    _background = PATH + 'Swordsman.png'
    _icon = ICON_PATH + 'Swordsman.png'
    _abilities = [Ability.Unstoppable
                  ,Ability.CombatTraining]
    def __init__(self,player) -> None:
        super().__init__(player)

class Ranger(Hero):
    _background = PATH + 'Ranger.png'
    _icon = ICON_PATH + 'Ranger.png'
    _abilities = [Ability.Eavesdropping
                  ,Ability.BearAttack]
    def __init__(self,player) -> None:
        super().__init__(player)

class Oracle(Hero):
    _background = PATH + 'Oracle.png'
    _icon = ICON_PATH + 'Oracle.png'
    _abilities = [Ability.Fateweaver
                  ,Ability.Foresight]
    def __init__(self,player) -> None:
        super().__init__(player)

class LordOfKarak(Hero):
    _background = PATH + 'LordOfKarak.png'
    _icon = ICON_PATH + 'LordOfKarak.png'
    _abilities = []
    def __init__(self,player) -> None:
        super().__init__(player)

class BattleMage(Hero):
    _background = PATH + 'BattleMage.png'
    _icon = ICON_PATH + 'BattleMage.png'
    _abilities = [Ability.SwordMaster
                  ,Ability.BlitzAttack]
    def __init__(self,player) -> None:
        super().__init__(player)

class Barbarian(Hero):
    _background = PATH + 'Barbarian.png'
    _icon = ICON_PATH + 'Barbarian.png'
    _abilities = [Ability.Berserk
                  ,Ability.Perseverance]
    def __init__(self,player) -> None:
        super().__init__(player)

class Acrobat(Hero):
    _background = PATH + 'Acrobat.png'
    _icon = ICON_PATH + 'Acrobat.png'
    _abilities = [Ability.ThrowingDaggers
                  ,Ability.Sprint]
    def __init__(self,player) -> None:
        super().__init__(player)

class WarriorPrincess(Hero):
    _background = PATH + 'WarriorPrincess.png'
    _icon = ICON_PATH + 'WarriorPrincess.png'
    _abilities = [Ability.DualWielding
                  ,Ability.TacticalReposition]
    def __init__(self,player) -> None:
        super().__init__(player)

class BeastHunter(Hero):
    _background = PATH + 'BeastHunter.png'
    _icon = ICON_PATH + 'BeastHunter.png'
    _abilities = [Ability.Protector
                  ,Ability.Ambush]
    def __init__(self,player) -> None:
        super().__init__(player)

class Alchemist(Hero):
    _background = PATH + 'Alchemist.png'
    _icon = ICON_PATH + 'Alchemist.png'
    _abilities = [Ability.Stoneskin
                  ,Ability.Transformation]
    def __init__(self,player) -> None:
        super().__init__(player)