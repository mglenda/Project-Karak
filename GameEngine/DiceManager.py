from GameEngine.Dice import Dice
from GameEngine.DiceDefinition import DiceDefinition

class DiceManager:
    dices: list[Dice]

    def __init__(self, dice_types: list[DiceDefinition] = []):
        self.dices = []
        for dt in dice_types:
            self.dices.append(Dice(dt))

    def add_dice(self,dice_type: DiceDefinition):
        self.dices.append(Dice(dice_type))

    def roll(self):
        for d in self.dices:
            d.roll()

    def get_value(self) -> int:
        res: int = 0
        for d in self.dices:
            res += d.get_value() if d.get_value() is not None else 0
        return res

    def get_dices(self) -> list[Dice]:
        return self.dices
