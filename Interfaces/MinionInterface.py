from Interfaces.PlaceableInterface import PlaceableInterface
from GameEngine.MinionDefinition import MinionDefinition
from GameEngine.Duelist import Duelist

class MinionInterface(PlaceableInterface,Duelist):
    definition: MinionDefinition
    power: int
    agressive: bool