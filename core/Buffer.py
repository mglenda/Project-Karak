import pygame
import pygame.freetype

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
        if not pygame.freetype.get_init():
            pygame.freetype.init()

        font = pygame.freetype.Font(font_path,font_size)
        font.antialiased = True
        rendered_surface, _ = font.render(text,fgcolor=font_color)
        rendered_surface = rendered_surface.convert_alpha()
        if angle != 0:
            rendered_surface = pygame.transform.rotate(rendered_surface,angle)
        if alpha < 255:
            rendered_surface.set_alpha(alpha)
        self.font_color: tuple = font_color
        self.font_size: int = font_size
        self.text: str = text
        self.font_path: str = font_path
        self.angle: int = angle
        self.w: int = rendered_surface.get_width() if w is None else w
        self.h: int = rendered_surface.get_height() if h is None else h
        self.alpha = alpha
        if w is not None or h is not None:
            self.surface = pygame.Surface((self.w,self.h), pygame.SRCALPHA)
            x = round((self.w - rendered_surface.get_width()) / 2)
            y = round((self.h - rendered_surface.get_height()) / 2)
            self.surface.blit(rendered_surface,(x,y))
            if alpha < 255:
                self.surface.set_alpha(alpha)
        else:
            self.surface = rendered_surface
    
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

class FittedTextImage():
    def __init__(self, font_color: tuple, text: str, font_path: str, angle: int, w: int, h: int, alpha: int = 255, padding: float = 0.92) -> None:
        self.font_color: tuple = font_color
        self.text: str = text
        self.font_path: str = font_path
        self.angle: int = angle
        self.w: int = max(1, round(w))
        self.h: int = max(1, round(h))
        self.alpha: int = alpha
        self.padding: float = padding
        self.surface = pygame.Surface((self.w,self.h), pygame.SRCALPHA)

        if text != "":
            font_size = self._fit_font_size()
            font = pygame.freetype.Font(font_path,font_size)
            font.antialiased = True
            text_surface, _ = font.render(text,fgcolor=font_color)
            text_surface = text_surface.convert_alpha()
            if angle != 0:
                text_surface = pygame.transform.rotate(text_surface,angle)

            x = round((self.surface.get_width() - text_surface.get_width()) / 2)
            y = round((self.surface.get_height() - text_surface.get_height()) / 2)
            self.surface.blit(text_surface,(x,y))

        if alpha < 255:
            self.surface.set_alpha(alpha)

    def _fit_font_size(self) -> int:
        if not pygame.freetype.get_init():
            pygame.freetype.init()

        max_w = max(1,self.w * self.padding)
        max_h = max(1,self.h * self.padding)
        low = 1
        high = max(1,round(self.h * 2))
        best = low

        while low <= high:
            mid = (low + high) // 2
            font = pygame.freetype.Font(self.font_path,mid)
            rect = font.get_rect(self.text)
            if rect.width <= max_w and rect.height <= max_h:
                best = mid
                low = mid + 1
            else:
                high = mid - 1

        return best

class FittedTextImageBuffer():
    def __init__(self) -> None:
        self.storage: list[FittedTextImage] = {}

    def get(self, font_color: tuple, text: str, font_path: str, angle: int, w: int, h: int, alpha: int = 255, padding: float = 0.92) -> pygame.Surface:
        key = (text,font_path,font_color,round(w,4),round(h,4),angle,alpha,padding)
        t: FittedTextImage = None
        try:
            t = self.storage[key]
        except (KeyError):
            t = FittedTextImage(font_color=font_color,text=text,font_path=font_path,angle=angle,w=w,h=h,alpha=alpha,padding=padding)
            self.storage[key] = t
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
