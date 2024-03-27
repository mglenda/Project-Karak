import pygame

class Texture():
    def __init__(self,w: int,h: int,angle: int,path: str) -> None:
        self.surface: pygame.Surface = pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(),(w,h))
        if angle != 0:
            self.surface = pygame.transform.rotate(self.surface,angle)
        self.w: int = w
        self.h: int = h
        self.angle: int = angle
        self.path: str = path

class ImageBuffer():
    def __init__(self) -> None:
        self.storage: list[Texture] = []

    def get(self,path: str,w: int,h: int,angle: int) -> pygame.Surface:
        for t in self.storage:
            if t.h == round(h,4) and t.w == round(w,4) and t.path == path and t.angle == angle:
                return t.surface.copy()
            
        t = Texture(w=round(w,4),h=round(h,4),path=path,angle=angle)
        self.storage.append(t)
        return t.surface.copy()
    
    def clear(self):
        self.storage.clear()

class TextImage():
    def __init__(self, font_color: tuple, font_size: int, text: str, font_path: str,angle: int, w: int = None, h: int = None) -> None:
        self.surface = pygame.font.Font(font_path,font_size).render(text,False,font_color).convert_alpha()
        if angle != 0:
            self.surface = pygame.transform.rotate(self.surface,angle)
        self.font_color: tuple = font_color
        self.font_size: int = font_size
        self.text: str = text
        self.font_path: str = font_path
        self.angle: int = angle
        self.w: int = self.surface.get_width() if w is None else w
        self.h: int = self.surface.get_height() if h is None else h
        if w is not None or h is not None:
            self.surface = pygame.transform.smoothscale(self.surface,(self.w,self.h))
    
class TextImageBuffer():
    def __init__(self) -> None:
        self.storage: list[TextImage] = []

    def get(self,font_color: tuple, font_size: int, text: str, font_path: str,angle: int,w: int = None, h: int = None) -> pygame.Surface:
        for t in self.storage:
            if t.font_color == font_color and t.font_size == font_size and t.text == text and t.font_path == font_path and t.angle == angle and (w is None or t.w == w) and (h is None or t.h == h):
                return t.surface.copy()
            
        t = TextImage(font_color=font_color,font_size=font_size,text=text,font_path=font_path,angle=angle,w=w,h=h)
        self.storage.append(t)
        return t.surface.copy()
    
    def clear(self):
        self.storage.clear()

class RectTexture():
    def __init__(self,w: int, h: int, color: tuple) -> None:
        self.color = color
        self.w = w
        self.h = h
        self.surface = pygame.Surface((self.w,self.h))
        self.surface.fill(self.color)

class RectBuffer():
    def __init__(self) -> None:
        self.storage: list[RectTexture] = []

    def get(self,w: int,h: int,color: tuple) -> pygame.Surface:
        for t in self.storage:
            if t.h == round(h,4) and t.w == round(w,4) and t.color == color:
                return t.surface.copy()
            
        t = RectTexture(w=round(w,4),h=round(h,4),color=color)
        self.storage.append(t)
        return t.surface.copy()
    
    def clear(self):
        self.storage.clear()