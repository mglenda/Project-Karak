import pygame
from GUI.Frame import Frame,FRAMEPOINT
from GameLogic.Placeable import Placeable

FONT_PATH_REGULAR = '_Fonts\\BreatheFireIii-PKLOB.ttf'

class Rect(Frame):
    _color: tuple
    def __init__(self,w: int, h: int, color: tuple, parent: Frame) -> None:
        super().__init__(parent)
        self._color = color
        self.set_w(w)
        self.set_h(h)
        self.refresh()

    def set_color(self, color: tuple) -> bool:
        if self._color != color:
            self._color = color
            self.refresh()
            return True
        return False

    def refresh(self):
        self._surface = pygame.Surface((self._w,self._h))
        self._surface.fill(self._color)
        if self._alpha < 255:
            self._surface.convert_alpha()
            self._surface.set_alpha(self._alpha)

    def get_tilesize(self) -> int:
        pass


class Image(Frame):
    _stored: pygame.Surface
    _path: str
    def __init__(self,w: int,h: int,path: str,parent: Frame) -> None:
        super().__init__(parent)
        self._path = path
        self._stored = pygame.image.load(path).convert_alpha()
        self.set_w(w)
        self.set_h(h)
        self.refresh()

    def refresh(self):
        self._surface = pygame.transform.smoothscale(self._stored,(self._w,self._h))
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface,self._angle)

    def rotate(self,angle: int):
        super().rotate(angle)
        self.refresh()

    def set_texture(self,path: str) -> bool:
        if path != self._path:
            self._path = path
            self._stored = pygame.image.load(path).convert_alpha()
            self.refresh()
            return True
        return False
    
    def set_alpha(self, alpha: int, refresh: bool = True):
        self._stored.set_alpha(alpha)
        return super().set_alpha(alpha, refresh)

class TextField(Frame):
    _font: pygame.font.Font
    _font_color: tuple
    _text: str
    _max_length: int
    _font_size: int
    _stored: pygame.Surface
    _font_path: str
    def __init__(self,parent: Frame,font_color: tuple = (255,215,0),font_size: int = 15,text: str = '',max_length: int = 15,font_path: str = FONT_PATH_REGULAR) -> None:
        super().__init__(parent)
        self._font = pygame.font.Font(font_path,font_size)
        self._font_color = font_color
        self._font_path = font_path
        self._max_length = max_length
        self._font_size = font_size
        self._text = None
        self.set_w(0)
        self.set_h(0)
        self.set_text(text)
        
    def set_text(self,text: str) -> bool:
        if text != self._text:
            if len(text) > self._max_length:
                text = text[:self._max_length]
            self._text = text
            w,h = self.get_w(),self.get_h()
            self.refresh()
            if h != 0:
                self.resize(w,h)
            return True
        return False

    def set_color(self,font_color: tuple) -> bool:
        if self._font_color != font_color:
            self._font_color = font_color
            self.refresh()
            return True
        return False

    def set_font_size(self,font_size:int) -> bool:
        if self._font_size != font_size:
            self._font_size = font_size
            self._font = pygame.font.Font(self._font_path,font_size)
            w,h = self.get_w(),self.get_h()
            self.refresh()
            if h != 0:
                self.resize(w,h)
            return True
        return False
            
    def get_text(self) -> str:
        return self._text
    
    def refresh(self):
        self._stored = self._font.render(self._text,False,self._font_color)
        self._surface = self._stored
        self.set_w(self._surface.get_width())
        self.set_h(self._surface.get_height())
        self._attach()
        if self._alpha < 255:
            self._surface.convert_alpha()
            self._surface.set_alpha(self._alpha)

    def resize(self, w: int, h: int):
        if w != self.get_w() or h != self.get_h():
            ratio = h / self.get_h()
            w = self.get_w() * ratio
            self.set_w(w)
            self.set_h(h)
            self._surface = pygame.transform.scale(self._stored,(self._w,self._h))
            self._attach()
            if self._alpha < 255:
                self._surface.convert_alpha()
                self._surface.set_alpha(self._alpha)

class TileInterface(Image):
    _texture: str
    _pathing: tuple
    _focus_layer: Image
    _press_layer: Image
    _c: int
    _r: int
    def __init__(self, w: int, h: int, path: str, parent: Frame) -> None:
        super().__init__(w, h, path, parent)

    def get_c(self):
        pass
    
    def get_r(self):
        pass
    
    def is_passable_top(self):
        pass
    
    def is_passable_right(self):
        pass
    
    def is_passable_bottom(self):
        pass
    
    def is_passable_left(self):
        pass
    
    def rotate_up(self):
        pass
    
    def rotate_down(self):
        pass

    def add_hero(self, hero):
        pass

    def remove_hero(self, hero):
        pass

    def add_hero(self, hero):
        pass

    def remove_hero(self, hero):
        pass

    def reattach_hero_icons(self):
        pass
                
    def get_icon_size(self) -> int:
        pass

    def add_placeable(self, placeable: Placeable):
        pass

    def get_placeable(self) -> Placeable:
        pass
    
    def remove_placeable(self):
        pass

    def is_placed(self) -> bool:
        pass
    
    def set_placed(self, placed: bool):
        pass

    def is_spawn(self) -> bool:
        pass