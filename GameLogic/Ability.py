from Game import GAME
from GameLogic.Combatiant import Combatiant
from GUI._const_combat_modifiers import MODIFIER_ABILITY,MODIFIER_SCROLL

PATH = '_Textures\\Abilities\\'

STAGE_ALWAYS = 0
STAGE_FIGHT = 1
STAGE_FIGHT_START = 2
STAGE_FIGHT_END = 3
STAGE_FIGHT_AFTERMATH = 5
STAGE_EXPLORING = 4
STAGE_TURNBEGIN = 6

class Ability():
    _passive: bool = False
    _background: str
    _name: str
    _hero_card: bool = True
    _active: bool = True

    def __init__(self, user) -> None:
        self._user = user

    def is_passive(self):
        return self._passive
    
    def get_icon(self) -> str:
        return self._background
    
    def get_name(self) -> str:
        return self._name
    
    def is_usable(self) -> bool:
        return False
    
    def is_active(self) -> bool:
        return self._active
    
    def get_user(self):
        return self._user
    
    def set_user(self, user):
        self._user = user
    
    def set_active(self, active:bool):
        self._active = active
    
    def use(self):
        GAME.get_abilities_panel().reload()

#Hero Abilities
class RollDice(Ability):
    _passive: bool = False
    _background: str = PATH + 'RollDice.png'   
    _name: str = 'Roll'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

class MagicalAffinity(Ability):
    _passive: bool = True
    _background: str = PATH + 'MagicalAffinity.png'
    _name: str = 'Magic Affinity'

    def __init__(self, user) -> None:
        super().__init__(user)

class AstralWalking(Ability):
    _passive: bool = True
    _background: str = PATH + 'AstralWalking.png'
    _name: str = 'Astral Walking'

    def __init__(self, user) -> None:
        super().__init__(user)

class Berserk(Ability):
    _passive: bool = True
    _background: str = PATH + 'Berserk.png'
    _name: str = 'Berserk'

    def __init__(self, user) -> None:
        super().__init__(user)

class Perseverance(Ability):
    _passive: bool = True
    _background: str = PATH + 'Perseverance.png'
    _name: str = 'Perseverance'

    def __init__(self, user) -> None:
        super().__init__(user)

class Backstab(Ability):
    _passive: bool = True
    _background: str = PATH + 'Backstab.png'
    _name: str = 'Backstab'

    def __init__(self, user) -> None:
        super().__init__(user)

class BearAttack(Ability):
    _passive: bool = True
    _background: str = PATH + 'BearAttack.png'
    _name: str = 'Bear Attack'

    def __init__(self, user) -> None:
        super().__init__(user)

class BlitzAttack(Ability):
    _passive: bool = False
    _background: str = PATH + 'BlitzAttack.png'
    _name: str = 'Blitz Attack'

    def __init__(self, user) -> None:
        super().__init__(user)

class CombatTraining(Ability):
    _passive: bool = False
    _background: str = PATH + 'CombatTraining.png'
    _name: str = 'Combat Training'

    def __init__(self, user) -> None:
        super().__init__(user)

class DoubleAttack(Ability):
    _passive: bool = False
    _background: str = PATH + 'DoubleAttack.png'
    _name: str = 'Double Attack'

    def __init__(self, user) -> None:
        super().__init__(user)

class Eavesdropping(Ability):
    _passive: bool = False
    _background: str = PATH + 'Eavesdropping.png'
    _name: str = 'Eavesdropping'

    def __init__(self, user) -> None:
        super().__init__(user)

class Fateweaver(Ability):
    _passive: bool = True
    _background: str = PATH + 'Fateweaver.png'
    _name: str = 'Fateweaver'

    def __init__(self, user) -> None:
        super().__init__(user)

class Foresight(Ability):
    _passive: bool = True
    _background: str = PATH + 'Foresight.png'
    _name: str = 'Foresight' 

    def __init__(self, user) -> None:
        super().__init__(user)

class MagicSwap(Ability):
    _passive: bool = False
    _background: str = PATH + 'MagicSwap.png'
    _name: str = 'Magic Swap'

    def __init__(self, user) -> None:
        super().__init__(user)

class Reincarnation(Ability):
    _passive: bool = True
    _background: str = PATH + 'Reincarnation.png'
    _name: str = 'Reincarnation'

    def __init__(self, user) -> None:
        super().__init__(user)

class Sacrifice(Ability):
    _passive: bool = False
    _background: str = PATH + 'Sacrifice.png'
    _name: str = 'Sacrifice'

    def __init__(self, user) -> None:
        super().__init__(user)

class Sprint(Ability):
    _passive: bool = False
    _background: str = PATH + 'Sprint.png'
    _name: str = 'Sprint'

    def __init__(self, user) -> None:
        super().__init__(user)

