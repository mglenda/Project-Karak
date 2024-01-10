from GameLogic.Items import Item,TYPE_KEY,TYPE_SCROLL,TYPE_WEAPON

MAX_WEAPONS = 2
MAX_KEYS = 1
MAX_SCROLLS = 3

class Inventory():
    _keys = []
    _weapons = []
    _scrolls = []

    def __init__(self) -> None:
        pass

    def add(self,item:Item) -> bool:
        if self.has_free_slot(item):
            if item.get_type() == TYPE_KEY:
                self.add_key(item)
            elif item.get_type() == TYPE_SCROLL:
                self.add_scroll(item)
            elif item.get_type() == TYPE_WEAPON:
                self.add_weapon(item)
    
    def has_free_slot(self, item: Item) -> bool:
        if item.get_type() == TYPE_KEY:
            return self.has_free_key_slot()
        elif item.get_type() == TYPE_SCROLL:
            return self.has_free_scrol_slot()
        elif item.get_type() == TYPE_WEAPON:
            return self.has_free_weapon_slot()
        
    def add_weapon(self, weapon:Item):
        self._weapons.append(weapon)

    def add_scroll(self, scroll:Item):
        self._scrolls.append(scroll)

    def add_key(self, key:Item):
        self._keys.append(key)

    def has_free_weapon_slot(self) -> bool:
        return self.get_weapons_count() < MAX_WEAPONS
    
    def has_free_key_slot(self) -> bool:
        return self.get_keys_count() < MAX_KEYS
    
    def has_free_scrol_slot(self) -> bool:
        return self.get_scrolls_count() < MAX_SCROLLS
    
    def get_weapons_count(self) -> int:
        return len(self._weapons)
    
    def get_keys_count(self) -> int:
        return len(self._keys)
    
    def get_scrolls_count(self) -> int:
        return len(self._scrolls)