import GameLogic.Items as Items

class Minion():
    _power: int
    _reward: Items.Item

    def __init__(self) -> None:
        pass

    def get_power(self):
        return self._power
    
    def kill(self) -> Items.Item:
        return self._reward

class Rat(Minion):
    _power: int = 5
    _reward: Items.Item = Items.Dagger()

    def __init__(self) -> None:
        super().__init__()