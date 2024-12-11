from GameEngine.HeroDefinition import HeroDefinition
from Interfaces.HeroInterface import HeroInterface
from Interfaces.TileObjectInterface import TileObjectInterface
from GameEngine.Inventory import Inventory
from GameEngine.Constants import Constants

class Hero(HeroInterface):
    definition: HeroDefinition
    name: str
    tile: TileObjectInterface
    former_tile: TileObjectInterface
    hit_points: int
    max_hit_points: int
    move_points: int
    max_move_points: int

    inventory: Inventory

    def __init__(self, definition: HeroDefinition, name: str) -> None:
        self.definition = definition
        self.name = name
        self.tile = None
        self.former_tile = None
        self.max_hit_points = getattr(self.definition,'max_hit_points',Constants.HERO_MAX_HP)
        self.max_move_points = getattr(self.definition,'max_move_points',Constants.HERO_MOVEPOINTS)
        self.hit_points = self.max_hit_points
        self.move_points = self.max_move_points
        self.inventory = Inventory(self)
        self.power = 0

    def get_move_points(self) -> int:
        return self.move_points
    
    def get_max_move_points(self) -> int:
        return self.max_move_points
    
    def get_hit_points(self) -> int:
        return self.hit_points
    
    def get_max_hit_points(self) -> int:
        return self.max_hit_points

    def refresh_move_points(self):
        self.move_points = self.max_move_points

    def hurt(self, amnt: int = 1):
        self.hit_points -= amnt
        if self.hit_points < 0:
            self.hit_points = 0

    def heal(self, amnt: int = None):
        if amnt is None:
            self.hit_points = self.max_hit_points
        else:
            self.hit_points = self.max_hit_points if self.hit_points + amnt > self.max_hit_points else self.hit_points + amnt
    
    def move_to_tile(self, tile: TileObjectInterface):
        self.former_tile = self.tile
        if self.tile is not None:
            self.tile.remove_hero(self)
        self.tile = tile
        tile.add_hero(self)
        self.move_points -= 1
    
    def move_to_former_tile(self):
        if self.former_tile is not None:
            if self.tile is not None:
                self.tile.remove_hero(self)
            self.tile = self.former_tile
            self.tile.add_hero(self)
            self.move_points -= 1

    def get_tile(self) -> TileObjectInterface:
        return self.tile

    def get_definition(self) -> HeroDefinition:
        return self.definition
    
    def get_icon_path(self) -> str:
        return self.definition.icon_path
    
    def get_portrait_path(self) -> str:
        return self.definition.portrait_path
    
    def get_combat_icon_path(self) -> str:
        return self.definition.combat_icon_path
    
    def get_name(self) -> str:
        return self.name
    
    def get_weapon_power(self) -> int:
        return self.power + self.inventory.get_power()