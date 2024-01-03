import Items

MAX_WEAPONS = 2
MAX_KEYS = 1
MAX_SCROLLS = 3

class Inventory():
    _items = [None,None,None,None,None,None]

    def __init__(self) -> None:
        pass

    def add(self,item:Items.Item) -> bool:
        if item.get_type() == Items.TYPE_WEAPON and self.get_count(type=Items.TYPE_WEAPON) < MAX_WEAPONS:
            self._items.append(item)
            return True
        elif item.get_type() == Items.TYPE_KEY and self.get_count(type=Items.TYPE_KEY) < MAX_KEYS:
            self._items.append(item)
            return True
        elif item.get_type() == Items.TYPE_SCROLL and self.get_count(type=Items.TYPE_SCROLL) < MAX_SCROLLS:
            self._items.append(item)
            return True
        return False
    
    def remove(self,item:Items.Item):
        i:Items.Item
        for j,i in enumerate(self._items):
            if i == item:
                self._items[j] = None

    def get(self,slot:int=None,item_type:Items.Item = None) -> Items.Item:
        if item_type is not None:
            if slot is None:
                i:Items.Item
                for i in self._items:
                    if type(i) == item_type:
                        return i
                return None
            else:
                return self._items[slot] if type(self._items[slot]) == item_type else None
        elif slot is None or slot > len(self._items) or slot < 0:
            return None
        return self._items[slot]

    def get_count(self,type:int):
        i:Items.Item
        c = 0
        for i in self._items:
            if i is not None and i.get_type() == type:
                c += 1
        return c
    
    def get_items(self):
        l = []
        i:Items.Item
        for i in self._items:
            if i is not None:
                l.append(i)
        return l