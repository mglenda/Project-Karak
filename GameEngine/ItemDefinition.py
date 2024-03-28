from GameEngine.PlaceableDefinition import PlaceableDefinition
from GameEngine.Constants import ItemTypes

PATH = '_Textures\\Items\\Retextured\\'

class ItemDefinition(PlaceableDefinition):
    type: int
    power: int

class Dagger(ItemDefinition):
    type: int = ItemTypes.WEAPON
    power: int = 1
    path: str = PATH + 'Daggers.png'

class Sword(ItemDefinition):
    type: int = ItemTypes.WEAPON
    power: int = 2
    path: str = PATH + 'Sword.png'

class Axe(ItemDefinition):
    type: int = ItemTypes.WEAPON
    power: int = 3
    path: str = PATH + 'Axe.png'

class Key(ItemDefinition):
    type: int = ItemTypes.KEY
    power: int = 0
    path: str = PATH + 'Key.png'

class Chest(ItemDefinition):
    type: int = ItemTypes.CHEST
    power: int = 0
    path: str = PATH + 'ChestOpened.png'

class DragonChest(ItemDefinition):
    type: int = ItemTypes.CHEST
    power: int = 0
    path: str = PATH + 'ChestDragon.png'

class MagicBolt(ItemDefinition):
    type: int = ItemTypes.SCROLL
    power: int = 0
    path: str = PATH + 'MagicBolt.png'

class ThornOfDarkness(ItemDefinition):
    type: int = ItemTypes.SCROLL
    power: int = 0
    path: str = PATH + 'ThornOfDarkness.png'

class HealingPortal(ItemDefinition):
    type: int = ItemTypes.SCROLL
    power: int = 0
    path: str = PATH + 'HealingPortal.png'

class FrostFist(ItemDefinition):
    type: int = ItemTypes.SCROLL
    power: int = 0
    path: str = PATH + 'FrostFist.png'