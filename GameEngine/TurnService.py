from __future__ import annotations

from GameContext import GameContext
from GameEngine.Constants import DurationScopes
from GameEngine.MovementService import MovementService
import GameEngine.Buff as buff
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero


class TurnService:
    def __init__(self, context: GameContext, movement_service: MovementService) -> None:
        self.context = context
        self.movement_service = movement_service

    def end_turn(self):
        hero = self.context.get_current_hero()

        for h in self.context.heroes:
            if h.has_buff(buff.Unconsciousness):
                h.remove_buffs(buff.Unconsciousness)
                h.add_buff(buff.Injured)

        for i, h in enumerate(self.context.heroes):
            if i != 0:
                self.context.heroes[i - 1] = h
        self.context.heroes[i] = hero

        self.refresh_hero(self.context.heroes[0])
        self.movement_service.load_move_options()

    def refresh_hero(self, hero: Hero):
        hero.refresh_move_points()
        hero.reset_cooldowns(DurationScopes.DURATION_SCOPE_TURN)
        hero.remove_buffs(DurationScopes.DURATION_SCOPE_TURN)
