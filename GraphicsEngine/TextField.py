from GraphicsEngine.Frame import Frame
from core.MemoryEngine import MEMORY_ENGINE

FONT_PATH_REGULAR = '_Fonts\\BreatheFireIii-PKLOB.ttf'

class TextField(Frame):
    def __init__(self,parent: Frame,font_color: tuple = (255,215,0),font_size: int = 15,text: str = '',font_path: str = FONT_PATH_REGULAR) -> None:
        super().__init__(parent)

        self.font_color = font_color
        self.font_size = font_size
        self.text = text
        self.font_path = font_path
        self.refresh_surface()

    def set_text(self,text: str):
        self.text = text
        self.refresh_surface(w=self.w,h=self.h)

    def set_color(self,font_color: tuple):
        self.font_color = font_color
        self.refresh_surface(w=self.w,h=self.h)

    def set_font_size(self,font_size:int):
        self.font_size = font_size
        self.refresh_surface()
            
    def get_text(self) -> str:
        return self.text
    
    def resize(self, factor: float):
        super().resize(factor)
        self.refresh_surface(w=self.w,h=self.h)

    def set_size(self, w: int, h: int):
        super().set_size(w, h)
        self.refresh_surface(w=self.w,h=self.h)

    def refresh_surface(self,w: int = None,h: int = None):
        self.surface = MEMORY_ENGINE.get_txt_buffer().get(font_color=self.font_color,font_size=self.font_size,text=self.text,font_path=self.font_path,angle=self.angle,w=w,h=h,alpha=self.alpha)
        self.w = self.surface.get_width() if w is None else w
        self.h = self.surface.get_height() if h is None else h

    def rotate(self, angle: int):
        super().rotate(angle)
        self.refresh_surface()