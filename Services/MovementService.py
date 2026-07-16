from __future__ import annotations

from GameContext import GameContext
from GameEngine.Constants import DurationScopes
from GameEngine.DiceManager import DiceManager
import GameEngine.DiceDefinition as diceType
from GameEngine.MinionDefinition import MinionDefinition
from GameEngine.Minion import Minion
import GameEngine.Buff as buff
import GameEngine.BuffModifier as bMod
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.TileObject import TileObject
    from Services.DiceService import DiceService


class MovementService:
    def __init__(self, context: GameContext, dice_service: "DiceService") -> None:
        self.context = context
        self.dice_service = dice_service
        self.curse_roll_active = False
        self.curse_roll_result_until = None
        self.arena_service = None
        self.lord_of_karak_service = None

    def set_arena_service(self, arena_service) -> None:
        self.arena_service = arena_service

    def set_lord_of_karak_service(self, service) -> None:
        self.lord_of_karak_service = service

    def choose_minion(self, tile: TileObject):
        arr = self.context.minion_pack.pick()
        if len(arr) == 0:
            self.move_to_tile(tile)
        else:
            if len(arr) == 1:
                self.spawn_minion(arr[0], tile)
                self.move_to_tile(tile)
            else:
                pass

    def spawn_minion(self, definition: MinionDefinition, tile: TileObject):
        from GameEngine.Minion import Minion
        Minion(definition).set_tile(tile)

    def confirm_tile_placement(self, tile: TileObject):
        self.context.get_current_hero().remove_buffs(buff.ChoosingTile)
        tile.on_click(self.move_to_tile, tile)
        if self.lord_of_karak_service is not None and self.lord_of_karak_service.handle_tile_placed(tile, lambda: self._finish_tile_placement(tile)):
            return
        self._finish_tile_placement(tile)

    def _finish_tile_placement(self, tile: TileObject):
        if tile.is_spawn:
            self.choose_minion(tile)
        else:
            self.move_to_tile(tile)

    def move_to_tile(self, tile: TileObject):
        hero = self.context.get_current_hero()
        hero.move_to_tile(tile)
        hero.reset_cooldowns(DurationScopes.DURATION_SCOPE_TILEMOVE)
        hero.remove_buffs(DurationScopes.DURATION_SCOPE_TILEMOVE)
        if tile.get_definition().is_arena and not tile.arena_triggered and self.arena_service is not None:
            tile.arena_triggered = True
            self.arena_service.start_arena_duel(tile)
            return
        if tile.get_definition().is_cursed and not hero.is_cursed():
            self.start_curse_roll_prompt()
            return

        self.load_move_options()

    def start_curse_roll_prompt(self):
        hero = self.context.get_current_hero()
        self.curse_roll_active = True
        self.curse_roll_result_until = None
        self.context.get_tilemap().disable_all_tiles()
        self.context.ui.get_curse_panel().show_prompt()
        self.context.ui.get_action_panel().clear_actions()
        hero.refresh_actions()
        self.dice_service.force_mouse_motion()

    def is_curse_roll_action_available(self) -> bool:
        return (
            self.curse_roll_active
            and self.curse_roll_result_until is None
            and not self.dice_service.is_dice_rolling()
        )

    def is_curse_roll_active(self) -> bool:
        return self.curse_roll_active

    def roll_curse_dice(self):
        if not self.is_curse_roll_action_available():
            return

        self.dice_service.create_dice_manager([diceType.Normal])
        self.dice_service.start_dice_roll(
            self.context.get_current_hero(),
            apply_roll_lock=False,
            on_finish=self.finish_curse_roll
        )

    def finish_curse_roll(self, dice_manager: DiceManager):
        hero = self.context.get_current_hero()
        if dice_manager.get_value() <= 3:
            self.apply_curse(hero)
            self.context.ui.get_curse_panel().show_result("You were cursed")
        else:
            self.context.ui.get_curse_panel().show_result("You resisted the curse")

        self.curse_roll_result_until = pygame.time.get_ticks() + 2000
        hero.refresh_actions()

    def apply_curse(self, hero: "Hero") -> None:
        for other_hero in self.context.heroes:
            if other_hero is not hero and other_hero.has_buff(buff.Curse):
                other_hero.remove_buffs(buff.Curse)

        if not hero.has_buff(buff.Curse):
            hero.add_buff(buff.Curse)
            hero.refresh_actions()

    def update(self):
        if self.curse_roll_result_until is None:
            return

        if pygame.time.get_ticks() < self.curse_roll_result_until:
            return

        self.dice_service.clear_dice_manager()
        self.curse_roll_active = False
        self.curse_roll_result_until = None
        self.context.ui.get_curse_panel().hide()
        self.context.get_current_hero().refresh_actions()
        self.load_move_options()
        self.dice_service.force_mouse_motion()

    def load_move_options(self):
        hero = self.context.get_current_hero()
        tile = hero.get_tile()
        placeable = tile.get_placeable()

        if not(isinstance(placeable, Minion) and placeable.agressive) or hero.has_modifier(bMod.IgnoreHostiles):
            if hero.get_move_points() > 0 and not hero.has_modifier(bMod.CannotMove):
                tile = hero.get_tile()
                self.context.get_tilemap().load_path(tile, 1)
            else:
                self.context.get_tilemap().disable_all_tiles()
        else:
            self.context.get_tilemap().disable_all_tiles()
