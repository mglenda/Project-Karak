from Interfaces.ActionInterface import ActionInterface

PATH = '_Textures\\Heroes\\Retextured\\'
ICON_PATH = '_Textures\\Heroes\\MyIcons\\'
COMBAT_ICON_PATH = '_Textures\\Heroes\\Combat\\'

class HeroDefinition():
    portrait_path: str
    icon_path: str
    combat_icon_path: str
    default_actions: list[ActionInterface]

class Wizard(HeroDefinition):
    portrait_path: str = PATH + 'Wizard.png'
    icon_path: str = ICON_PATH + 'Wizard.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Wizard.png'
    default_actions: list[ActionInterface] = []

class Warrior(HeroDefinition):
    portrait_path: str = PATH + 'Warrior.png'
    icon_path: str = ICON_PATH + 'Warrior.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Warrior.png'
    default_actions: list[ActionInterface] = []

class Warlock(HeroDefinition):
    portrait_path: str = PATH + 'Warlock.png'
    icon_path: str = ICON_PATH + 'Warlock.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Warlock.png'
    default_actions: list[ActionInterface] = []

class Thief(HeroDefinition):
    portrait_path: str = PATH + 'Thief.png'
    icon_path: str = ICON_PATH + 'Thief.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Thief.png'
    default_actions: list[ActionInterface] = []
        
class Swordsman(HeroDefinition):
    portrait_path: str = PATH + 'Swordsman.png'
    icon_path: str = ICON_PATH + 'Swordsman.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Swordsman.png'
    default_actions: list[ActionInterface] = []

class Ranger(HeroDefinition):
    portrait_path: str = PATH + 'Ranger.png'
    icon_path: str = ICON_PATH + 'Ranger.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Ranger.png'
    default_actions: list[ActionInterface] = []

class Oracle(HeroDefinition):
    portrait_path: str = PATH + 'Oracle.png'
    icon_path: str = ICON_PATH + 'Oracle.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Oracle.png'
    default_actions: list[ActionInterface] = []

class LordOfKarak(HeroDefinition):
    portrait_path: str = PATH + 'LordOfKarak.png'
    icon_path: str = ICON_PATH + 'LordOfKarak.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'LordOfKarak.png'
    default_actions: list[ActionInterface] = []

class BattleMage(HeroDefinition):
    portrait_path: str = PATH + 'BattleMage.png'
    icon_path: str = ICON_PATH + 'BattleMage.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'BattleMage.png'
    default_actions: list[ActionInterface] = []

class Barbarian(HeroDefinition):
    portrait_path: str = PATH + 'Barbarian.png'
    icon_path: str = ICON_PATH + 'Barbarian.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Barbarian.png'
    default_actions: list[ActionInterface] = []

class Acrobat(HeroDefinition):
    portrait_path: str = PATH + 'Acrobat.png'
    icon_path: str = ICON_PATH + 'Acrobat.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Acrobat.png'
    default_actions: list[ActionInterface] = []

class WarriorPrincess(HeroDefinition):
    portrait_path: str = PATH + 'WarriorPrincess.png'
    icon_path: str = ICON_PATH + 'WarriorPrincess.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'WarriorPrincess.png'
    default_actions: list[ActionInterface] = []

class BeastHunter(HeroDefinition):
    portrait_path: str = PATH + 'BeastHunter.png'
    icon_path: str = ICON_PATH + 'BeastHunter.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'BeastHunter.png'
    default_actions: list[ActionInterface] = []

class Alchemist(HeroDefinition):
    portrait_path: str = PATH + 'Alchemist.png'
    icon_path: str = ICON_PATH + 'Alchemist.png'
    combat_icon_path: str = COMBAT_ICON_PATH + 'Alchemist.png'
    default_actions: list[ActionInterface] = []