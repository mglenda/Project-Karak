import pygame

TILEPATH = 'Textures\\Tiles\\Retextured\\'
MIN_TILE_SIZE = 25
MAX_TILE_SIZE = 300
#Pathing = (TOP,RIGHT,BOTTOM,LEFT)
#Default is (1,1,1,1)
class Tile():
    texture = 'Background.png'
    texture_focused = 'FocusedLayer.png'
    pathing = (1,1,1,1)
    revealed = False
    focused = False
    angle = 0
    parent = None
    attach = None

    def __init__(self,x,y,w,h):
        self.width = w
        self.height = h
        self.x,self.y = x,y
        self.def_img = pygame.image.load(TILEPATH + self.texture).convert_alpha()
        self.def_focus_layer = pygame.image.load(TILEPATH + self.texture_focused).convert_alpha()
        self.textures_reload()

    def resize(self,w,h):
        self.width = self.width + w if self.width + w > MIN_TILE_SIZE and self.width + w < MAX_TILE_SIZE else self.width
        self.height = self.height + h if self.height + h > MIN_TILE_SIZE and self.height + h < MAX_TILE_SIZE else self.height
        
        self.textures_reload()

    def reattach(self):
        if self.parent is not None and self.attach is not None:
            if self.attach == 'TOP':
                self.y = self.parent.get_y() - self.parent.get_height()
                self.x = self.parent.get_x()
            elif self.attach == 'RIGHT':
                self.x = self.parent.get_x() + self.parent.get_width()
                self.y = self.parent.get_y()
            elif self.attach == 'BOTTOM':
                self.y = self.parent.get_y() + self.parent.get_height()
                self.x = self.parent.get_x()
            elif self.attach == 'LEFT':
                self.x = self.parent.get_x() - self.parent.get_width()
                self.y = self.parent.get_y()
    
    def textures_reload(self):
        self.img = self.def_img
        self.img = pygame.transform.scale(self.img,(self.width,self.height))
        self.focus_layer = self.def_focus_layer
        self.focus_layer = pygame.transform.scale(self.focus_layer,(self.width,self.height))
        self.img = pygame.transform.rotate(self.img,self.angle)
        self.focus_layer = pygame.transform.rotate(self.focus_layer,self.angle)

    def set_parent(self,parent):
        self.parent = parent

    def set_attach(self,attach):
        self.attach = attach

    def get_parent(self):
        return self.parent
    
    def get_attach(self):
        return self.attach

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y
    
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

    def rotate_up(self):
        self.pathing = (
            self.pathing[1]
            ,self.pathing[2]
            ,self.pathing[3]
            ,self.pathing[0]
        )
        self.img = pygame.transform.rotate(self.img,90)
        self.focus_layer = pygame.transform.rotate(self.focus_layer,90)
        self.angle = self.angle + 90 if self.angle < 360 else 0
    
    def rotate_down(self):
        self.pathing = (
            self.pathing[3]
            ,self.pathing[0]
            ,self.pathing[1]
            ,self.pathing[2]
        )
        self.img = pygame.transform.rotate(self.img,-90)
        self.focus_layer = pygame.transform.rotate(self.focus_layer,-90)
        self.angle = self.angle - 90 if self.angle > 0 else 270

    def collides(self,x,y):
        return self.x <= x and self.y <= y and self.x + self.width >= x and self.y + self.height >= y

    def set_focus(self,bool):
        self.focused = bool

    def get_pathing(self):
        return self.pathing
    
    def is_focused(self):
        return self.focused
    
    def get_img(self):
        return self.img
    
    def get_focus_layer(self):
        return self.focus_layer
    
    def on_click(self):
        pass

    def draw(self,screen:pygame.Surface):
        screen.blit(self.get_img(),(self.get_x(),self.get_y()))
        if self.is_focused():
            screen.blit(self.get_focus_layer(),(self.get_x(),self.get_y()))
        
class Start(Tile):
    texture = 'Start.png'
    texture_focused = 'Start.png'
    revealed = True
    def __init__(self,x,y,w,h):
        super().__init__(x,y,w,h)

class CorridorCorner(Tile):
    texture = 'CorridorCorner.png'
    texture_focused = 'CorridorCorner.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Arena(Tile):
    texture = 'Arena.png'
    texture_focused = 'Arena.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Chamber(Tile):
    texture = 'Chamber.png'
    texture_focused = 'Chamber.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class ChamberCorner(Tile):
    texture = 'ChamberCorner.png'
    texture_focused = 'ChamberCorner.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class ChamberCross(Tile):
    texture = 'ChamberCross.png'
    texture_focused = 'ChamberCross.png'
    revealed = True
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class ChamberT(Tile):
    texture = 'ChamberT.png'
    texture_focused = 'ChamberT.png'
    revealed = True
    pathing = (0,1,1,1)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Corridor(Tile):
    texture = 'Corridor.png'
    texture_focused = 'Corridor.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class CorridorCross(Tile):
    texture = 'CorridorCross.png'
    texture_focused = 'CorridorCross.png'
    revealed = True
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class CorridorT(Tile):
    texture = 'CorridorT.png'
    texture_focused = 'CorridorT.png'
    revealed = True
    pathing = (1,0,1,1)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Curse(Tile):
    texture = 'Curse.png'
    texture_focused = 'Curse.png'
    revealed = True
    pathing = (1,1,1,1)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Fountain(Tile):
    texture = 'Fountain.png'
    texture_focused = 'Fountain.png'
    revealed = True
    pathing = (0,1,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())

class Portal(Tile):
    texture = 'Portal.png'
    texture_focused = 'Portal.png'
    revealed = True
    pathing = (1,0,1,0)
    def __init__(self,parent:Tile):
        super().__init__(parent.get_x(),parent.get_y(),parent.get_width(),parent.get_height())
        self.set_parent(parent.get_parent())
        self.set_attach(parent.get_attach())