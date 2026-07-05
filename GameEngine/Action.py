from __future__ import annotations

from GameEngine.Cooldown import Cooldown
from GameEngine.Constants import DurationScopes, ItemTypes
from GameEngine.Item import Item
from GameEngine.ItemDefinition import Chest, FrostFist as FrostFistItem, HealingPortal, Key, MagicBolt as MagicBoltItem
from GameEngine.Minion import Minion
from GameEngine.MinionDefinition import ChestClosed
import GameEngine.Buff as buff
import GameEngine.BuffModifier as bMod
from typing import Type
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game
    from GameEngine.Hero import Hero

PATH = '_Textures\\Abilities\\'


ACTION_TYPE_COMBAT: int = 3
ACTION_TYPE_SCROLL: int = 2
ACTION_TYPE_ABILITY: int = 1
ACTION_TYPE_GENERAL: int = 0

class Action:
    hero: Hero
    path: str
    path_focused: str
    prio: int
    cooldown: Cooldown
    default_scope: int
    action_types: list[int]
    modifiers_default: list[Type[bMod.BuffModifier]]
    modifiers: list[bMod.BuffModifier]
    available: bool
    passive: bool
    is_default: bool = False

    def __init__(self, hero: Hero, game: "Game"):
        self.game = game
        self.hero = hero
        self.cooldown = None
        self.available = True

        self.modifiers = []
        for m_class in self.modifiers_default:
            self.modifiers.append(m_class(hero))

    def get_availability(self) -> bool:
        return self.cooldown is None and not self.hero.has_modifier(bMod.CannotDoAnything) and (not self.is_action_type(ACTION_TYPE_ABILITY) or not self.hero.has_modifier(bMod.Cursed)) and (self.is_action_type(ACTION_TYPE_COMBAT) or not self.hero.has_modifier(bMod.Injured))

    def is_available(self) -> bool:
        return self.available

    def update_priority(self):
        pass
    
    def update(self):
        self.update_priority()
        former_available = self.available
        self.available = self.get_availability()

        if former_available != self.available:
            for m in self.modifiers:
                if former_available:
                    m.disable()
                else:
                    m.enable()

    def has_modifier(self, mod_type: Type[bMod.BuffModifier]) -> bool:
        for m in self.modifiers:
            if isinstance(m,mod_type):
                return True
        return False

    def run(self):
        self.set_cooldown(self.default_scope)

    def reset_cooldown(self):
        self.cooldown = None

    def set_cooldown(self, duration_scope: int):
        self.cooldown = Cooldown(duration_scope)

    def get_cooldown(self) -> Cooldown:
        return self.cooldown
    
    def is_action_type(self, action_type: int) -> bool:
        return action_type in self.action_types

    def is_passive(self) -> bool:
        return self.passive

class ActionCombat(Action):
    path = PATH + 'Combat.png'
    path_focused = PATH + 'CombatFocused.png'
    prio: int = 4
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self) -> bool:
        return super().get_availability() and ((self.hero.is_in_combat() and self.hero.has_modifier(bMod.CannotRollDice)) or (self.hero.is_in_hostile_tile() and not self.hero.is_in_combat() and not self.hero.has_modifier(bMod.CannotStartCombat)))
    
    def run(self):
        if self.hero.is_in_combat():
            self.set_cooldown(DurationScopes.DURATION_SCOPE_TURN)
            self.game.combat_service.end_combat()
        else:
            self.game.combat_service.start_combat()

class PickUpItem(Action):
    path = PATH + 'PickUpItem.png'
    path_focused = PATH + 'PickUpItemFocused.png'
    prio: int = 4
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self) -> bool:
        reward = self.game.reward_service.get_reward()
        if reward is not None and reward.get_hero() == self.hero:
            return True

        placeable = self.hero.get_tile().get_placeable()
        return (
            super().get_availability()
            and not self.hero.has_buff(buff.PickedUpReward)
            and placeable is not None
            and isinstance(placeable, Item)
            and placeable.type in (ItemTypes.WEAPON, ItemTypes.SCROLL, ItemTypes.KEY)
            and self.hero.inventory.can_pick_up_item(placeable)
        )
    
    def run(self):
        reward = self.game.reward_service.get_reward()
        if reward is not None:
            selected_slot = self.game.context.ui.get_reward_panel().get_selected_slot()
            self.game.reward_service.finish_reward(selected_slot)
        else:
            self.game.reward_service.create_reward(self.hero, self.hero.get_tile().get_placeable())

