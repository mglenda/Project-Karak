from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.Hero import Hero

class BuffModifier:
    hero: Hero

    def __init__(self, hero: Hero):
        self.hero = hero
        self.enable()

    def enable(self):
        pass

    def disable(self):
        pass

    def remove(self):
        self.disable()
        self.hero = None

    def get_scroll_power_bonus(self) -> int:
        return 0

class IgnoreHostiles(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotStartCombat(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotEndTurn(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotRollDice(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotMove(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class Cursed(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class Injured(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotDoAnything(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CannotPickUpItems(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class CanWalkThroughWalls(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)


class AbilityPower_Plus_1(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

    def enable(self):
        self.hero.add_ability_power(1)
    
    def disable(self):
        self.hero.add_ability_power(-1)

class WinOnDraw(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class MagicalAffinity(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

    def get_scroll_power_bonus(self) -> int:
        power = 0
        for action in self.hero.actions:
            item_definition = getattr(action, "item_definition", None)
            scroll_power = getattr(action, "scroll_power", 0)
            if item_definition is not None and scroll_power > 0:
                power += self.hero.inventory.get_item_count(item_definition) * scroll_power
        return power
