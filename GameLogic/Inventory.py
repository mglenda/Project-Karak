from GameLogic.Items import Item,TYPE_KEY,TYPE_SCROLL,TYPE_WEAPON,TYPE_CHEST

MAX_WEAPONS = 2
MAX_KEYS = 1
MAX_SCROLLS = 3

class Inventory():
    _keys = list[Item]
    _weapons = list[Item]
    _scrolls = list[Item]
    _chests = list[Item]
    _stacks_allowed = dict
    def __init__(self, hero) -> None:
        self._weapons: list[Item] = [None,None]
        self._keys: list[Item] = [None]
        self._scrolls: list[Item] = [None,None,None]
        self._chests: list[Item] = []
        self._stacks_allowed = {}
        self._hero = hero

    def set_allowed_stacks(self, item: Item, stacks: int):
        item = item if not isinstance(item,Item) else item.__class__
        self._stacks_allowed[item] = stacks if stacks >= 0 else 0

    def get_allowed_stacks(self, item: Item):
        item = item if not isinstance(item,Item) else item.__class__
        if item in self._stacks_allowed.keys():
            return self._stacks_allowed[item]
        return 1

    def add(self, item: Item) -> bool:
        if self.has_free_slot(item):
            if item.get_type() == TYPE_KEY:
                self.add_key(item)
            elif item.get_type() == TYPE_SCROLL:
                self.add_scroll(item)
            elif item.get_type() == TYPE_WEAPON:
                self.add_weapon(item)
            elif item.get_type() == TYPE_CHEST:
                self.add_chest(item)
            item.set_hero(self._hero)
            return True
        return False
    
    def remove(self, item: Item):
        if item.get_type() == TYPE_KEY:
            self.remove_key(item)
        elif item.get_type() == TYPE_SCROLL:
            self.remove_scroll(item)
        elif item.get_type() == TYPE_WEAPON:
            self.remove_weapon(item)
        elif item.get_type() == TYPE_CHEST:
            self.remove_chest(item)
        item.set_hero(None)
    
    def has_free_slot(self, item: Item) -> bool:
        if item.get_type() == TYPE_KEY:
            return self.has_free_key_slot()
        elif item.get_type() == TYPE_SCROLL:
            return self.has_free_scroll_slot()
        elif item.get_type() == TYPE_WEAPON:
            return self.has_free_weapon_slot()
        return True
        
    def get_weapons(self) -> list[Item]:
        return self._weapons
    
    def remove_weapon(self, weapon:Item):
        for i,_ in enumerate(self._weapons):
            if self._weapons[i] == weapon:
                self._weapons[i] = None
                break
    
    def get_scrolls(self) -> list[Item]:
        return self._scrolls
    
    def remove_scroll(self, scroll:Item):
        for i,_ in enumerate(self._scrolls):
            if self._scrolls[i] == scroll:
                self._scrolls[i] = None
                break
    
    def get_keys(self) -> list[Item]:
        return self._keys
    
    def remove_key(self, key:Item):
        for i,_ in enumerate(self._keys):
            if self._keys[i] == key:
                self._keys[i] = None
                break

    def get_chests(self) -> list[Item]:
        return self._chests
    
    def remove_chest(self, chest:Item):
        self._chests.remove(chest)
    
    def add_chest(self, chest:Item):
        self._chests.append(chest)
        
    def add_weapon(self, weapon:Item):
        for i,w in enumerate(self._weapons):
            if w == None:
                self._weapons[i] = weapon
                break

    def add_scroll(self, scroll:Item):
        for i,w in enumerate(self._scrolls):
            if w == None:
                self._scrolls[i] = scroll
                break

    def add_key(self, key:Item):
        for i,w in enumerate(self._keys):
            if w == None:
                self._keys[i] = key
                break

    def has_free_weapon_slot(self) -> bool:
        wc = 0
        for w in self._weapons:
            if w is not None:
                wc+=1
        return wc < MAX_WEAPONS
    
    def has_free_key_slot(self) -> bool:
        wc = 0
        for w in self._keys:
            if w is not None:
                wc+=1
        return wc < MAX_KEYS
    
    def has_free_scroll_slot(self) -> bool:
        wc = 0
        for w in self._scrolls:
            if w is not None:
                wc+=1
        return wc < MAX_SCROLLS
    
    def get_items(self) -> list[Item]:
        items: list[Item] = []
        for i in self._weapons:
            items.append(i)
        for i in self._scrolls:
            items.append(i)
        for i in self._keys:
            items.append(i)
        for i in self._chests:
            items.append(i)
        return items