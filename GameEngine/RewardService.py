from __future__ import annotations

from GameContext import GameContext
from GameEngine.Constants import ItemTypes
import GameEngine.Buff as buff
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
        if item.type == ItemTypes.CHEST:
            self.pick_up_item(hero, item)
            return

        free_slot = hero.inventory.get_free_slot(item.type)
        if free_slot is not None:
            self.pick_up_item(hero, item, free_slot)
            return

        self.context.reward = Reward(hero, item)

    def pick_up_item(self, hero: Hero, item: Item, slot: InventorySlot = None):
        leftover = hero.inventory.add_item(item, slot)
        hero.add_buff(buff.PickedUpReward)

        tile = hero.get_tile()
        if leftover is None:
            if tile.get_placeable() == item:
                tile.remove_placeable()
        else:
            tile.add_placeable(leftover)

    def finish_reward(self, slot: InventorySlot = None):
        reward = self.get_reward()
        if reward is None:
            return

        hero = reward.get_hero()
        item = reward.get_item()

        if slot is not None and slot in hero.inventory.slots and slot.verify_type(item.type):
            self.pick_up_item(hero, item, slot)

        self.clear_reward()

    def clear_reward(self):
        self.context.reward = None
