from __future__ import annotations

from GameContext import GameContext
from GameEngine.Combat import Combat
from Services.DiceService import DiceService
from GameEngine.Duelist import Duelist
from GameEngine.Constants import DurationScopes
from GameEngine.Hero import Hero
from GameEngine.Minion import Minion


class CombatService:
    def __init__(self, context: GameContext, dice_service: DiceService) -> None:
        self.context = context
        self.dice_service = dice_service

    def start_combat(self):
        self.context.get_tilemap().disable_all_tiles()
        attacker: Duelist = self.context.get_current_hero()
        defender: Duelist = attacker.get_tile().get_placeable()
        self.context.combat = Combat(attacker, defender)
        self.dice_service.create_dice_manager(self.context.get_current_hero().get_dices())

    def end_combat(self):
        combat = self.context.combat
        h = combat.get_active_duelist()
        if isinstance(h, Hero):
            h.reset_cooldowns(DurationScopes.DURATION_SCOPE_COMBAT)
            h.remove_buffs(DurationScopes.DURATION_SCOPE_COMBAT)

        if combat is not None:
            if combat.is_finished():
                if combat.is_draw():
                    if not combat.is_arena_duel():
                        self.context.get_current_hero().move_to_former_tile()
                else:
                    loser = combat.get_loser()
                    winner = combat.get_winner()
                    if isinstance(winner, Minion):
                        winner.explore()
                        self.context.get_current_hero().hurt()
                        self.context.get_current_hero().move_to_former_tile()
                    elif isinstance(loser, Minion):
                        loser.remove()
                self.dice_service.clear_dice_manager()
                combat.end()
                self.context.combat = None
            else:
                combat.active_next()
                self.dice_service.create_dice_manager(self.context.get_current_hero_active().get_dices())

    def get_combat(self) -> Combat:
        return self.context.combat
