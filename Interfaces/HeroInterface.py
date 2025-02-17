from GameEngine.HeroDefinition import HeroDefinition
from Interfaces.Interface import Interface
from Interfaces.ActionInterface import ActionInterface
from Interfaces.InventoryInterface import InventoryInterface
from GameEngine.Duelist import Duelist

class HeroInterface(Interface,Duelist):
    definition: HeroDefinition
    name: str
    tile: Interface
    former_tile: Interface
    hit_points: int
    max_hit_points: int
    move_points: int
    max_move_points: int
    actions: list[ActionInterface]

    inventory: InventoryInterface

    def __init__(self, definition: HeroDefinition, name: str) -> None:
        pass

    def get_move_points(self) -> int:
        pass
    
    def get_max_move_points(self) -> int:
        pass
    
    def get_hit_points(self) -> int:
        pass
    
    def get_max_hit_points(self) -> int:
        pass

    def refresh_move_points(self):
        pass

    def hurt(self, amnt: int = 1):
        pass

    def heal(self, amnt: int = None):
        pass

    def move_to_tile(self, tile: Interface):
        pass

    def move_to_former_tile(self):
        pass

    def get_tile(self) -> Interface:
        pass
    
    def get_definition(self) -> HeroDefinition:
        pass

    def get_icon_path(self) -> str:
        pass

    def get_combat_icon_path(self) -> str:
        pass
    
    def get_portrait_path(self) -> str:
        pass
    
    def get_name(self) -> str:
        pass

    def get_available_actions(self) -> list[ActionInterface]:
        pass

    def is_in_hostile_tile(self) -> bool:
        pass