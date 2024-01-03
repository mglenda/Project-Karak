class Ability():
    _passive: bool = False

    def __init__(self) -> None:
        pass

    def is_passive(self):
        return self._passive

#Hero Abilities
class MagicalAffinity(Ability):
    _passive: bool = True

    def __init__(self) -> None:
        super().__init__()

class AstralWalking(Ability):
    _passive: bool = True

    def __init__(self) -> None:
        super().__init__()

#Item Abilities
class UnlockChest(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()