class UnlockChest(Action):
    path = PATH + 'UnlockChest.png'
    path_focused = PATH + 'UnlockChest.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self) -> bool:
        placeable = self.hero.get_tile().get_placeable()
        return (
            super().get_availability()
            and not self.hero.has_buff(buff.PickedUpReward)
            and isinstance(placeable, Minion)
            and placeable.definition == ChestClosed
            and self.hero.inventory.has_item(Key)
        )

    def run(self):
        if self.hero.inventory.consume_item(Key) is None:
            self.update()
            return

        chest = self.hero.get_tile().get_placeable()
        if chest is not None:
            self.hero.get_tile().remove_placeable()
            chest.tile = None

        self.game.reward_service.create_reward(self.hero, Item(Chest))

class EndTurn(Action):
    path = PATH + 'EndTurn.png'
    path_focused = PATH + 'EndTurnFocused.png'
    prio: int = 8
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self) -> bool:
        return (not self.hero.is_in_hostile_tile() or self.hero.has_modifier(bMod.IgnoreHostiles) or self.hero.has_modifier(bMod.CannotStartCombat)) and not(self.hero.is_in_combat()) and not self.hero.has_modifier(bMod.CannotEndTurn)
    
    def run(self):
        self.game.turn_service.end_turn()

    def set_cooldown(self, cooldown_scope):
        pass

class Stealth(Action):
    path = PATH + 'Stealth.png'
    path_focused = PATH + 'Stealth.png'
    prio: int = 5
    default_scope: int = DurationScopes.DURATION_SCOPE_TILEMOVE
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.IgnoreHostiles]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self) -> bool:
        # return super().get_availability() and self.hero.is_in_hostile_tile() and not(self.hero.is_in_combat()) and not(self.hero.has_modifier(bMod.CannotStartCombat))
        return super().get_availability()
    
    def run(self):
        # super().run()
        # if not self.hero.is_action_on_cooldown(ActionCombat):
        #     self.hero.set_cooldown(ActionCombat,DurationScopes.DURATION_SCOPE_TILEMOVE)
        # self.hero.add_buff(buff.Stealth)
        # self.hero.explore_minion()
        # self.game.movement_service.load_move_options()
        pass

class RollDice(Action):
    path = PATH + 'RollDice.png'
    path_focused = PATH + 'RollDiceFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL,ACTION_TYPE_COMBAT]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability() and self.game.dice_service.get_dice_manager() is not None and not self.game.dice_service.is_dice_rolling() and not self.hero.has_modifier(bMod.CannotRollDice)
    
    def run(self):
        self.game.dice_service.start_dice_roll(self.hero)

class Revitalize(Action):
    path = PATH + 'Revitalize.png'
    path_focused = PATH + 'RevitalizeFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return self.hero.has_buff(buff.Injured)
    
    def run(self):
        self.hero.remove_buffs(buff.Injured)
        self.hero.heal(1)
        self.game.turn_service.end_turn()

class HealingFountain(Action):
    path = PATH + 'FountainHeal.png'
    path_focused = PATH + 'FountainHealFocused.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_GENERAL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability() and self.hero.is_on_fountain() and (self.hero.is_cursed() or self.hero.get_hit_points() < self.hero.get_max_hit_points())
    
    def run(self):
        self.hero.remove_buffs(buff.Curse)
        self.hero.heal()
        self.hero.set_move_points(0)
        self.hero.add_buff(buff.HealedOnFountain)
        self.game.movement_service.load_move_options()

