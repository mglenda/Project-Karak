from GraphicsEngine.Frame import Frame
from core.MemoryEngine import MEMORY_ENGINE

class Image(Frame):
    path: str
    def __init__(self,w: int,h: int,path: str,parent: Frame) -> None:
        super().__init__(parent)
        self.path = path
        self.set_w(w)
        self.set_h(h)
        self.refresh_surface()
        self.refresh_alpha()

    def set_texture(self,path: str):
        if path != self.path:
            self.path = path
            self.refresh_surface()
            self.refresh_alpha()

    def resize(self, factor: float):
        super().resize(factor)
        self.refresh_surface()
        self.refresh_alpha()

    def set_size(self, w: int, h: int):
        super().set_size(w, h)
        self.refresh_surface()
        self.refresh_alpha()

    def refresh_surface(self):
        self.surface = MEMORY_ENGINE.get_img_buffer().get(path=self.path,w=self.w,h=self.h,angle=self.angle)

    def rotate(self, angle: int):
        super().rotate(angle)
        self.refresh_surface()
        self.refresh_alpha()