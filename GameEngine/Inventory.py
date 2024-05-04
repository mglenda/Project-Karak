from Interfaces.ItemInterface import ItemInterface
from Interfaces.InventoryInterface import InventoryInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.ItemDefinition import ItemDefinition
from GameEngine.Constants import Constants,ItemTypes
from GameEngine.InventorySlot import InventorySlot

class Inventory(InventoryInterface):
    max_weapons: int
    max_scrolls: int
    max_keys: int
    hero: HeroInterface

    slots: list[InventorySlot]
    chests: list[ItemInterface]

    def __init__(self, hero: HeroInterface) -> None:
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

    def remove_item(self, item: ItemInterface):
        if item.type == ItemTypes.CHEST:
            if item in self.chests:
                self.chests.remove(item)
        else:
            for s in self.slots:
                if s.get_item() == item:
                    s.remove_item(item)

    def add_item(self, item: ItemInterface, slot: InventorySlot = None) -> ItemInterface:
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