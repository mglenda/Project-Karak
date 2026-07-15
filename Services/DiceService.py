from __future__ import annotations

from GameContext import GameContext
from GameEngine.DiceDefinition import DiceDefinition
from GameEngine.DiceManager import DiceManager
import GameEngine.Buff as buff
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero


class DiceService:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def create_dice_manager(self, dice_types: list[DiceDefinition]):
        self.context.dice_manager = DiceManager(dice_types)

    def start_dice_roll(self, hero: Hero, apply_roll_lock: bool = True, on_finish: Callable[[DiceManager], None] = None):
        dice_manager = self.context.dice_manager
        if dice_manager is None or dice_manager.is_rolling():
            return

        self.context.rolling_hero = hero
        self.context.apply_roll_lock = apply_roll_lock
        self.context.dice_roll_finished_callback = on_finish
        dice_manager.start_roll()
        self.context.ui.get_action_panel().clear_actions()

    def start_dice_reroll(self, index: int):
        dice_manager = self.context.dice_manager
        if dice_manager is None or dice_manager.is_rolling():
            return

        self.context.rolling_hero = None
        self.context.apply_roll_lock = False
        dice_manager.start_reroll(index)
        self.context.ui.get_action_panel().clear_actions()

    def finish_dice_roll(self):
        dice_manager = self.context.dice_manager
        if dice_manager is None or not dice_manager.is_rolling():
            return

        dice_manager.commit_roll()
        if self.context.apply_roll_lock and self.context.rolling_hero is not None:
            self.context.rolling_hero.add_buff(buff.CannotRollDices)
            self.context.rolling_hero.refresh_actions()

        on_finish = self.context.dice_roll_finished_callback
        self.context.rolling_hero = None
        self.context.apply_roll_lock = False
        self.context.dice_roll_finished_callback = None
        if on_finish is not None:
            on_finish(dice_manager)

        self.force_mouse_motion()

    def is_dice_rolling(self) -> bool:
        dice_manager = self.context.dice_manager
        return dice_manager is not None and dice_manager.is_rolling()

    def get_dice_manager(self) -> DiceManager:
        return self.context.dice_manager

    def clear_dice_manager(self):
        self.context.dice_manager = None

    def force_mouse_motion(self):
        ui = self.context.ui
        ui.on_mouse_motion(ui.get_mouse_x(), ui.get_mouse_y())
