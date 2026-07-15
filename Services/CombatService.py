from __future__ import annotations

from GameContext import GameContext
from GameEngine.Combat import Combat
from Services.DiceService import DiceService
from GameEngine.Duelist import Duelist
from GameEngine.Constants import DurationScopes
from GameEngine.Hero import Hero
from GameEngine.Minion import Minion
import GameEngine.Buff as buff
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Services.HeroSelectionService import HeroSelectionService
    from Services.MovementService import MovementService
    from Services.RewardService import RewardService
    from GameEngine.Item import Item


class CombatService:
    def __init__(self, context: GameContext, dice_service: DiceService, movement_service: MovementService, hero_selection_service: HeroSelectionService, reward_service: RewardService) -> None:
        self.context = context
        self.dice_service = dice_service
        self.movement_service = movement_service
        self.hero_selection_service = hero_selection_service
        self.reward_service = reward_service
        self.arena_tile = None
        self.arena_loot_winner = None
        self.arena_loot_loser = None
        self.arena_loot_items = []

    def start_arena_duel(self, tile) -> None:
        attacker = self.context.get_current_hero()
        opponents = [hero for hero in self.context.heroes if hero is not attacker]
        if not opponents:
            self.movement_service.load_move_options()
            return
        self.arena_tile = tile
        if len(opponents) == 1:
            self._start_arena_combat(opponents[0])
            return
        self.hero_selection_service.start_selection(
            attacker,
            allow_self=False,
            on_select=self._start_arena_combat,
            prompt='Choose an arena opponent',
            restore_movement=False,
        )

    def _start_arena_combat(self, defender: Hero) -> None:
        attacker = self.context.get_current_hero()
        defender.remove_buffs(buff.Exhausted)
        defender.remove_buffs(buff.ObtainedItem)
        defender.reset_cooldowns(DurationScopes.DURATION_SCOPE_TURN)
        defender.move_to_tile(self.arena_tile, consume_move_points=False)
        self.context.get_tilemap().disable_all_tiles()
        self.context.combat = Combat(attacker, defender)
        self.dice_service.create_dice_manager(attacker.get_dices())
        attacker.refresh_actions()
        defender.refresh_actions()

    def is_arena_loot_active(self) -> bool:
        return bool(self.arena_loot_items)

    def select_arena_loot(self, item: Item) -> bool:
        if item not in self.arena_loot_items:
            return False
        winner = self.arena_loot_winner
        loser = self.arena_loot_loser
        self.clear_arena_loot()
        self.context.ui.get_arena_loot_panel().update()
        if loser.inventory.remove_item(item) is None:
            return False
        self.reward_service.create_reward(
            winner,
            item,
            on_finish=lambda leftover: self._finish_arena_reward(loser, leftover),
        )
        return True

    def _finish_arena_reward(self, loser: Hero, leftover: Item | None) -> None:
        if leftover is not None and loser is self.context.get_current_hero():
            loser.add_buff(buff.ArenaPickupBlocked)
            loser.refresh_actions()

    def clear_arena_loot(self) -> None:
        self.arena_loot_winner = None
        self.arena_loot_loser = None
        self.arena_loot_items = []

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
                loser = None
                curse_target_on_defeat = False
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
                        curse_target_on_defeat = loser.definition.curse_target_on_defeat
                        loser.remove()
                    elif combat.is_arena_duel():
                        loser.hurt()
                        self.arena_loot_winner = winner
                        self.arena_loot_loser = loser
                        self.arena_loot_items = [
                            slot.get_item() for slot in loser.inventory.slots
                            if slot.get_item() is not None
                        ] + list(loser.inventory.chests)
                self.dice_service.clear_dice_manager()
                arena_duel = combat.is_arena_duel()
                combat.end(add_exhausted=not arena_duel)
                if arena_duel:
                    active_hero = self.context.get_current_hero()
                    if not active_hero.has_buff(buff.Exhausted):
                        active_hero.add_buff(buff.Exhausted)
                    active_hero.refresh_actions()
                self.context.combat = None
                self.context.ui.get_arena_loot_panel().update()
                if combat.is_arena_duel() and not self.is_arena_loot_active():
                    self.movement_service.load_move_options()
                if not combat.is_draw() and isinstance(loser, Minion) and curse_target_on_defeat:
                    self.hero_selection_service.start_selection(
                        self.context.get_current_hero(),
                        allow_self=True,
                        on_select=self.movement_service.apply_curse,
                        prompt='Choose a hero to curse',
                    )
            else:
                combat.active_next()
                self.dice_service.create_dice_manager(self.context.get_current_hero_active().get_dices())

    def get_combat(self) -> Combat:
        return self.context.combat
