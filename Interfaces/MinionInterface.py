from Interfaces.Interface import Interface
from GameEngine.MinionDefinition import MinionDefinition
from GameEngine.Duelist import Duelist

class MinionInterface(Duelist,Interface):
    definition: MinionDefinition
    agressive: bool
    explored: bool

    def __init__(self):
        super().__init__()

    def get_icon_path(self) -> str:
        pass

    def is_explored(self) -> bool:
        pass

    def explore(self):
        pass

    def remove(self):
        pass