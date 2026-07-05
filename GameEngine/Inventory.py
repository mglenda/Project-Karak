from __future__ import annotations

from GameEngine.ItemDefinition import ItemDefinition
from GameEngine.Constants import Constants,ItemTypes
from GameEngine.InventorySlot import InventorySlot
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero
    from GameEngine.Item import Item

class Inventory:
    max_weapons: int
    max_scrolls: int
    max_keys: int
    hero: Hero

    slots: list[InventorySlot]
    chests: list[Item]

    def __init__(self, hero: Hero) -> None:
        self.max_weapons = Constants.MAX_WEAPONS
        self.max_keys = Constants.MAX_KEYS
        self.max_scrolls = Constants.MAX_SCROLLS
        self.hero = hero

        self.slots = []
        self.chests = []

        for _ in range(self.max_weapons):
            self.slots.append(InventorySlot(ItemTypes.WEAPON))
        
        for _ in range(self.max_scrolls):
            self.slots.append(InventorySlot(ItemTypes.SCROLL))

        for _ in range(self.max_keys):
            self.slots.append(InventorySlot(ItemTypes.KEY))

    def has_item(self, definition: ItemDefinition) -> bool:
        for s in self.slots:
            if s.get_item_definition() == definition:
                return True
        for i in self.chests:
            if i is not None and i.definition == definition:
                return True
        return False

    def remove_item(self, item: Item):
        if item.type == ItemTypes.CHEST:
            if item in self.chests:
                self.chests.remove(item)
        else:
            for s in self.slots:
                if s.get_item() == item:
                    s.remove_item(item)

    def add_item(self, item: Item, slot: InventorySlot = None) -> Item:
        if item.type == ItemTypes.CHEST:
            self.chests.append(item)
        else:
            if slot is None:
                for s in self.slots:
                    if s.get_item() is None and s.verify_type(item.type):
                        return s.add_item(item)
            else:
                return slot.add_item(item)
        return None
    
    def get_slots_by_type(self, type: int) -> list[InventorySlot]:
        slots = []
        for s in self.slots:
            if s.get_type() == type:
                slots.append(s)
        return slots
    
    def get_power(self) -> int:
        power: int = 0
        for s in self.slots:
            power += s.get_item_power()
        return power
