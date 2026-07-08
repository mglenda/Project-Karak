class TextColors:
    WHITE = (255, 255, 255)
    GREEN = (80, 220, 100)
    RED = (230, 55, 55)
    GOLD = (255, 215, 0)
    PURPLE = (180, 90, 255)

    _LEGACY_NAMES = {
        "White": WHITE,
        "Green": GREEN,
        "Red": RED,
        "Gold": GOLD,
        "Purple": PURPLE,
    }

    @classmethod
    def normalize(cls, color: tuple | str) -> tuple:
        if isinstance(color, str):
            return cls._LEGACY_NAMES[color]
        return color
