from Interfaces.BuffModifierInterface import BuffModifierInterface
from Interfaces.HeroInterface import HeroInterface

class BuffModifier(BuffModifierInterface):
    hero: HeroInterface

    def __init__(self, hero: HeroInterface):
        self.hero = hero
        self.apply()

    def apply(self):
        pass

    def remove(self):
        self.hero = None

class bm_IgnoreHostiles(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class bm_CannotStartCombat(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)

class bm_CannotEndTurn(BuffModifier):

    def __init__(self, hero):
        super().__init__(hero)