from GUI.TilePack import TilePack
import GUI.Tiles as Tiles
from GUI.CastleScreen import CastleScreen

class TileMap():
    tiles = {}
    def __init__(self,castle:CastleScreen):
        self.tilepack = TilePack()
        self.castle = castle

    def create_starting_tile(self):
        tile = Tiles.Start(self.castle.get_tile_size(),self.castle.get_tile_size())
        self.castle.add(tile)
        tile.set_abs_point(x=self.castle.get_start_x(),y=self.castle.get_start_y())
        self.store_tile(tile,0,0)
        return tile
    
    def create_tile(self,parent:Tiles.Tile,attach:str):
        c,r = self.get_tile_index(parent)
        x,y,w,h = parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height()
        tile = Tiles.Tile(w,h)
        if attach == 'TOP':
            y = y - h
            r += -1
        elif attach == 'RIGHT':
            x = x + w
            c += 1
        elif attach == 'BOTTOM':
            y = y + h
            r += 1
        elif attach == 'LEFT':
            x = x - w
            c += -1
        tile.set_abs_point(x=x,y=y)
        self.store_tile(tile,c,r)
        self.castle.add(tile)
        return tile
    
    def store_tile(self,tile:Tiles.Tile,c,r):
        self.tiles[str(c)+str(r)] = {'c':c,'r':r,'t':tile}
    
    def get_tile_index(self,tile:Tiles.Tile):
        for _,d in self.tiles.items():
            if d['t'] == tile:
                return d['c'],d['r']
        return None,None
    
    def index_exists(self,c,r):
        return (str(c) + str(r)) in self.tiles
    
    def get_tiles(self):
        return self.tiles