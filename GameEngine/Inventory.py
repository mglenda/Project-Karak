from Interfaces.ItemInterface import ItemInterface
from Interfaces.InventoryInterface import InventoryInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.ItemDefinition import ItemDefinition
from GameEngine.Constants import Constants,ItemTypes

class Inventory(InventoryInterface):
    max_weapons: int
    max_scrolls: int
    max_keys: int
    hero: HeroInterface

    weapons: list[ItemInterface]
    scrolls: list[ItemInterface]
    keys: list[ItemInterface]
    chests: list[ItemInterface]

    def __init__(self, hero: HeroInterface) -> None:
        self.max_weapons = Constants.MAX_WEAPONS
        self.max_keys = Constants.MAX_KEYS
        self.max_scrolls = Constants.MAX_SCROLLS
        self.hero = hero

        self.keys = []
        self.scrolls = []
        self.weapons = []
        self.chests = []

        for _ in range(self.max_weapons):
            self.weapons.append(None)
        
        for _ in range(self.max_scrolls):
            self.scrolls.append(None)

        for _ in range(self.max_keys):
            self.keys.append(None)

    def has_item(self, definition: ItemDefinition) -> bool:
        for i in self.weapons:
            if i is not None and i.definition == definition:
                return True
        for i in self.scrolls:
            if i is not None and i.definition == definition:
                return True
        for i in self.keys:
            if i is not None and i.definition == definition:
                return True
        for i in self.chests:
            if i is not None and i.definition == definition:
                return True
        return False

    def remove_item(self, item: ItemInterface):
        if item.definition.type == ItemTypes.CHEST:
            if item in self.chests:
                self.chests.remove(item)
        else:
            for i,w in enumerate(self.weapons):
                if w == item:
                    self.weapons[i] = None

            for i,s in enumerate(self.scrolls):
                if s == item:
                    self.scrolls[i] = None

            for i,k in enumerate(self.keys):
                if k == item:
                    self.keys[i] = None

    def add_item(self, item: ItemDefinition, slot_type: int, slot: int = None):
        if slot_type == ItemTypes.WEAPON:
            self.weapons[slot] = item
        elif slot_type == ItemTypes.SCROLL:
            self.scrolls[slot] = item
        elif slot_type == ItemTypes.KEY:
            self.keys[slot] = item
        elif slot_type == ItemTypes.CHEST:
            self.chests.append(item)

    def get_items(self) -> list[ItemInterface]:
        items: list[ItemInterface] = []
        for i in self.weapons:
            if i is not None:
                items.append(i)
        for i in self.scrolls:
            if i is not None:
                items.append(i)
        for i in self.keys:
            if i is not None:
                items.append(i)
        return items

    def get_weapons(self) -> list[ItemInterface]:
        return self.weapons
    
    def get_scrolls(self) -> list[ItemInterface]:
        return self.scrolls
    
    def get_keys(self) -> list[ItemInterface]:
        return self.keys
    
    def get_chests(self) -> list[ItemInterface]:
        return self.chests