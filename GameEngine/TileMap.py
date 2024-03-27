from GraphicsEngine.Frame import Frame,FRAMEPOINT
from GameEngine.TileObject import TileObject
from GameEngine.TileDefinitions import TileDefinition,Start,Unknown
from GameEngine.TilePack import TilePack
from Interfaces.TileMapInterface import TileMapInterface
from GraphicsEngine.Constants import MouseEvent
from GameEngine.Constants import Constants

from Game import GAME

class TileMap(TileMapInterface):
    tilesize: int
    world: Frame
    tiles: list[TileObject]
    tilepack: TilePack

    def __init__(self, world: Frame) -> None:
        self.tilesize: int = Constants.DEFAULT_TILESIZE
        self.world = world
        self.tilepack = TilePack()
        self.tiles = [
            TileObject(Start,self.tilesize,self.world,0,0)
        ]
        self.tiles[0].g_tile.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.spawn_unknowns(self.tiles[0])
        self.tiles[0].on_click(GAME.move_to_tile,self.tiles[0])

    def draw_tile_definition(self, start: TileObject, tile: TileObject):
        dfn: TileDefinition = self.tilepack.pick()
        if dfn is not None:
            self.disable_all_tiles()
            tile.set_active(True)
            tile.set_type(dfn)
            tile.on_click(self.confirm_tile_placement,tile)
            tile.g_tile.register_mouse_event(MouseEvent.WHEELUP,self.rotate_tile_up,start,tile)
            tile.g_tile.register_mouse_event(MouseEvent.WHEELDOWN,self.rotate_tile_down,start,tile)

            if not self.is_accessible(start,tile):
                self.rotate_tile_up(start,tile)

    def rotate_tile_up(self, start: TileObject, tile: TileObject):
        tile.rotate_up()
        if not self.is_accessible(start,tile):
            self.rotate_tile_up(start, tile)

    def rotate_tile_down(self, start: TileObject, tile: TileObject):
        tile.rotate_down()
        if not self.is_accessible(start,tile):
            self.rotate_tile_down(start, tile)

    def is_accessible(self, start: TileObject, tile: TileObject) -> bool:
        if self.get_tile_on_top(start) == tile:
            return self.is_passable_top(start) and self.is_passable_bottom(tile)
        elif self.get_tile_on_bottom(start) == tile:
            return self.is_passable_bottom(start) and self.is_passable_top(tile)
        elif self.get_tile_on_left(start) == tile:
            return self.is_passable_left(start) and self.is_passable_right(tile)
        elif self.get_tile_on_right(start) == tile:
            return self.is_passable_right(start) and self.is_passable_left(tile)
        return False

    def confirm_tile_placement(self, tile: TileObject):
        tile.rotate_off()
        tile.set_active(False)
        
        if self.tilepack.get_count() > 0:
            self.spawn_unknowns(tile)
        else:
            self.destory_unknowns()

        GAME.confirm_tile_placement(tile)

    def load_path(self, start: TileObject, movement: int):
        self.disable_all_tiles()
        self.pathfinding(start,movement,start)

    def disable_all_tiles(self):
        for t in self.tiles:
            t.set_active(False)

    def pathfinding(self, start: TileObject, movement: int, root: TileObject):
        if movement > 0:
            if self.is_passable_top(start):
                t = self.get_tile_on_top(start)
                if t is not None and self.is_passable_bottom(t) and t != root:
                    t.set_active(True)
                    if t.get_definition() != Unknown:
                        self.pathfinding(t,movement - 1,root)
                    else:
                        t.on_click(self.draw_tile_definition,start,t)
            if self.is_passable_bottom(start):
                t = self.get_tile_on_bottom(start)
                if t is not None and self.is_passable_top(t) and t != root:
                    t.set_active(True)
                    if t.get_definition() != Unknown:
                        self.pathfinding(t,movement - 1,root)
                    else:
                        t.on_click(self.draw_tile_definition,start,t)
            if self.is_passable_left(start):
                t = self.get_tile_on_left(start)
                if t is not None and self.is_passable_right(t) and t != root:
                    t.set_active(True)
                    if t.get_definition() != Unknown:
                        self.pathfinding(t,movement - 1,root)
                    else:
                        t.on_click(self.draw_tile_definition,start,t)
            if self.is_passable_right(start):
                t = self.get_tile_on_right(start)
                if t is not None and self.is_passable_left(t) and t != root:
                    t.set_active(True)
                    if t.get_definition() != Unknown:
                        self.pathfinding(t,movement - 1,root)
                    else:
                        t.on_click(self.draw_tile_definition,start,t)

    def spawn_unknowns(self, tile: TileObject):
        if tile.get_definition() != Unknown:
            if self.is_passable_top(tile) and self.get_tile_on_top(tile) is None:
                self.place_unknown_tile(tile,tile.row + 1,tile.column).g_tile.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,tile.g_tile)
            if self.is_passable_bottom(tile) and self.get_tile_on_bottom(tile) is None:
                self.place_unknown_tile(tile,tile.row - 1,tile.column).g_tile.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,0,tile.g_tile)
            if self.is_passable_right(tile) and self.get_tile_on_right(tile) is None:
                self.place_unknown_tile(tile,tile.row,tile.column + 1).g_tile.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,0,0,tile.g_tile)
            if self.is_passable_left(tile) and self.get_tile_on_left(tile) is None:
                self.place_unknown_tile(tile,tile.row,tile.column - 1).g_tile.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,0,0,tile.g_tile)

    def place_unknown_tile(self,start: TileObject ,row: int, column: int) -> TileObject:
        t = TileObject(Unknown,self.tilesize,self.world,row,column)
        self.tiles.append(t)
        t.on_click(self.draw_tile_definition,start,t)
        return t
    
    def destory_unknowns(self):
        for t in reversed(self.tiles):
            if t.get_definition() == Unknown:
                t.destroy()
                self.tiles.remove(t)
    
    def is_passable_top(self, tile: TileObject):
        return tile.pathing[0] == 1
    
    def is_passable_right(self, tile: TileObject):
        return tile.pathing[1] == 1
    
    def is_passable_bottom(self, tile: TileObject):
        return tile.pathing[2] == 1
    
    def is_passable_left(self, tile: TileObject):
        return tile.pathing[3] == 1

    def get_tile_on_right(self, tile: TileObject) -> TileObject:
        for t in self.tiles:
            if t.row == tile.row and t.column == tile.column + 1:
                return t
        return None

    def get_tile_on_left(self, tile: TileObject) -> TileObject:
        for t in self.tiles:
            if t.row == tile.row and t.column == tile.column - 1:
                return t
        return None

    def get_tile_on_top(self, tile: TileObject) -> TileObject:
        for t in self.tiles:
            if t.row == tile.row + 1 and t.column == tile.column:
                return t
        return None
    
    def get_tile_on_bottom(self, tile: TileObject) -> TileObject:
        for t in self.tiles:
            if t.row == tile.row - 1 and t.column == tile.column:
                return t
        return None

    def set_tilesize(self, size: int):
        self.tilesize = size

    def get_tilesize(self) -> int:
        return self.tilesize