from GUI.TilePack import TilePack
import GUI.Tiles as Tiles

class TileMap():
    def __init__(self):
        self.tilepack = TilePack()

    def create_starting_zone(self,w,h):
        tile = Tiles.Tile(w,h)
        return tile