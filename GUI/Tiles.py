import pygame
import GUI.Graphics as Graphics

#Pathing = (TOP,RIGHT,BOTTOM,LEFT)
#Default is (1,1,1,1)
PATH = 'Textures\\Tiles\\Retextured\\'
class Tile(Graphics.GraphicLayout):
    pathing = (1,1,1,1)
    img = 'Background.png'
    def __init__(self,w,h):
        super().__init__(main=Graphics.GraphicElement(w=w,h=h,img=PATH + self.img))

    def draw(self):
        return super().draw()

class Start(Tile):
    img = 'Start.png'
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