from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.Item import Item

class Reward:
    hero: Hero
    item: Item

    def __init__(self, hero: Hero, item: Item):
        self.hero = hero
        self.item = item
    
    def get_hero(self) -> Hero:
        return self.hero
    
    def get_item(self) -> Item:
        return self.item
