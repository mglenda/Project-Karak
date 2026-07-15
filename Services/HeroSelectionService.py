from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from GameContext import GameContext

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from Services.MovementService import MovementService


class HeroSelectionService:
    def __init__(self, context: GameContext, movement_service: MovementService) -> None:
        self.context = context
        self.movement_service = movement_service
        self.source_hero: Hero | None = None
        self.candidates: list[Hero] = []
        self.prompt = ''
        self.on_select: Callable[[Hero], None] | None = None
        self.selection_id = 0
        self.restore_movement = True

    def start_selection(
        self,
        source_hero: Hero,
        allow_self: bool,
        on_select: Callable[[Hero], None],
        prompt: str = 'Choose a hero',
        restore_movement: bool = True,
    ) -> bool:
        if self.is_active():
            return False

        candidates = [
            hero for hero in self.context.heroes
            if allow_self or hero is not source_hero
        ]
        if not candidates:
            return False

        self.source_hero = source_hero
        self.candidates = candidates
        self.prompt = prompt
        self.on_select = on_select
        self.selection_id += 1
        self.restore_movement = restore_movement

        self.context.get_tilemap().disable_all_tiles()
        self.context.ui.get_action_panel().clear_actions()
        self.context.ui.get_hero_selection_panel().update()
        source_hero.refresh_actions()
        self.movement_service.dice_service.force_mouse_motion()
        return True

    def select_hero(self, hero: Hero) -> bool:
        if not self.is_active() or hero not in self.candidates:
            return False

        callback = self.on_select
        source_hero = self.source_hero
        restore_movement = self.restore_movement
        self.clear()
        self.context.ui.get_hero_selection_panel().update()
        callback(hero)

        if source_hero is not None:
            source_hero.refresh_actions()
        if restore_movement:
            self.movement_service.load_move_options()
        self.movement_service.dice_service.force_mouse_motion()
        return True

    def clear(self) -> None:
        self.source_hero = None
        self.candidates = []
        self.prompt = ''
        self.on_select = None
        self.restore_movement = True

    def is_active(self) -> bool:
        return self.on_select is not None
