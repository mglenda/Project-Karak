from Interfaces.Interface import Interface
from GameEngine.DiceDefinition import DiceDefinition

class DiceInterface(Interface):
    definition: DiceDefinition
    value: int

    def roll(self):
        pass