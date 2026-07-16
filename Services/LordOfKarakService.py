from __future__ import annotations

from typing import Callable, TYPE_CHECKING

import GameEngine.Buff as buff
from GameEngine.HeroDefinition import LordOfKarak

if TYPE_CHECKING:
    from GameContext import GameContext
    from GameEngine.TileObject import TileObject


class LordOfKarakService:
    SECRET_CHAMBERS_REQUIRED = 4

    def __init__(self, context: GameContext) -> None:
        self.context = context
        self.triggered = False
        self.active = False
        self.hero = None
        self.former_action_types = []
        self.new_action_types = []
        self.on_dismiss: Callable[[], None] | None = None

    def handle_tile_placed(self, tile: TileObject, on_dismiss: Callable[[], None]) -> bool:
        if self.triggered or not tile.get_definition().is_secret_chamber:
            return False
        secret_count = sum(t.get_definition().is_secret_chamber for t in self.context.get_tilemap().tiles)
        if secret_count < self.SECRET_CHAMBERS_REQUIRED:
            return False
        self.triggered = True
        self.active = True
        self.on_dismiss = on_dismiss
        self._transform_last_ranked_hero()
        self.context.get_tilemap().disable_all_tiles()
        self.context.ui.get_action_panel().clear_actions()
        self.context.ui.get_lord_of_karak_panel().update()
        return True

    def _transform_last_ranked_hero(self) -> None:
        self.hero = self.context.get_hero_ranking()[-1]
        self.former_action_types = [type(action) for action in self.hero.special_actions]
        action_types = list(self.former_action_types) if len(self.context.heroes) == 2 else []
        for other in self.context.heroes:
            if other is not self.hero:
                action_types.extend(type(action) for action in other.special_actions)
        self.new_action_types = list(dict.fromkeys(action_types))
        self.hero.definition = LordOfKarak
        self.hero.replace_special_actions(self.new_action_types)
        self.hero.heal()
        self.hero.refresh_move_points()
        self.hero.remove_buffs(buff.Curse)
        self.hero.refresh_actions()
        if self.hero.get_tile() is not None:
            self.hero.get_tile().graphics_refresh_heroes()

    def dismiss(self) -> None:
        if not self.active:
            return
        continuation = self.on_dismiss
        self.active = False
        self.on_dismiss = None
        self.context.ui.get_lord_of_karak_panel().update()
        continuation()

    def is_active(self) -> bool:
        return self.active
