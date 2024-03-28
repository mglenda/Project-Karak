from GameEngine.HeroDefinition import HeroDefinition
from Interfaces.Interface import Interface
from Interfaces.InventoryInterface import InventoryInterface

class HeroInterface(Interface):
    definition: HeroDefinition
    name: str
    tile: Interface

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

    def get_tile(self) -> Interface:
        pass
    
    def get_definition(self) -> HeroDefinition:
        pass

    def get_icon_path(self) -> str:
        pass
    
    def get_portrait_path(self) -> str:
        pass
    
    def get_name(self) -> str:
        pass