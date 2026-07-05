from __future__ import annotations

from GameEngine.Combat import Combat
from GameEngine.DiceManager import DiceManager
from GameEngine.Reward import Reward
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI import UI
    from GameEngine.MinionPack import MinionPack
    from GameEngine.Hero import Hero
    from GameEngine.TileMap import TileMap


class GameContext:
    def __init__(self) -> None:
        self.ui: "UI" = None
        self.heroes: list[Hero] = []
        self.minion_pack: "MinionPack" = None
        self.combat: Combat = None
        self.dice_manager: DiceManager = None
        self.reward: Reward = None
        self.running: bool = False
        self.rolling_hero: Hero = None
        self.apply_roll_lock: bool = False

    def get_tilemap(self) -> TileMap:
        return self.ui.get_world().get_tilemap()

    def get_current_hero(self) -> Hero:
        return self.heroes[0]

    def get_current_hero_active(self) -> Hero:
        if self.combat is not None and self.combat.is_arena_duel():
            return self.combat.get_active_duelist()
        return self.get_current_hero()
