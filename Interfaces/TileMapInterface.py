from GraphicsEngine.Frame import Frame
from GameEngine.TilePack import TilePack
from Interfaces.TileObjectInterface import TileObjectInterface
from Interfaces.Interface import Interface

class TileMapInterface(Interface):
    tilesize: int
    world: Frame
    tiles: list[TileObjectInterface]
    tilepack: TilePack

    def __init__(self, world: Frame) -> None:
        pass

    def draw_tile_definition(self, tile: TileObjectInterface):
        pass

    def rotate_tile_up(self, start: TileObjectInterface, tile: TileObjectInterface):
        pass

    def rotate_tile_down(self, start: TileObjectInterface, tile: TileObjectInterface):
        pass

    def is_accessible(self, start: TileObjectInterface, tile: TileObjectInterface) -> bool:
        pass

    def confirm_tile_placement(self, tile: TileObjectInterface):
        pass

    def load_path(self, start: TileObjectInterface, movement: int):
        pass

    def pathfinding(self, start: TileObjectInterface, movement: int):
        pass

    def spawn_unknowns(self, tile: TileObjectInterface):
        pass

    def place_unknown_tile(self,row: int, column: int) -> TileObjectInterface:
        pass

    def destory_unknowns(self):
        pass
    
    def is_passable_top(self, tile: TileObjectInterface):
        pass
    
    def is_passable_right(self, tile: TileObjectInterface):
        pass
    
    def is_passable_bottom(self, tile: TileObjectInterface):
        pass
    
    def is_passable_left(self, tile: TileObjectInterface):
        pass

    def get_tile_on_right(self, tile: TileObjectInterface) -> TileObjectInterface:
        pass

    def get_tile_on_left(self, tile: TileObjectInterface) -> TileObjectInterface:
        pass

    def get_tile_on_top(self, tile: TileObjectInterface) -> TileObjectInterface:
        pass
    
    def get_tile_on_bottom(self, tile: TileObjectInterface) -> TileObjectInterface:
        pass

    def set_tilesize(self, size: int):
        pass

    def get_tilesize(self) -> int:
        pass