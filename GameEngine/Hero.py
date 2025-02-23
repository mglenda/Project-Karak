from GameEngine.HeroDefinition import HeroDefinition
from Interfaces.HeroInterface import HeroInterface
from Interfaces.TileObjectInterface import TileObjectInterface
from Interfaces.MinionInterface import MinionInterface
from GameEngine.Inventory import Inventory
from GameEngine.Constants import Constants
from GameEngine.Action import Action,ActionCombat,EndTurn,RollDice,Revitalize,HealingFountain
from GameEngine.Buff import Buff,Unconsciousness,Curse
from GameEngine.BuffModifier import BuffModifier,CanWalkThroughWalls
import GameEngine.DiceDefinition as diceType
from typing import Type,overload

class Hero(HeroInterface):
    definition: HeroDefinition
    name: str
    tile: TileObjectInterface
    former_tile: TileObjectInterface
    hit_points: int
    max_hit_points: int
    move_points: int
    max_move_points: int
    actions: list[Action]
    active_buffs: list[Buff]
    dices: list[diceType.DiceDefinition]

    inventory: Inventory

    def __init__(self, definition: HeroDefinition, name: str) -> None:
        super().__init__(definition,name)
        self.definition = definition
        self.name = name
        self.tile = None
        self.former_tile = None
        self.max_hit_points = getattr(self.definition,'max_hit_points',Constants.HERO_MAX_HP)
        self.max_move_points = getattr(self.definition,'max_move_points',Constants.HERO_MOVEPOINTS)
        self.hit_points = self.max_hit_points
        self.move_points = self.max_move_points
        self.inventory = Inventory(self)
        self.power = 0
        self.dices = [diceType.Normal,diceType.Normal]

        self.actions = [EndTurn(self),ActionCombat(self),RollDice(self),Revitalize(self),HealingFountain(self)]
        self.active_buffs = []

        a_type: Type[Action] = None
        for a_type in self.definition.default_actions:
            self.actions.append(a_type(self))

        self.actions.sort(key=lambda x: x.prio)

    def set_move_points(self,points: int):
        self.move_points = points

    def add_move_points(self,points: int):
        self.move_points += points

    def get_move_points(self) -> int:
        return self.move_points
    
    def get_max_move_points(self) -> int:
        return self.max_move_points
    
    def get_hit_points(self) -> int:
        return self.hit_points
    
    def get_max_hit_points(self) -> int:
        return self.max_hit_points

    def refresh_move_points(self):
        self.move_points = self.max_move_points

    def hurt(self, amnt: int = 1):
        self.hit_points -= amnt
        if self.hit_points < 0:
            self.hit_points = 0

        if self.hit_points == 0:
            self.add_buff(Unconsciousness)

    def heal(self, amnt: int = None):
        if amnt is None:
            self.hit_points = self.max_hit_points
        else:
            self.hit_points = self.max_hit_points if self.hit_points + amnt > self.max_hit_points else self.hit_points + amnt
    
    def move_to_tile(self, tile: TileObjectInterface):
        self.former_tile = self.tile
        if self.tile is not None:
            self.tile.remove_hero(self)
        self.tile = tile
        tile.add_hero(self)
        if self.move_points > 0:
            self.move_points -= 1
    
    def move_to_former_tile(self):
        if self.former_tile is not None:
            if self.tile is not None:
                self.tile.remove_hero(self)
            self.tile = self.former_tile
            self.tile.add_hero(self)

    def get_tile(self) -> TileObjectInterface:
        return self.tile

    def get_definition(self) -> HeroDefinition:
        return self.definition
    
    def get_icon_path(self) -> str:
        return self.definition.icon_path
    
    def get_portrait_path(self) -> str:
        return self.definition.portrait_path
    
    def get_combat_icon_path(self) -> str:
        return self.definition.combat_icon_path
    
    def get_name(self) -> str:
        return self.name
    
    def get_weapon_power(self) -> int:
        return self.power + self.inventory.get_power()
    
    def get_available_actions(self) -> list[Action]:
        la: list[Action] = []
        for a in self.actions:
            if a.is_available():
                la.append(a)

        la.sort(key=lambda x: x.prio)
        return la
    
    def is_in_hostile_tile(self) -> bool:
        p = self.tile.get_placeable()
        return isinstance(p,MinionInterface) and p.agressive
    
    def reset_cooldowns(self, duration_scope: int):
        for a in self.actions:
            if a.cooldown is not None and a.get_cooldown().get_scope() <= duration_scope:
                a.reset_cooldown()

    def reset_action_cooldown(self, action_type: Type[Action]):
        for a in self.actions:
            if isinstance(a,action_type):
                a.reset_cooldown()

    def set_cooldown(self, action_type: Type[Action], duration_scope: int):
        for a in self.actions:
            if isinstance(a,action_type):
                a.set_cooldown(duration_scope)

    def is_action_on_cooldown(self, action_type: Type[Action]) -> bool:
        for a in self.actions:
            if isinstance(a,action_type):
                return a.get_cooldown() is not None
        return False
    
    def has_an_action(self, action_type: Type[Action]) -> bool:
        for a in self.actions:
            if isinstance(a,action_type):
                return True
        return False

    def add_buff(self, buff_type: Type[Buff], duration_scope: int = None):
        self.active_buffs.append(buff_type(self,duration_scope))

    def has_modifier(self, mod_type: Type[BuffModifier]) -> bool:
        for b in self.active_buffs:
            if b.has_modifier(mod_type):
                return True

        for a in self.actions:
            if a.is_available() and a.has_modifier(mod_type):
                return True
                    
        return False
    
    def has_buff(self, buff_type: Type[Buff]) -> bool:
        for b in self.active_buffs:
            if isinstance(b,buff_type):
                return True
        return False
    
    def remove_modifier(self, mod_type: Type[BuffModifier]):
        for b in reversed(self.active_buffs):
            if b.has_modifier(mod_type):
                b.remove()
                self.active_buffs.remove(b)

    @overload
    def remove_buffs(self, duration_scope: int) -> None: ...
    
    @overload
    def remove_buffs(self, buff_type: Type[Buff]) -> None: ...

    def remove_buffs(self, arg) -> None:
        for b in reversed(self.active_buffs):
            remove: bool = False
            if isinstance(arg,int):
                remove = arg is None or b.get_scope() <= arg
            elif issubclass(arg, Buff):
                remove = isinstance(b,arg)
            
            if remove:
                b.remove()
                self.active_buffs.remove(b)
                
    def get_dices(self) -> list[diceType.DiceDefinition]:
        return self.dices
    
    def is_on_fountain(self) -> bool:
        return self.tile is not None and self.tile.get_definition().is_healing
    
    def is_cursed(self) -> bool:
        return self.has_buff(Curse)
    
    def can_pass_walls(self) -> bool:
        return self.has_modifier(CanWalkThroughWalls)
    
    def refresh_actions(self):
        for a in self.actions:
            a.update()

    def fighting_explored(self) -> bool:
        opp = self.get_opponent()
        b = isinstance(opp,MinionInterface) and opp.is_explored()
        return isinstance(opp,MinionInterface) and opp.is_explored()
    
    def explore_minion(self):
        p = self.tile.get_placeable()
        if isinstance(p,MinionInterface) and p.agressive:
            p.explore()