class ActionHealingPortal(Action):
    path = PATH + 'HealingPortal.png'
    path_focused = PATH + 'HealingPortal.png'
    prio: int = 9
    action_types: list[int] = [ACTION_TYPE_SCROLL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False
    is_default = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def update_priority(self):
        half_hit_points = self.hero.get_max_hit_points() // 2
        if self.hero.is_cursed() or self.hero.get_hit_points() <= half_hit_points:
            self.prio = 2
        else:
            self.prio = 10

    def get_availability(self):
        return (
            super().get_availability()
            and self.hero.inventory.has_item(HealingPortal)
            and not self.hero.is_in_combat()
            and (
                not self.hero.is_in_hostile_tile()
                or self.hero.has_modifier(bMod.IgnoreHostiles)
                or self.hero.has_modifier(bMod.CannotStartCombat)
            )
        )

    def run(self):
        if self.hero.inventory.consume_item(HealingPortal) is None:
            self.update()
            return

        self.hero.add_buff(buff.ChoosingTile)
        self.game.context.get_tilemap().load_healing_portal_targets(self)
        self.game.context.ui.get_action_panel().clear_actions()

    def teleport_to_healing_tile(self, tile):
        self.hero.remove_buffs(buff.ChoosingTile)
        self.hero.move_to_tile(tile, consume_move_points=False)
        self.hero.remove_modifier(bMod.Cursed)
        self.hero.heal()
        self.game.movement_service.load_move_options()

class DoubleAttack(Action):
    path = PATH + 'DoubleAttack.png'
    path_focused = PATH + 'DoubleAttack.png'
    prio: int = 0
    default_scope: int = DurationScopes.DURATION_SCOPE_COMBAT
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def update_priority(self):
        combat = self.game.combat_service.get_combat()
        if combat is None:
            self.prio = 0
            return

        if combat.get_winner() == self.hero:
            self.prio = 10
        else:
            self.prio = 0

    def get_availability(self):
        dice_manager = self.game.dice_service.get_dice_manager()
        return (
            super().get_availability()
            and self.hero.is_in_combat()
            and self.hero.has_modifier(bMod.CannotRollDice)
            and dice_manager is not None
            and dice_manager.get_roll_id() == 1
            and not dice_manager.is_rolling()
        )

    def run(self):
        super().run()
        self.game.dice_service.start_dice_roll(self.hero)

class ScrollPowerAction(Action):
    item_definition = None
    scroll_power: int = 0
    prio: int = 10
    action_types: list[int] = [ACTION_TYPE_SCROLL]
    modifiers_default: list[Type[bMod.BuffModifier]] = []
    modifiers: list[bMod.BuffModifier]
    passive = False

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def update_priority(self):
        dice_manager = self.game.dice_service.get_dice_manager()
        if dice_manager is None or dice_manager.get_roll_id() == 0:
            self.prio = 10
            return

        combat = self.game.combat_service.get_combat()
        if combat is not None and combat.get_loser() == self.hero:
            self.prio = 4
        else:
            self.prio = 10

    def get_availability(self):
        return (
            super().get_availability()
            and self.hero.is_in_combat()
            and self.item_definition is not None
            and self.hero.inventory.has_item(self.item_definition)
            and not self.hero.has_modifier(bMod.MagicalAffinity)
        )

    def run(self):
        if self.hero.inventory.consume_item(self.item_definition) is None:
            self.update()
            return

        self.hero.add_scroll_power(self.scroll_power)
        self.hero.refresh_actions()
        self.game.force_mouse_motion()

class MagicBolt(ScrollPowerAction):
    path = PATH + 'MagicBolt.png'
    path_focused = PATH + 'MagicBolt.png'
    item_definition = MagicBoltItem
    scroll_power: int = 1
    is_default = True

class FrostFist(ScrollPowerAction):
    path = PATH + 'FrostFist.png'
    path_focused = PATH + 'FrostFist.png'
    item_definition = FrostFistItem
    scroll_power: int = 2
    is_default = True

class MagicalAffinity(Action):
    path = PATH + 'MagicalAffinity.png'
    path_focused = PATH + 'MagicalAffinity.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.MagicalAffinity]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability() and self.hero.is_in_combat()

class AstralWalking(Action):
    path = PATH + 'AstralWalking.png'
    path_focused = PATH + 'AstralWalking.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.CanWalkThroughWalls]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability()
    
    def run(self):
        pass

class Ambush(Action):
    path = PATH + 'Ambush.png'
    path_focused = PATH + 'Ambush.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.AbilityPower_Plus_1]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability() and self.hero.fighting_explored()
    
    def run(self):
        pass

class Backstab(Action):
    path = PATH + 'Backstab.png'
    path_focused = PATH + 'Backstab.png'
    prio: int = 0
    action_types: list[int] = [ACTION_TYPE_ABILITY]
    modifiers_default: list[Type[bMod.BuffModifier]] = [bMod.WinOnDraw]
    modifiers: list[bMod.BuffModifier]
    passive = True

    def __init__(self, hero, game: "Game"):
        super().__init__(hero, game)

    def get_availability(self):
        return super().get_availability()
    
    def run(self):
        pass


def _iter_action_types(action_type: Type[Action]):
    for subclass in action_type.__subclasses__():
        yield subclass
        yield from _iter_action_types(subclass)


def get_default_action_types() -> list[Type[Action]]:
    return [action_type for action_type in _iter_action_types(Action) if action_type.is_default]

