from __future__ import annotations

from GameEngine.ItemDefinition import ItemDefinition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Item import Item

class InventorySlot:
    type: int
    item: Item
    
    def  __init__(self, type: int) -> None:
        self.type = type
        self.item = None

    def add_item(self, item: Item) -> Item:
        leftover = self.item
        self.item = item
        return leftover

    def remove_item(self) -> Item:
        item = self.item
        self.item = None
        return item
    
    def get_item(self) -> Item:
        return self.item

    def set_type(self, type: int):
        self.type = type

    def get_type(self) -> int:
        return self.type

    def get_item_definition(self) -> ItemDefinition:
        if self.item is not None:
            return self.item.definition
        return None
    
    def verify_type(self, type: int) -> bool:
        return self.type == type

    def get_item_power(self) -> int:
        if self.item is not None:
            return self.item.get_power()
        return 0
