from Interfaces.BuffModifierInterface import BuffModifierInterface
from Interfaces.HeroInterface import HeroInterface

class BuffModifier(BuffModifierInterface):
    hero: HeroInterface

    def __init__(self, hero: HeroInterface):
        self.hero = hero
        self.enable()

    def enable(self):
        pass

    def disable(self):
        pass

    def remove(self):
        self.disable()
        self.hero = None

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

class CanWalkThroughWalls(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)


class AmbushBonus(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

    def enable(self):
        self.hero.add_ability_power(1)
    
    def disable(self):
        self.hero.add_ability_power(-1)

class WinOnDraw(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)