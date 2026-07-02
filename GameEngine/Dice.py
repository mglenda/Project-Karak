from Interfaces.DiceInterface import DiceInterface
from GameEngine.DiceDefinition import DiceDefinition
from random import choice

class Dice(DiceInterface):
    definition: DiceDefinition
    value: int
    pending_value: int

    def __init__(self, definition: DiceDefinition):
        self.definition = definition
        self.value = None
        self.pending_value = None

    def roll_pending(self):
        self.pending_value = choice(self.definition.values)

    def commit_roll(self):
        if self.pending_value is not None:
            self.value = self.pending_value
            self.pending_value = None

    def clear_pending(self):
        self.pending_value = None

    def roll(self):
        self.roll_pending()
        self.commit_roll()

    def get_value(self) -> int:
        return self.value

    def get_pending_value(self) -> int:
        return self.pending_value
