from GameEngine.MinionDefinition import MinionDefinition
from GameEngine.Duelist import Duelist
from GameEngine.Placeable import Placeable
from GameEngine.Item import Item

class Minion(Placeable, Duelist):
    definition: MinionDefinition
    agressive: bool
    explored: bool

    def __init__(self, definition: MinionDefinition, explored: bool = False) -> None:
        Placeable.__init__(self,definition)
        Duelist.__init__(self)

        self.power = definition.power
        self.agressive = definition.agressive
        self.explored = explored

    def get_wheel_value(self) -> int:
        if self.agressive:
            return self.power
        return None
    
    def set_definition(self, definition: MinionDefinition):
        super().set_definition(definition)

        self.power = definition.power
        self.agressive = definition.agressive

    def get_icon_path(self) -> str:
        return self.definition.path
    
    def get_combat_icon_path(self) -> str:
        return self.definition.path
    
    def remove(self, drop_reward: bool = True):
        Placeable.remove(self)
        if drop_reward:
            self.tile.add_placeable(Item(self.definition.reward))

    def is_explored(self) -> bool:
        return self.explored
    
    def explore(self):
        self.explored = True
