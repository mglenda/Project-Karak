import pygame
import Tilemap
import Tiles

class Screen():
    def __init__(self):
        self.children = []
        self.SCREEN:pygame.Surface = None
        self.bg_color = (0,0,0)

    def add_child(self,child):
        self.children.append(child)

    def remove_child(self,child):
        for ch in self.children:
            if ch['element'] == child:
                self.children.remove(ch)
                break

    def get_screen(self):
        return self.SCREEN
    
    def get_width(self):
        return self.SCREEN.get_width()
    
    def get_height(self):
        return self.SCREEN.get_height()
    
    def draw(self):
        pygame.draw.rect(self.SCREEN,self.bg_color,(0,0,self.SCREEN.get_width(),self.SCREEN.get_height()))
            
    def add(self,element,x,y):
        self.add_child({
            "element": element
            ,"x": x
            ,"y": y
        })
        element.set_attach_coords(x,y)

    def set_attach_coords(self,x,y):
        self.attach_x = x
        self.attach_y = y

    def get_attach_coords(self):
        return self.attach_x,self.attach_y
        
class MainScreen(Screen):
    def __init__(self):
        super().__init__()
        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.SCREEN = pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()   

        self.castle = CastleScreen(w=self.WIDTH-20,h=self.HEIGHT*0.92)
        self.add(element=self.castle,x=10,y=45)

    def set_fps(self,fps):
        self.clock.tick(fps)

    def get_castle(self):
        return self.castle

    def draw(self):
        super(self.__class__,self).draw()
        for ch in self.children:
            self.SCREEN.blit(ch['element'].get_screen(),(ch['x'],ch['y']))
            ch['element'].draw()

class CastleScreen(Screen):
    def __init__(self,w,h):
        super().__init__()
        self.WIDTH = w
        self.HEIGHT = h
        self.SCREEN = pygame.Surface((w,h)) 
        self.bg_color = (25,25,25)

        self.TILE_SIZE = 150
        self.START_X = w / 2 - self.TILE_SIZE / 2
        self.START_Y = h * 0.4 - self.TILE_SIZE / 2
        self.tilemap = Tilemap.TileMap()
        self.tilemap.tile_create_start(x=self.START_X,y=self.START_Y,w=self.TILE_SIZE,h=self.TILE_SIZE)

    def collides(self,x,y):
        at_x,at_y = self.get_attach_coords()
        x -= at_x
        y -= at_y
        return self.SCREEN.get_rect().collidepoint(x,y)

    def get_tile_size(self):
        return self.TILE_SIZE
    
    def get_start_x(self):
        return self.START_X
    
    def get_start_y(self):
        return self.START_Y
    
    def get_tilemap(self):
        return self.tilemap

    def draw(self):
        super(self.__class__,self).draw()
        t:Tiles.Tile
        for t in self.tilemap.get_tiles():
            t.draw(self.get_screen())
        t = self.tilemap.get_spawned_tile()
        if t is not None:
            t.draw(self.get_screen())

    def mouse_motion(self,x,y):
        t:Tiles.Tile
        at_x,at_y = self.get_attach_coords()
        x -= at_x
        y -= at_y
        for t in self.tilemap.get_tiles():
            if t.collides(x,y):
                t.set_focus(True)
            else:
                t.set_focus(False)

    def get_focused_tile(self):
        t:Tiles.Tile
        for t in self.tilemap.get_tiles():
            if t.is_focused():
                return t
        return None