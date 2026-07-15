from __future__ import annotations

from GameEngine.Combat import Combat
from GameEngine.DiceManager import DiceManager
from GameEngine.Reward import Reward
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from UI import UI
    from GameEngine.MinionPack import MinionPack
    from GameEngine.Hero import Hero
    from GameEngine.TileMap import TileMap


class GameContext:
    def __init__(self) -> None:
        self.ui: "UI" = None
        self.heroes: list[Hero] = []
        self.initial_hero_order: list[Hero] = []
        self.minion_pack: "MinionPack" = None
        self.combat: Combat = None
        self.dice_manager: DiceManager = None
        self.reward: Reward = None
        self.running: bool = False
        self.rolling_hero: Hero = None
        self.apply_roll_lock: bool = False
        self.dice_roll_finished_callback: Callable[[DiceManager], None] = None

    def get_tilemap(self) -> TileMap:
        return self.ui.get_world().get_tilemap()

    def get_current_hero(self) -> Hero:
        return self.heroes[0]

    def get_current_hero_active(self) -> Hero:
        if self.combat is not None and self.combat.is_arena_duel():
            return self.combat.get_active_duelist()
        if self.reward is not None:
            return self.reward.get_hero()
        return self.get_current_hero()

    def capture_initial_hero_order(self) -> None:
        self.initial_hero_order = list(self.heroes)

    def get_hero_ranking(self) -> list[Hero]:
        initial_order = {
            id(hero): index
            for index, hero in enumerate(self.initial_hero_order)
        }
        return sorted(
            self.heroes,
            key=lambda hero: (
                hero.get_chest_score(),
                hero.get_weapon_power(),
                hero.get_non_chest_non_weapon_slot_item_count(),
                -initial_order.get(id(hero), len(initial_order)),
            ),
            reverse=True,
        )
