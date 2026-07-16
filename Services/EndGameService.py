from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING

from GameEngine.Item import Item
from GameEngine.MinionDefinition import Dragon

if TYPE_CHECKING:
    from GameContext import GameContext
    from GameEngine.Hero import Hero
    from GameEngine.Minion import Minion
    from Services.RewardService import RewardService
    from Services.GameStatisticsService import GameStatisticsService


class EndGamePhase(Enum):
    INACTIVE = auto()
    ANNOUNCEMENT = auto()
    REPORT = auto()


class EndGameService:
    def __init__(self, context: GameContext, reward_service: RewardService,
                 statistics_service: GameStatisticsService = None) -> None:
        self.context = context
        self.reward_service = reward_service
        self.statistics_service = statistics_service
        self.phase = EndGamePhase.INACTIVE
        self.reason = ''
        self.triggering_hero: Hero | None = None
        self.ranking: list[Hero] = []
        self.selected_hero: Hero | None = None

    def handle_minion_defeated(self, hero: Hero, minion: Minion) -> bool:
        if self.phase is not EndGamePhase.INACTIVE or minion.definition is not Dragon:
            return False

        self.reward_service.create_reward(hero, Item(minion.definition.reward))
        minion.remove(drop_reward=False)
        self.triggering_hero = hero
        self.reason = f'{hero.get_name()} has slain the Dragon. The game is over.'
        self.ranking = list(self.context.get_hero_ranking())
        self.phase = EndGamePhase.ANNOUNCEMENT
        self.context.get_tilemap().disable_all_tiles()
        self.context.ui.get_action_panel().clear_actions()
        return True

    def continue_to_report(self) -> None:
        if self.phase is EndGamePhase.ANNOUNCEMENT:
            self.phase = EndGamePhase.REPORT

    def show_hero_detail(self, hero: Hero) -> None:
        if self.is_report() and hero in self.ranking:
            self.selected_hero = hero

    def close_hero_detail(self) -> None:
        self.selected_hero = None

    def is_hero_detail_visible(self) -> bool:
        return self.selected_hero is not None

    def is_active(self) -> bool:
        return self.phase is not EndGamePhase.INACTIVE

    def is_announcement(self) -> bool:
        return self.phase is EndGamePhase.ANNOUNCEMENT

    def is_report(self) -> bool:
        return self.phase is EndGamePhase.REPORT
