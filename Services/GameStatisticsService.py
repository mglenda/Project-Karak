from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from GameEngine.Hero import Hero
from GameEngine.Minion import Minion

if TYPE_CHECKING:
    from GameEngine.Combat import Combat


@dataclass
class HeroStatistics:
    combats: int = 0
    wins: int = 0
    losses: int = 0
    draws: int = 0
    minion_combats: int = 0
    hero_combats: int = 0
    combat_power_total: int = 0
    highest_combat_power: int = 0
    full_rolls: int = 0
    roll_total: int = 0
    highest_roll: int = 0
    rerolled_dice: int = 0
    minions_defeated: int = 0
    strongest_minion_defeated: int = 0

    def get_win_rate(self) -> float:
        return self.wins / self.combats * 100 if self.combats else 0.0

    def get_average_combat_power(self) -> float:
        return self.combat_power_total / self.combats if self.combats else 0.0

    def get_average_roll(self) -> float:
        return self.roll_total / self.full_rolls if self.full_rolls else 0.0


class GameStatisticsService:
    def __init__(self) -> None:
        self._hero_statistics: dict[Hero, HeroStatistics] = {}

    def get(self, hero: Hero) -> HeroStatistics:
        if hero not in self._hero_statistics:
            self._hero_statistics[hero] = HeroStatistics()
        return self._hero_statistics[hero]

    def record_roll(self, hero: Hero, value: int) -> None:
        statistics = self.get(hero)
        statistics.full_rolls += 1
        statistics.roll_total += value
        statistics.highest_roll = max(statistics.highest_roll, value)

    def record_reroll(self, hero: Hero) -> None:
        self.get(hero).rerolled_dice += 1

    def record_combat(self, combat: Combat) -> None:
        winner = None if combat.is_draw() else combat.get_winner()
        loser = None if combat.is_draw() else combat.get_loser()
        is_hero_combat = combat.is_arena_duel()

        for duelist in combat.duelists:
            if not isinstance(duelist, Hero):
                continue
            statistics = self.get(duelist)
            power = duelist.get_total_power()
            statistics.combats += 1
            statistics.combat_power_total += power
            statistics.highest_combat_power = max(statistics.highest_combat_power, power)
            if is_hero_combat:
                statistics.hero_combats += 1
            else:
                statistics.minion_combats += 1
            if winner is duelist:
                statistics.wins += 1
            elif loser is duelist:
                statistics.losses += 1
            else:
                statistics.draws += 1

            opponent = next(other for other in combat.duelists if other is not duelist)
            if winner is duelist and isinstance(opponent, Minion):
                statistics.minions_defeated += 1
                statistics.strongest_minion_defeated = max(
                    statistics.strongest_minion_defeated,
                    opponent.definition.power,
                )

    def get_master_of_combat(self, heroes: list[Hero]) -> Hero | None:
        winners = [hero for hero in heroes if self.get(hero).wins]
        return self._max_hero(winners, lambda hero: (self.get(hero).wins, self.get(hero).get_win_rate()))

    def get_giant_slayer(self, heroes: list[Hero]) -> Hero | None:
        slayers = [hero for hero in heroes if self.get(hero).minions_defeated]
        return self._max_hero(slayers, lambda hero: (self.get(hero).strongest_minion_defeated, self.get(hero).minions_defeated))

    def get_high_roller(self, heroes: list[Hero]) -> Hero | None:
        rolled = [hero for hero in heroes if self.get(hero).full_rolls]
        return self._max_hero(rolled, lambda hero: (self.get(hero).get_average_roll(), self.get(hero).highest_roll))

    def get_unlucky_soul(self, heroes: list[Hero]) -> Hero | None:
        rolled = [hero for hero in heroes if self.get(hero).full_rolls]
        if not rolled:
            return None
        return min(rolled, key=lambda hero: self.get(hero).get_average_roll())

    @staticmethod
    def _max_hero(heroes: list[Hero], key) -> Hero | None:
        return max(heroes, key=key) if heroes else None
