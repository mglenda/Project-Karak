from __future__ import annotations

from GameContext import GameContext
from GameEngine.Constants import ItemTypes
import GameEngine.Buff as buff
from GameEngine.Reward import Reward
from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.Item import Item
    from GameEngine.InventorySlot import InventorySlot


class RewardService:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def get_reward(self) -> Reward:
        return self.context.reward

    def create_reward(self, hero: Hero, item: Item, on_finish: Callable[[Item | None], None] = None):
        if item.type == ItemTypes.CHEST:
            self.pick_up_item(hero, item, on_finish=on_finish)
            return

        free_slot = hero.inventory.get_free_slot(item.type)
        if free_slot is not None:
            self.pick_up_item(hero, item, free_slot, on_finish)
            return

        self.context.reward = Reward(hero, item, on_finish)

    def pick_up_item(self, hero: Hero, item: Item, slot: InventorySlot = None, on_finish: Callable[[Item | None], None] = None):
        leftover = hero.inventory.add_item(item, slot)
        hero.add_buff(buff.ObtainedItem)
        hero.refresh_actions()
        self.context.get_tilemap().disable_all_tiles()

        tile = hero.get_tile()
        if leftover is None:
            if tile.get_placeable() == item:
                tile.remove_placeable()
        else:
            tile.add_placeable(leftover)
        if on_finish is not None:
            on_finish(leftover)

    def finish_reward(self, slot: InventorySlot = None):
        reward = self.get_reward()
        if reward is None:
            return

        hero = reward.get_hero()
        item = reward.get_item()

        if slot is not None and slot in hero.inventory.slots and slot.verify_type(item.type):
            self.pick_up_item(hero, item, slot, reward.get_on_finish())

        self.clear_reward()

    def clear_reward(self):
        self.context.reward = None