class Stealth(Ability):
    _passive: bool = False
    _background: str = PATH + 'Stealth.png'
    _name: str = 'Stealth'

    def __init__(self, user) -> None:
        super().__init__(user)

class SwordMaster(Ability):
    _passive: bool = True
    _background: str = PATH + 'SwordMaster.png'
    _name: str = 'Sword Master'

    def __init__(self, user) -> None:
        super().__init__(user)

class ThrowingDaggers(Ability):
    _passive: bool = True
    _background: str = PATH + 'ThrowingDaggers.png'
    _name: str = 'Throwing Daggers'

    def __init__(self, user) -> None:
        super().__init__(user)

class Unstoppable(Ability):
    _passive: bool = True
    _background: str = PATH + 'Unstoppable.png'
    _name: str = 'Unstoppable'

    def __init__(self, user) -> None:
        super().__init__(user)

class TacticalReposition(Ability):
    _passive: bool = False
    _background: str = PATH + 'TacticalReposition.png'
    _name: str = 'Tactical Reposition'

    def __init__(self, user) -> None:
        super().__init__(user)

class DualWielding(Ability):
    _passive: bool = False
    _background: str = PATH + 'DualWielding.png'
    _name: str = 'Dual Wielding'

    def __init__(self, user) -> None:
        super().__init__(user)

class Ambush(Ability):
    _passive: bool = True
    _background: str = PATH + 'Ambush.png'
    _name: str = 'Ambush'

    def __init__(self, user) -> None:
        super().__init__(user)

class Protector(Ability):
    _passive: bool = False
    _background: str = PATH + 'Protector.png'
    _name: str = 'Protector'

    def __init__(self, user) -> None:
        super().__init__(user)

class Stoneskin(Ability):
    _passive: bool = True
    _background: str = PATH + 'Stoneskin.png'
    _name: str = 'Stoneskin'

    def __init__(self, user) -> None:
        super().__init__(user)

class Transformation(Ability):
    _passive: bool = False
    _background: str = PATH + 'Transformation.png'
    _name: str = 'Transformation'

    def __init__(self, user) -> None:
        super().__init__(user)


#Item Abilities
class UnlockChest(Ability):
    _passive: bool = False
    _background: str = PATH + 'UnlockChest.png'
    _name: str = 'Unlock Chest'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

class MagicBolt(Ability):
    _passive: bool = False
    _background: str = PATH + 'MagicBolt.png'
    _name: str = 'Magic Bolt +1'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

    def is_usable(self) -> bool:
        return GAME.get_castle().get_stage() in (STAGE_FIGHT_START,STAGE_FIGHT_END) and self._active
    
    def is_passive(self):
        from GameLogic.Items import Item
        if isinstance(self._user,Item):
            return self._user.get_hero().has_ability(MagicalAffinity)
        else:
            return self._user.has_ability(MagicalAffinity)
        
    def use(self):
        from GameLogic.Items import Item
        if isinstance(self._user,Item):
            GAME.get_combat_screen().set_modifier(1,MODIFIER_SCROLL,self._user.get_hero())
            if not self._user.get_hero().has_ability(MagicalAffinity):
                self._user.set_stacks(self._user.get_stacks() - 1)
        else:
            GAME.get_combat_screen().set_modifier(1,MODIFIER_SCROLL,self._user)
        self._active = False
        super().use()

class ThornOfDarkness(Ability):
    _passive: bool = False
    _background: str = PATH + 'ThornOfDarkness.png'
    _name: str = 'Thorn Of Darkness'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

class HealingPortal(Ability):
    _passive: bool = False
    _background: str = PATH + 'HealingPortal.png'
    _name: str = 'Healing Portal'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

class FrostFist(Ability):
    _passive: bool = False
    _background: str = PATH + 'FrostFist.png'
    _name: str = 'Frost Fist +2'
    _hero_card = False

    def __init__(self, user) -> None:
        super().__init__(user)

    def is_usable(self) -> bool:
        return GAME.get_castle().get_stage() in (STAGE_FIGHT_START,STAGE_FIGHT_END) and self._active
    
    def is_passive(self):
        from GameLogic.Items import Item
        if isinstance(self._user,Item):
            return self._user.get_hero().has_ability(MagicalAffinity)
        else:
            return self._user.has_ability(MagicalAffinity)
        
    def use(self):
        from GameLogic.Items import Item
        if isinstance(self._user,Item):
            GAME.get_combat_screen().set_modifier(2,MODIFIER_SCROLL,self._user.get_hero())
            if not self._user.get_hero().has_ability(MagicalAffinity):
                self._user.set_stacks(self._user.get_stacks() - 1)
        else:
            GAME.get_combat_screen().set_modifier(2,MODIFIER_SCROLL,self._user)
        self._active = False
        super().use()