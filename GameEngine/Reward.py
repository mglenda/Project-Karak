from __future__ import annotations

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.Item import Item

class Reward:
    hero: Hero
    item: Item

    def __init__(self, hero: Hero, item: Item, on_finish: Callable[[Item | None], None] = None):
        self.hero = hero
        self.item = item
        self.on_finish = on_finish
    
    def get_hero(self) -> Hero:
        return self.hero
    
    def get_item(self) -> Item:
        return self.item

    def get_on_finish(self):
        return self.on_finish
