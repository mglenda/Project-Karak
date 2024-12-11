from Interfaces.PlaceableInterface import PlaceableInterface
from Interfaces.TileObjectInterface import TileObjectInterface
from GameEngine.PlaceableDefinition import PlaceableDefinition

class Placeable(PlaceableInterface):
    definition: PlaceableDefinition
    tile: TileObjectInterface

    def __init__(self, definition: PlaceableDefinition) -> None:
        self.definition = definition
        self.tile = None

    def set_tile(self, tile: TileObjectInterface):
        if self.tile is not None:
            self.tile.remove_placeable()
        self.tile = tile
        tile.add_placeable(self)

    def get_path(self) -> str:
        return self.definition.path
    
    def set_definition(self, definition: PlaceableDefinition):
        self.definition = definition

    def remove(self):
        if self.tile is not None:
            self.tile.remove_placeable()