import random
import Tiles

class TilePack():
    def __init__(self):
        self.pack = []
        for i in range(4):
            self.pack.append(Tiles.CorridorCorner)
        for i in range(6):
            self.pack.append(Tiles.Arena)
        for i in range(4):
            self.pack.append(Tiles.Portal)
        for i in range(2):
            self.pack.append(Tiles.Fountain)
        for i in range(5):
            self.pack.append(Tiles.CorridorT)
        for i in range(7):
            self.pack.append(Tiles.CorridorCross)
        for i in range(16):
            self.pack.append(Tiles.ChamberCross)
        for i in range(17):
            self.pack.append(Tiles.ChamberT)
        for i in range(15):
            self.pack.append(Tiles.ChamberCorner)
        for i in range(13):
            self.pack.append(Tiles.Chamber)
        for i in range(4):
            self.pack.append(Tiles.Curse)
        random.shuffle(self.pack)

    def pick(self):
        if len(self.pack) > 0:
            return self.pack.pop()
        return None

class TileMap():
    def __init__(self):
        self.tilepack = TilePack()
        self.tiles = []
        self.tilemap = {}

    def get_tiles(self):
        return self.tiles
    
    def get_tilepack(self):
        return self.tilepack
    
    def tile_create_start(self,x,y,w,h):
        self.tile_register(Tiles.Start(x,y,w,h),0,0)
             
    def tile_create(self,parent:Tiles.Tile,attach):
        c,r = self.tilemap_get_index(parent)
        x,y,w,h = parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height()
        if attach == 'TOP':
            y = parent.get_y() - parent.get_height()
            r += -1
        elif attach == 'RIGHT':
            x = parent.get_x() + parent.get_width()
            c += 1
        elif attach == 'BOTTOM':
            y = parent.get_y() + parent.get_height()
            r += 1
        elif attach == 'LEFT':
            x = parent.get_x() - parent.get_width()
            c += -1
        tile = Tiles.Tile(x,y,w,h)
        tile.set_parent(parent)
        tile.set_attach(attach)
        self.tile_register(tile,c,r)

    def tile_register(self,tile:Tiles.Tile,c,r):
        self.tiles.append(tile)
        self.tilemap[str(c)+str(r)] = {'c':c,'r':r,'t':tile}
        # check sides:
        if (str(c) + str(r-1)) not in self.tilemap and tile.is_revealed() and tile.is_connectable_top():
            self.tile_create(tile,'TOP')
        if (str(c+1) + str(r)) not in self.tilemap and tile.is_revealed() and tile.is_connectable_right():
            self.tile_create(tile,'RIGHT')
        if (str(c) + str(r+1)) not in self.tilemap and tile.is_revealed() and tile.is_connectable_bottom():
            self.tile_create(tile,'BOTTOM')
        if (str(c-1) + str(r)) not in self.tilemap and tile.is_revealed() and tile.is_connectable_left():
            self.tile_create(tile,'LEFT')

    def tilemap_get_index(self,t:Tiles.Tile):
        for _,d in self.tilemap.items():
            if d['t'] == t:
                return d['c'],d['r']
        return None,None
    
    def tile_spawn(self,parent=Tiles.Tile):
        t:Tiles.Tile = self.tilepack.pick()
        if t is not None:
            self.spawned_tile = t(parent)
            self.tile_former = parent

    def get_spawned_tile(self) -> Tiles.Tile:
        if hasattr(self,'spawned_tile'):
            return self.spawned_tile
        else:
            return None
        
    def tile_spawn_confirm(self):
        c,r = self.tilemap_get_index(self.tile_former)
        self.tiles.remove(self.tile_former)
        del self.tile_former
        self.tile_register(self.spawned_tile,c,r)
        del self.spawned_tile
    
    def move(self,x,y):
        t:Tiles.Tile
        for t in self.tiles:
            t.set_x(t.get_x()+x)
            t.set_y(t.get_y()+y)
        if hasattr(self,'spawned_tile') and self.spawned_tile is not None:
            t = self.spawned_tile
            t.set_x(t.get_x()+x)
            t.set_y(t.get_y()+y)

    def resize(self,w,h):
        t:Tiles.Tile
        for t in self.tiles:
            t.resize(w,h)
        for t in self.tiles:
            t.reattach()
        if hasattr(self,'spawned_tile') and self.spawned_tile is not None:
            t = self.spawned_tile
            t.resize(w,h)