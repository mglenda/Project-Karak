import pygame
from GUI.Frame import Frame, FrameInterface
from GUI._ComponentListeners import KeyBoardListener
from Game import GAME

class MainScreen(Frame,KeyBoardListener):
    _entered: FrameInterface
    def __init__(self) -> None:
        super().__init__(None)
        self.set_x(0)
        self.set_y(0)
        self.set_w(pygame.display.Info().current_w)
        self.set_h(pygame.display.Info().current_h)
        self._surface = pygame.display.set_mode((self._w,self._h),pygame.FULLSCREEN)
        self.set_visible(True)
        self.set_active(True)
        self._entered = None

    def draw(self):
        pygame.draw.rect(self._surface,(0,0,0),(0,0,self._w,self._h))
        c:Frame
        for c in self.get_children():
            if c.is_visible() and c.get_x() is not None and c.get_y() is not None:
                self._surface.blit(c.get_surface(),(c.get_x(),c.get_y()))

    def add(self, component: FrameInterface):
        return super().add(component)

    def is_active(self) -> bool:
        return self._active
    
    def is_visible(self) -> bool:
        return self._visible
    
    def _on_mouse_motion(self, x, y) -> bool:
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                if self._entered != e:
                    if self._entered is not None and self._entered.is_active():
                        self._entered._on_mouse_leave()
                    self._entered = e
                    e._on_mouse_enter()
                    break
        if self._entered is not None and not self._entered.collide(x,y) and self._entered.is_active():
            self._entered._on_mouse_leave()
            self._entered = None
    
    def _on_mouse_left_click(self, x, y):
        super()._on_mouse_left_click(x, y)

    def _on_mouse_right_click(self, x, y):
        super()._on_mouse_right_click(x, y)