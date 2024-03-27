from GraphicsEngine.Tile import Tile,Frame,Image
from GraphicsEngine.Constants import MouseEvent
from GameEngine.TileDefinitions import TileDefinition
from Interfaces.Interface import Interface
from Interfaces.PlaceableInterface import PlaceableInterface

class TileObjectInterface(Interface):
    g_tile: Tile
    pathing: tuple
    path: str
    definition: TileDefinition
    is_spawn: bool
    column: int
    row: int

    heroes: list[Interface]
    hero_icons: list[Image]
    placeable: PlaceableInterface

    def __init__(self, definition: TileDefinition, size: int, world: Frame,row: int, column: int) -> None:
        pass

    def add_placeable(self, placeable: PlaceableInterface):
        pass

    def remove_placeable(self):
        pass

    def get_placeable(self) -> PlaceableInterface:
        pass

    def add_hero(self, hero: Interface):
        pass

    def remove_hero(self, hero: Interface):
        pass

    def graphics_refresh_heroes(self):
        pass

    def graphics_get_hero_icon_size(self) -> int:
        pass

    def set_type(self, definition: TileDefinition):
        pass

    def get_definition(self) -> TileDefinition:
        pass
    
    def set_active(self, active: bool):
        pass

    def on_click(self,func,*args):
        pass

    def rotate_off(self):
        pass

    def clear_mouse_events(self):
        pass
    
    def rotate_up(self):
        pass
    
    def rotate_down(self):
        pass

    def destroy(self):
        pass