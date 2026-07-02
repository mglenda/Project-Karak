from Interfaces.HeroInterface import HeroInterface
from GameEngine.Combat import Combat
from GameEngine.DiceManager import DiceManager
from GameEngine.Reward import Reward
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UI import UI
    from GameEngine.MinionPack import MinionPack
    from Interfaces.TileMapInterface import TileMapInterface


class GameContext:
    def __init__(self) -> None:
        self.ui: "UI" = None
        self.heroes: list[HeroInterface] = []
        self.minion_pack: "MinionPack" = None
        self.combat: Combat = None
        self.dice_manager: DiceManager = None
        self.reward: Reward = None
        self.running: bool = False
        self.rolling_hero: HeroInterface = None
        self.apply_roll_lock: bool = False

    def get_tilemap(self) -> "TileMapInterface":
        return self.ui.get_world().get_tilemap()

    def get_current_hero(self) -> HeroInterface:
        return self.heroes[0]

    def get_current_hero_active(self) -> HeroInterface:
        if self.combat is not None and self.combat.is_arena_duel():
            return self.combat.get_active_duelist()
        return self.get_current_hero()
