from GUI.MainScreen import MainScreen
from GUI.CastleScreen import CastleScreen
from GUI.TileMap import TileMap
from GUI.Tiles import Tile

class Game():
    def __init__(self):
        self.main_screen = MainScreen()
        self.castle = CastleScreen(w=self.main_screen.surf.get_width()
                                   ,h=self.main_screen.surf.get_height())
        self.main_screen.add(cont=self.castle,x=10,y=45)
        self.tilemap = TileMap(self.castle)

        self.register_tile(self.tilemap.create_starting_tile())
        print(len(self.castle.layouts))
        
    def register_tile(self,tile:Tile):
        c,r = self.tilemap.get_tile_index(tile)
        # check sides:
        if not self.tilemap.index_exists(c,r-1) and tile.is_revealed() and tile.is_connectable_top():
            self.tilemap.create_tile(tile,'TOP')
        if not self.tilemap.index_exists(c+1,r) and tile.is_revealed() and tile.is_connectable_right():
            self.tilemap.create_tile(tile,'RIGHT')
        if not self.tilemap.index_exists(c,r+1) and tile.is_revealed() and tile.is_connectable_bottom():
            self.tilemap.create_tile(tile,'BOTTOM')
        if not self.tilemap.index_exists(c-1,r) and tile.is_revealed() and tile.is_connectable_left():
            self.tilemap.create_tile(tile,'LEFT')
        self.register_tile_events(tile)

    def register_tile_events(self,tile:Tile):
        tile._register_on_mouse_enter_func(self.on_tile_enter,self,tile)
        tile._register_on_mouse_click_func(self.on_tile_click,self,tile)

    def on_tile_enter(self,tile:Tile):
        print(tile)

    def on_tile_click(self,tile:Tile):
        print(tile)

    def on_mouse_motion(self,coords:tuple):
        self.main_screen._on_mouse_motion(coords)

    def on_mouse_click(self,coords:tuple):
        self.main_screen._on_mouse_click(coords)

    def draw(self):
        self.main_screen.draw()