import pygame
from GUI.Frame import Frame,FRAMEPOINT

FONT_PATH = 'Fonts\\BreatheFireIii-PKLOB.ttf'

class Rect(Frame):
    _color: tuple
    def __init__(self,w: int, h: int, color: tuple, parent: Frame) -> None:
        super().__init__(parent)
        self._color = color
        self.set_w(w)
        self.set_h(h)
        self._refresh()

    def set_color(self, color: tuple):
        if self._set_color(color):
            self.draw()

    def _set_color(self, color: tuple) -> bool:
        if self._color != color:
            self._color = color
            self._refresh()
            return True
        return False

    def _refresh(self):
        self._surface = pygame.Surface((self._w,self._h))
        pygame.draw.rect(self._surface,self._color,(0,0,self._w,self._h))


class Image(Frame):
    _stored: pygame.Surface
    _path: str
    def __init__(self,w: int,h: int,path: str,parent: Frame) -> None:
        super().__init__(parent)
        self._path = path
        self._stored = pygame.image.load(path).convert_alpha()
        self.set_w(w)
        self.set_h(h)
        self._refresh()

    def _refresh(self):
        self._surface = self._stored
        self._surface = pygame.transform.scale(self._surface,(self._w,self._h))
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface,self._angle)

    def rotate(self, angle: int):
        self._rotate(angle)
        self.draw()

    def _rotate(self,angle: int):
        super().rotate(angle)
        self._refresh()

    def set_texture(self,path: str):
        if self._set_texture(path):
            self.draw()

    def _set_texture(self,path: str) -> bool:
        if path != self._path:
            self._path = path
            self._stored = pygame.image.load(path).convert_alpha()
            self._refresh()
            return True
        return False

class TextField(Frame):
    _font: pygame.font.Font
    _font_color: tuple
    _text: str
    _max_length: int
    _font_size: int
    def __init__(self,parent: Frame,font_color: tuple = (255,215,0),font_size: int = 15,text: str = '',max_length: int = 15) -> None:
        super().__init__(parent)
        self._font = pygame.font.Font(FONT_PATH,font_size)
        self._font_color = font_color
        self._max_length = max_length
        self._font_size = font_size
        self._text = None
        self.set_w(0)
        self.set_h(0)
        self.set_text(text)
        
    def set_text(self,text: str):
        if self._set_text(text):
            self.draw()

    def _set_text(self,text: str) -> bool:
        if text != self._text:
            if len(text) > self._max_length:
                text = text[:self._max_length]
            self._text = text
            self._refresh()
            return True
        return False

    def set_color(self,font_color: tuple):
        if self._set_color(font_color):
            self.draw()

    def _set_color(self,font_color: tuple) -> bool:
        if self._font_color != font_color:
            self._font_color = font_color
            self._refresh()
            return True
        return False
        
    def set_font_size(self,font_size:int):
        if self._set_font_size(font_size):
            self.draw()

    def _set_font_size(self,font_size:int) -> bool:
        if self._font_size != font_size:
            self._font_size = font_size
            self._font = pygame.font.Font(FONT_PATH,font_size)
            self._refresh()
            return True
        return False
            
    def get_text(self) -> str:
        return self._text
    
    def _refresh(self):
        self._surface = self._font.render(self._text,False,self._font_color)
        self.set_w(self._surface.get_width())
        self.set_h(self._surface.get_height())
        self._attach()

    def _resize(self, w: int, h: int):
        pass

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