from Interfaces.DiceInterface import DiceInterface
from GameEngine.DiceDefinition import DiceDefinition
from random import choice

class Dice(DiceInterface):
    definition: DiceDefinition
    value: int

    def __init__(self, definition: DiceDefinition):
        self.definition = definition
        self.value = None

    def roll(self):
        self.value = choice(self.definition.values)

    def get_value(self) -> int:
        return self.value