from GameEngine.Dice import Dice
from GameEngine.DiceDefinition import DiceDefinition

class DiceManager:
    dices: list[Dice]
    rolling: bool
    rolling_indices: list[int]
    roll_id: int

    def __init__(self, dice_types: list[DiceDefinition] = []):
        self.dices = []
        self.rolling = False
        self.rolling_indices = []
        self.roll_id = 0
        for dt in dice_types:
            self.dices.append(Dice(dt))

    def add_dice(self,dice_type: DiceDefinition):
        self.dices.append(Dice(dice_type))

    def start_roll(self):
        if self.rolling:
            return

        self.rolling = True
        self.roll_id += 1
        self.rolling_indices = []
        for i,d in enumerate(self.dices):
            d.roll_pending()
            self.rolling_indices.append(i)

    def start_reroll(self, index: int):
        if self.rolling or index < 0 or index >= len(self.dices):
            return

        self.rolling = True
        self.roll_id += 1
        self.rolling_indices = [index]
        self.dices[index].roll_pending()

    def commit_roll(self):
        for i in self.rolling_indices:
            self.dices[i].commit_roll()
        self.rolling = False
        self.rolling_indices = []

    def cancel_roll(self):
        for d in self.dices:
            d.clear_pending()
        self.rolling = False
        self.rolling_indices = []

    def is_rolling(self) -> bool:
        return self.rolling

    def is_dice_rolling(self, index: int) -> bool:
        return index in self.rolling_indices

    def get_roll_id(self) -> int:
        return self.roll_id

    def roll(self):
        self.start_roll()
        self.commit_roll()

    def get_value(self) -> int:
        res: int = 0
        for d in self.dices:
            res += d.get_value() if d.get_value() is not None else 0
        return res

    def get_dices(self) -> list[Dice]:
        return self.dices

