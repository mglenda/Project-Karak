from __future__ import annotations

from GameContext import GameContext
from GameEngine.Reward import Reward
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.Item import Item
    from GameEngine.InventorySlot import InventorySlot


class RewardService:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def get_reward(self) -> Reward:
        return self.context.reward

    def create_reward(self, hero: Hero, item: Item):
        self.context.reward = Reward(hero, item)

    def finish_reward(self, slot: InventorySlot = None):
        reward = self.get_reward()
        if reward is None:
            return

        hero = reward.get_hero()
        item = reward.get_item()

        if slot is not None and slot in hero.inventory.slots and slot.verify_type(item.type):
            leftover = hero.inventory.add_item(item, slot)
            tile = hero.get_tile()
            if leftover is None:
                if tile.get_placeable() == item:
                    tile.remove_placeable()
            else:
                tile.add_placeable(leftover)

        self.clear_reward()

    def clear_reward(self):
        self.context.reward = None
