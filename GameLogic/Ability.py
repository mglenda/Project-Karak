PATH = '_Textures\\Abilities\\'

class Ability():
    _passive: bool = False
    _background: str

    def __init__(self) -> None:
        pass

    def is_passive(self):
        return self._passive

#Hero Abilities
class MagicalAffinity(Ability):
    _passive: bool = True
    _background: str = PATH + 'MagicalAffinity.png'

    def __init__(self) -> None:
        super().__init__()

class AstralWalking(Ability):
    _passive: bool = True
    _background: str = PATH + 'AstralWalking.png'

    def __init__(self) -> None:
        super().__init__()

class Berserk(Ability):
    _passive: bool = True
    _background: str = PATH + 'Berserk.png'

    def __init__(self) -> None:
        super().__init__()

class Perseverance(Ability):
    _passive: bool = True
    _background: str = PATH + 'Perseverance.png'

    def __init__(self) -> None:
        super().__init__()

class Backstab(Ability):
    _passive: bool = True
    _background: str = PATH + 'Backstab.png'

    def __init__(self) -> None:
        super().__init__()

class BearAttack(Ability):
    _passive: bool = True
    _background: str = PATH + 'BearAttack.png'

    def __init__(self) -> None:
        super().__init__()

class BlitzAttack(Ability):
    _passive: bool = True
    _background: str = PATH + 'BlitzAttack.png'

    def __init__(self) -> None:
        super().__init__()

class CombatTraining(Ability):
    _passive: bool = True
    _background: str = PATH + 'CombatTraining.png'

    def __init__(self) -> None:
        super().__init__()

class DoubleAttack(Ability):
    _passive: bool = True
    _background: str = PATH + 'DoubleAttack.png'

    def __init__(self) -> None:
        super().__init__()

class Eavesdropping(Ability):
    _passive: bool = True
    _background: str = PATH + 'Eavesdropping.png'

    def __init__(self) -> None:
        super().__init__()

class Fateweaver(Ability):
    _passive: bool = True
    _background: str = PATH + 'Fateweaver.png'

    def __init__(self) -> None:
        super().__init__()

class Foresight(Ability):
    _passive: bool = True
    _background: str = PATH + 'Foresight.png'

    def __init__(self) -> None:
        super().__init__()

class MagicSwap(Ability):
    _passive: bool = True
    _background: str = PATH + 'MagicSwap.png'

    def __init__(self) -> None:
        super().__init__()

class Reincarnation(Ability):
    _passive: bool = True
    _background: str = PATH + 'Reincarnation.png'

    def __init__(self) -> None:
        super().__init__()

class Sacrifice(Ability):
    _passive: bool = True
    _background: str = PATH + 'Sacrifice.png'

    def __init__(self) -> None:
        super().__init__()

class Sprint(Ability):
    _passive: bool = True
    _background: str = PATH + 'Sprint.png'

    def __init__(self) -> None:
        super().__init__()

class Stealth(Ability):
    _passive: bool = True
    _background: str = PATH + 'Stealth.png'

    def __init__(self) -> None:
        super().__init__()

class SwordMaster(Ability):
    _passive: bool = True
    _background: str = PATH + 'SwordMaster.png'

    def __init__(self) -> None:
        super().__init__()

class ThrowingDaggers(Ability):
    _passive: bool = True
    _background: str = PATH + 'ThrowingDaggers.png'

    def __init__(self) -> None:
        super().__init__()

class Unstoppable(Ability):
    _passive: bool = True
    _background: str = PATH + 'Unstoppable.png'

    def __init__(self) -> None:
        super().__init__()

class TacticalReposition(Ability):
    _passive: bool = True
    _background: str = PATH + 'TacticalReposition.png'

    def __init__(self) -> None:
        super().__init__()

class DualWielding(Ability):
    _passive: bool = True
    _background: str = PATH + 'DualWielding.png'

    def __init__(self) -> None:
        super().__init__()

class Ambush(Ability):
    _passive: bool = True
    _background: str = PATH + 'Ambush.png'

    def __init__(self) -> None:
        super().__init__()

class Protector(Ability):
    _passive: bool = True
    _background: str = PATH + 'Protector.png'

    def __init__(self) -> None:
        super().__init__()

class Stoneskin(Ability):
    _passive: bool = True
    _background: str = PATH + 'Stoneskin.png'

    def __init__(self) -> None:
        super().__init__()

class Transformation(Ability):
    _passive: bool = True
    _background: str = PATH + 'Transformation.png'

    def __init__(self) -> None:
        super().__init__()


#Item Abilities
class UnlockChest(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()

class MagicBolt(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()

class ThornOfDarkness(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()

class HealingPortal(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()

class FrostFist(Ability):
    _passive: bool = False

    def __init__(self) -> None:
        super().__init__()