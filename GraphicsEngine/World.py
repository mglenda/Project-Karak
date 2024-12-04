from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.Image import Image
from GameEngine.TileMap import TileMap

ZOOM_MAX = 9
ZOOM_MIN = -2

class World(Rect):
    start_tile: Image
    motion_x: int
    motion_y: int
    center_x: int
    center_y: int
    zoom: float
    is_motion: bool
    tilemap: TileMap

    def __init__(self, parent: Frame):
        super().__init__(parent.get_w(),parent.get_h(),(0,0,0),parent)
        self.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.motion_x = 0
        self.motion_y = 0
        self.is_motion = False
        self.zoom = 0
        self.set_active(True)

        self.tilemap = TileMap(self)

        self.center_x = parent.get_w() / 2
        self.center_y = parent.get_h() / 2

    def get_tilemap(self) -> TileMap:
        return self.tilemap

    def on_mouse_motion(self, x, y):
        if self.is_motion:
            self.tilemap.tiles[0].g_tile.move(x - self.motion_x,y - self.motion_y)
            self.motion_x = x
            self.motion_y = y

    def on_mouse_left_press(self, x, y):
        self.motion_x = x
        self.motion_y = y
        self.is_motion = True

    def on_mouse_left_click(self, x, y):
        self.is_motion = False

    def on_mouse_leave(self):
        self.is_motion = False

    def on_mouse_wheel_down(self, x, y):
        if self.zoom > ZOOM_MIN:
            self.zoom -= 1
            val = -10
            size_fac = ((self.tilemap.get_tilesize() + val) / self.tilemap.get_tilesize()) - 1
            dist_x = (self.tilemap.tiles[0].g_tile.get_x() - (self.center_x - self.tilemap.get_tilesize() /2))
            dist_y = (self.tilemap.tiles[0].g_tile.get_y() - (self.center_y - self.tilemap.get_tilesize() /2))

            self.tilemap.set_tilesize(self.tilemap.get_tilesize() + val)
            for c in self.children:
                c.set_size(self.tilemap.get_tilesize(),self.tilemap.get_tilesize())
            
            for c in self.get_abs_att_children():
                c.attach()

            self.tilemap.tiles[0].g_tile.move(dist_x * size_fac,dist_y * size_fac)
    
    def on_mouse_wheel_up(self, x, y):
        if self.zoom < ZOOM_MAX:
            self.zoom += 1
            val = 10
            size_fac = ((self.tilemap.get_tilesize() + val) / self.tilemap.get_tilesize()) - 1
            dist_x = (self.tilemap.tiles[0].g_tile.get_x() - (self.center_x - self.tilemap.get_tilesize() / 2))
            dist_y = (self.tilemap.tiles[0].g_tile.get_y() - (self.center_y - self.tilemap.get_tilesize() / 2))

            self.tilemap.set_tilesize(self.tilemap.get_tilesize() + val)
            for c in self.children:
                c.set_size(self.tilemap.get_tilesize(),self.tilemap.get_tilesize())
            
            for c in self.get_abs_att_children():
                c.attach()

            self.tilemap.tiles[0].g_tile.move(dist_x * size_fac,dist_y * size_fac)
