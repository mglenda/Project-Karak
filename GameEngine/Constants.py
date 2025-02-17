class Constants():
    HERO_MAX_HP: int = 5
    HERO_MOVEPOINTS: int = 4
    DEFAULT_TILESIZE: int = 100
    MAX_KEYS = 1
    MAX_WEAPONS = 2
    MAX_SCROLLS = 3

class ItemTypes():
    WEAPON = 0
    SCROLL = 1
    KEY = 2
    CHEST = 3

class CooldownScopes():
    COOLDOWN_SCOPE_COMBAT = 0
    COOLDOWN_SCOPE_TILEMOVE = 1
    COOLDOWN_SCOPE_TURN = 5