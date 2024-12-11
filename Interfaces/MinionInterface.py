from Interfaces.PlaceableInterface import PlaceableInterface
from GameEngine.MinionDefinition import MinionDefinition
from GameEngine.Duelist import Duelist

class MinionInterface(PlaceableInterface,Duelist):
    definition: MinionDefinition
    agressive: bool

    def get_icon_path(self) -> str:
        pass