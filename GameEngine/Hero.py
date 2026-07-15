from __future__ import annotations

from GameEngine.HeroDefinition import HeroDefinition
from GameEngine.Duelist import Duelist
from GameEngine.Minion import Minion
from GameEngine.Inventory import Inventory
from GameEngine.Constants import Constants
from GameEngine.Action import Action, PickUpItem, Reincarnation, get_default_action_types
from GameEngine.Buff import Buff,Unconsciousness,ChoosingTile
from GameEngine.BuffModifier import BuffModifier,CanWalkThroughWalls,Cursed
import GameEngine.DiceDefinition as diceType
from typing import TYPE_CHECKING, Type, overload

if TYPE_CHECKING:
    from Game import Game
    from GameEngine.TileObject import TileObject

class Hero(Duelist):
    definition: HeroDefinition
    name: str
    tile: TileObject
    former_tile: TileObject
    hit_points: int
    max_hit_points: int
    move_points: int
    max_move_points: int
    actions: list[Action]
    active_buffs: list[Buff]

    inventory: Inventory

    def __init__(self, definition: HeroDefinition, name: str, game: "Game") -> None:
        Duelist.__init__(self)
        self.game = game
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

        self.actions = [action_type(self, self.game) for action_type in get_default_action_types()]
        self.active_buffs = []

        a_type: Type[Action] = None
        for a_type in self.definition.special_actions:
            self.actions.append(a_type(self, self.game))

        self.actions.sort(key=lambda x: x.prio)

    def get_inventory(self) -> Inventory:
        return self.inventory

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
            for action in self.actions:
                if isinstance(action,Reincarnation) and action.is_available():
                    action.run()
                    return

            self.add_buff(Unconsciousness)

    def heal(self, amnt: int = None):
        if amnt is None:
            self.hit_points = self.max_hit_points
        else:
            self.hit_points = self.max_hit_points if self.hit_points + amnt > self.max_hit_points else self.hit_points + amnt
    
    def move_to_tile(self, tile: TileObject, consume_move_points: bool = True):
        self.former_tile = self.tile
        if self.tile is not None:
            self.tile.remove_hero(self)
        self.tile = tile
        tile.add_hero(self)
        if consume_move_points and self.move_points > 0:
            self.move_points -= 1
    
    def move_to_former_tile(self):
        if self.former_tile is not None:
            if self.tile is not None:
                self.tile.remove_hero(self)
            self.tile = self.former_tile
            self.tile.add_hero(self)

    def get_tile(self) -> TileObject:
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
        return self.power + self.inventory.get_weapon_power()

    def get_chest_score(self) -> float:
        return self.inventory.get_chest_score()

    def get_chest_count(self) -> int:
        return self.inventory.get_chest_count()

    def get_non_chest_non_weapon_slot_item_count(self) -> int:
        return self.inventory.get_non_chest_non_weapon_slot_item_count()

    def get_scroll_power(self) -> int:
        power = super().get_scroll_power()
        for modifier in self.get_active_modifiers():
            power += modifier.get_scroll_power_bonus()
        return power
    
    def get_available_actions(self) -> list[Action]:
        if self.has_buff(ChoosingTile):
            return []

        if self.game.reward_service.get_reward() is not None:
            for a in self.actions:
                a.update_priority()
            return [a for a in self.actions if isinstance(a,PickUpItem) and a.is_available()]

        la: list[Action] = []
        for a in self.actions:
            a.update_priority()
            if a.is_available():
                la.append(a)

        la.sort(key=lambda x: x.prio)
        return la
    
    def is_in_hostile_tile(self) -> bool:
        p = self.tile.get_placeable()
        return isinstance(p, Minion) and p.agressive
    
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
        for modifier in self.get_active_modifiers():
            if isinstance(modifier, mod_type):
                return True
        return False

    def get_active_modifiers(self) -> list[BuffModifier]:
        modifiers: list[BuffModifier] = []
        for b in self.active_buffs:
            modifiers.extend(b.active_modifiers)

        for a in self.actions:
            if a.is_available():
                modifiers.extend(a.modifiers)

        return modifiers
    
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
        #Some actions may have availability bound to specific modifiers which can be part of buffs
        self.refresh_actions()
                
    def get_dices(self) -> list[diceType.DiceDefinition]:
        return [diceType.Normal,diceType.Normal]
    
    def is_on_fountain(self) -> bool:
        return self.tile is not None and self.tile.get_definition().is_healing
    
    def is_cursed(self) -> bool:
        return self.has_modifier(Cursed)
    
    def can_pass_walls(self) -> bool:
        return self.has_modifier(CanWalkThroughWalls)
    
    def refresh_actions(self):
        for a in self.actions:
            a.update()

    def fighting_explored(self) -> bool:
        opp = self.get_opponent()
        return isinstance(opp, Minion) and opp.is_explored()
    
    def explore_minion(self):
        p = self.tile.get_placeable()
        if isinstance(p, Minion) and p.agressive:
            p.explore()
