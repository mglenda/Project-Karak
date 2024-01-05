import pygame
from GUI.Frame import Frame

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
        self.set_active(True)

    def _refresh(self):
        self._surface = self._stored
        self._surface = pygame.transform.scale(self._surface,(self._w,self._h))
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface,self._angle)

    def resize(self, w: int, h: int):
        super().resize(w, h)
        self._refresh()

    def rotate(self, angle: int):
        super().rotate(angle)
        self._refresh()
        self.draw()

    def set_texture(self,path: str):
        if path != self._path:
            self._path = path
            self._stored = pygame.image.load(path).convert_alpha()
            self._refresh()