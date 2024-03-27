from Interfaces.Interface import Interface
from GameEngine.PlaceableDefinition import PlaceableDefinition

class PlaceableInterface(Interface):
    definition: PlaceableDefinition
    tile: Interface

    def get_wheel_value(self) -> int:
        pass

    def set_tile(self, tile: Interface):
        pass

    def get_path(self) -> str:
        pass

    def set_definition(self, definition: PlaceableDefinition):
        pass