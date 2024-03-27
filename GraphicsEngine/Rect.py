from GraphicsEngine.Frame import Frame
from core.MemoryEngine import MEMORY_ENGINE
import pygame

class Rect(Frame):
    color: tuple
    def __init__(self,w: int, h: int, color: tuple, parent: Frame) -> None:
        super().__init__(parent)
        self.set_w(w)
        self.set_h(h)
        self.color = color
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
        self.surface = MEMORY_ENGINE.get_rect_buffer().get(self.w,self.h,self.color)