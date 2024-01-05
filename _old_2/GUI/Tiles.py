import pygame
import GUI.Graphics as Graphics

#Pathing = (TOP,RIGHT,BOTTOM,LEFT)
#Default is (1,1,1,1)
PATH = 'Textures\\Tiles\\Retextured\\'
FOCUS_LAYER = 'FocusedLayer.png'

class Tile(Graphics.GraphicLayout):
    pathing = (1,1,1,1)
    img = 'Background.png'
    revealed = False
    on_mouse_enter = None
    on_mouse_click = None
    def __init__(self,w,h):
        super().__init__(main=Graphics.Background(w=w,h=h,rgb=(255,255,255)))
        self.theme_layer = Graphics.GraphicElement(w=w,h=h,img=PATH + self.img)
        self.focus_layer = Graphics.GraphicElement(w=w,h=h,img=PATH + FOCUS_LAYER)
        self.add(self.theme_layer)
        self.add(self.focus_layer)
        self.focus_layer.set_visible(False)

    def get_width(self):
        return self.get_surf().get_width()
    
    def get_height(self):
        return self.get_surf().get_height()
    
    def get_pathing(self):
        return self.pathing
    
    def is_revealed(self):
        return self.revealed
    
    def is_connectable_top(self):
        return self.pathing[0] == 1
    
    def is_connectable_right(self):
        return self.pathing[1] == 1
    
    def is_connectable_bottom(self):
        return self.pathing[2] == 1
    
    def is_connectable_left(self):
        return self.pathing[3] == 1

    def draw(self):
        super().draw()

    def _on_mouse_click(self, coords: tuple):
        super()._on_mouse_click(coords)
        if self.on_mouse_click is not None:
            self.on_mouse_click(self.on_mouse_click_args)
    
    def _on_mouse_enter(self, coords: tuple):
        if not self.revealed:
            self.focus_layer.set_visible(True)
        super()._on_mouse_enter(coords)
        if self.on_mouse_enter is not None:
            self.on_mouse_enter(self.on_mouse_enter_args)
    
    def _on_mouse_leave(self):
        self.focus_layer.set_visible(False)
        super()._on_mouse_leave()

    def _register_on_mouse_enter_func(self,func,*args):
        self.on_mouse_enter = func
        self.on_mouse_enter_args = args

    def _register_on_mouse_click_func(self,func,*args):
        self.on_mouse_click = func
        self.on_mouse_click_args = args

class Start(Tile):
    img = 'Start.png'
    pathing = (1,1,1,1)
    revealed = True
    def __init__(self,w,h):
        super().__init__(w,h)

class CorridorCorner(Tile):
    img = 'CorridorCorner.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class Arena(Tile):
    img = 'Arena.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class Chamber(Tile):
    img = 'Chamber.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class ChamberCorner(Tile):
    img = 'ChamberCorner.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class ChamberCross(Tile):
    img = 'ChamberCross.png'
    revealed = True
    def __init__(self,w,h):
        super().__init__(w,h)

class ChamberT(Tile):
    img = 'ChamberT.png'
    revealed = True
    pathing = (0,1,1,1)
    def __init__(self,w,h):
        super().__init__(w,h)

class Corridor(Tile):
    img = 'Corridor.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class CorridorCross(Tile):
    img = 'CorridorCross.png'
    revealed = True
    def __init__(self,w,h):
        super().__init__(w,h)

class CorridorT(Tile):
    img = 'CorridorT.png'
    revealed = True
    pathing = (1,0,1,1)
    def __init__(self,w,h):
        super().__init__(w,h)

class Curse(Tile):
    img = 'Curse.png'
    revealed = True
    pathing = (1,1,1,1)
    def __init__(self,w,h):
        super().__init__(w,h)

class Fountain(Tile):
    img = 'Fountain.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)

class Portal(Tile):
    img = 'Portal.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,w,h):
        super().__init__(w,h)