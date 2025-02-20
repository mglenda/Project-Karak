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