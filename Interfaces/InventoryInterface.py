from Interfaces.Interface import Interface
from Interfaces.ItemInterface import ItemInterface
from GameEngine.ItemDefinition import ItemDefinition
from Interfaces.InventorySlotInterface import InventorySlotInterface

class InventoryInterface(Interface):
    max_weapons: int
    max_scrolls: int
    max_keys: int
    hero: Interface

    slots: list[InventorySlotInterface]
    chests: list[ItemInterface]

    def has_item(self, definition: ItemDefinition) -> bool:
        pass

    def remove_item(self, item: ItemInterface):
        pass

    def add_item(self, item: ItemInterface, slot: InventorySlotInterface = None) -> ItemInterface:
        pass

    def get_slots_by_type(self, type: int) -> list[InventorySlotInterface]:
        pass

    def get_power(self) -> int:
        pass