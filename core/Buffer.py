import pygame

class Texture():
    def __init__(self,w: int,h: int,angle: int,path: str, alpha: int = 255) -> None:
        self.surface: pygame.Surface = pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(),(w,h))
        if angle != 0:
            self.surface = pygame.transform.rotate(self.surface,angle)
        if alpha < 255:
            self.surface.set_alpha(alpha)
        self.alpha = alpha
        self.w: int = w
        self.h: int = h
        self.angle: int = angle
        self.path: str = path

class ImageBuffer():
    def __init__(self) -> None:
        self.storage: list[Texture] = {}

    def get(self,path: str,w: int,h: int,angle: int, alpha: int = 255) -> pygame.Surface:
        t: Texture = None
        try:
            t = self.storage[(path,round(h,4),round(w,4),angle,alpha)]
        except (KeyError):
            t = Texture(w=round(w,4),h=round(h,4),path=path,angle=angle,alpha=alpha)
            self.storage[(path,round(h,4),round(w,4),angle,alpha)] = t
        return t.surface
    
    def clear(self):
        self.storage.clear()

class TextImage():
    def __init__(self, font_color: tuple, font_size: int, text: str, font_path: str,angle: int, w: int = None, h: int = None, alpha: int = 255) -> None:
        self.surface = pygame.font.Font(font_path,font_size).render(text,False,font_color).convert_alpha()
        if angle != 0:
            self.surface = pygame.transform.rotate(self.surface,angle)
        if alpha < 255:
            self.surface.set_alpha(alpha)
        self.font_color: tuple = font_color
        self.font_size: int = font_size
        self.text: str = text
        self.font_path: str = font_path
        self.angle: int = angle
        self.w: int = self.surface.get_width() if w is None else w
        self.h: int = self.surface.get_height() if h is None else h
        self.alpha = alpha
        if w is not None or h is not None:
            self.surface = pygame.transform.smoothscale(self.surface,(self.w,self.h))
    
class TextImageBuffer():
    def __init__(self) -> None:
        self.storage: list[TextImage] = {}
        
    def get(self,font_color: tuple, font_size: int, text: str, font_path: str,angle: int,w: int = None, h: int = None, alpha:int = 255) -> pygame.Surface:
        t: TextImage = None
        try:
            t = self.storage[(text,font_path,font_color,w,h,font_size,angle,alpha)]
        except (KeyError):
            t = TextImage(font_color=font_color,font_size=font_size,text=text,font_path=font_path,angle=angle,w=w,h=h,alpha=alpha)
            self.storage[(text,font_path,font_color,w,h,font_size,angle,alpha)] = t
        return t.surface
    
    def clear(self):
        self.storage.clear()

class RectTexture():
    def __init__(self,w: int, h: int, color: tuple,alpha: int = 255) -> None:
        self.color = color
        self.w = w
        self.h = h
        self.surface = pygame.Surface((self.w,self.h))
        self.surface.fill(self.color)
        self.alpha = alpha
        if alpha < 255:
            self.surface.set_alpha(alpha)

class RectBuffer():
    def __init__(self) -> None:
        self.storage: list[RectTexture] = {}

    def get(self,w: int,h: int,color: tuple, alpha: int = 255) -> pygame.Surface:
        t: RectTexture = None
        try:
            t = self.storage[(color,round(h,4),round(w,4),alpha)]
        except (KeyError):
            t = RectTexture(w=round(w,4),h=round(h,4),color=color,alpha=alpha)
            self.storage[(color,round(h,4),round(w,4),alpha)] = t
        return t.surface
    
    def clear(self):
        self.storage.clear()