from __future__ import annotations

from GameEngine.PlaceableDefinition import PlaceableDefinition
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.TileObject import TileObject

class Placeable:
    definition: PlaceableDefinition
    tile: TileObject

    def __init__(self, definition: PlaceableDefinition) -> None:
        self.definition = definition
        self.tile = None

    def set_tile(self, tile: TileObject):
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
