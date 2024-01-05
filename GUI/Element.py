import pygame
from GUI._ComponentListeners import MouseListener

class Element(MouseListener):
    _x: int
    _y: int
    _w: int
    _h: int
    _angle: int
    _surface = pygame.Surface
    _active: bool
    _visible: bool
    _x_offset: int
    _y_offset: int
    def __init__(self) -> None:
        self._visible = False
        self._active = False
        self._angle = 0
        self._x = None
        self._y = None
        self._surface = None
        self._x_offset = 0
        self._y_offset = 0
        self._w = 0
        self._h = 0

    def set_xy(self,x: int,y: int):
        self._x = x
        self._y = y

    def get_x(self) -> int:
        if self._x is not None:
            return self._x + self._x_offset
        else:
            return None
    
    def get_y(self) -> int:
        if self._y is not None:
            return self._y + self._y_offset
        else:
            return None
    
    def set_x(self,x: int):
        self._x = x

    def set_y(self,y: int):
        self._y = y

    def get_w(self) -> int:
        return self._w
    
    def get_h(self) -> int:
        return self._h
    
    def set_w(self,w: int):
        self._w = w

    def set_h(self,h: int):
        self._h = h

    def get_surface(self) -> pygame.Surface:
        return self._surface

    def draw(self):
        pass

    def set_active(self,active: bool):
        self._active = active

    def is_active(self) -> bool:
        return self._active
    
    def set_visible(self,visible: bool):
        if visible != self._visible:
            self._visible = visible
            self.draw()

    def is_visible(self) -> bool:
        return self._visible
    
    def rotate(self,angle: int):
        self._angle += angle
        if self._angle >= 360 or self._angle < 0:
            self._angle = self._angle % 360

    def set_x_offset(self,x_offset: int):
        self._x_offset = x_offset

    def get_x_offset(self) -> int:
        return self._x_offset
    
    def set_y_offset(self,y_offset: int):
        self._y_offset = y_offset

    def get_y_offset(self) -> int:
        return self._y_offset
    
    def collide(self,x: int,y: int) -> bool:
        return x >= self.get_x() and x <= self.get_x() + self.get_w() and y >= self.get_y() and y <= self.get_y() + self.get_h() and self.is_visible()