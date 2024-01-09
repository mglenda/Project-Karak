import GameLogic.Items as Items

MAX_WEAPONS = 2
MAX_KEYS = 1
MAX_SCROLLS = 3

class Inventory():
    _keys = []
    _weapons = []
    _scrolls = []

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