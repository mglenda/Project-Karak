import pygame
from GUI.Frame import Frame, FrameInterface
from GUI._ComponentListeners import KeyBoardListener

class MainScreen(Frame,KeyBoardListener):
    _entered: FrameInterface
    _focused: KeyBoardListener
    def __init__(self) -> None:
        self._is_draw_called = 0
        super().__init__(None)
        self.set_x(0)
        self.set_y(0)
        self.set_w(pygame.display.Info().current_w)
        self.set_h(pygame.display.Info().current_h)
        self._surface = pygame.display.set_mode((self._w,self._h),pygame.FULLSCREEN)
        self.set_visible(True)
        self.set_active(True)
        self._entered = None
        self._focused = None

    def draw(self):
        self._surface.fill((40,40,40))
        blits = self.get_blits_children()
        self._surface.blits(blits)
        pygame.display.update()

    def add(self, component: FrameInterface):
        return super().add(component)
    
    def _on_mouse_motion(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                if self._entered != e:
                    if self._entered is not None and self._entered.is_active():
                        self._entered._on_mouse_leave()
                    self._entered = e
                    e._on_mouse_enter()
                e._on_mouse_motion(x,y)
                return
        if self._entered is not None and not self._entered.collide(x,y) and self._entered.is_active():
            self._entered._on_mouse_leave()
            self._entered = None

    def set_focus(self, focused: KeyBoardListener):
        if self._focused != focused:
            if self._focused is not None:
                self._focused.set_focus(False)
            if focused is not None:
                focused.set_focus(True)
            self._focused = focused
    
    def _on_mouse_left_click(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_left_click(x,y)
                if isinstance(e,KeyBoardListener):
                    self.set_focus(e)
                return
        self.set_focus(None)
        super()._on_mouse_left_click(x, y)

    def _on_mouse_left_press(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_left_press(x,y)
                return
        super()._on_mouse_left_press(x, y)
    
    def _on_mouse_right_click(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_right_click(x,y)
                return
        super()._on_mouse_right_click(x, y)
    
    def _on_mouse_right_press(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_right_press(x,y)
                return
        super()._on_mouse_right_press(x, y)
    
    def _on_mouse_wheel_click(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_wheel_click(x,y)
                return
        super()._on_mouse_wheel_click(x, y)
    
    def _on_mouse_wheel_press(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_wheel_press(x,y)
                return
        super()._on_mouse_wheel_press(x, y)
    
    def _on_mouse_wheel_down(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_wheel_down(x,y)
                return
        super()._on_mouse_wheel_down(x, y)
    
    def _on_mouse_wheel_up(self, x, y):
        e:FrameInterface
        for e in reversed(self.get_children()):
            if e.is_active() and e.collide(x,y):
                e._on_mouse_wheel_up(x,y)
                return
        super()._on_mouse_wheel_up(x, y)

    def _on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        if self._focused is not None:
            self._focused._on_key_hold(keys,unicode)
            return
        super()._on_key_hold(keys,unicode)
    
    def _on_key_pressed(self, key: int, unicode: str):
        if self._focused is not None:
            self._focused._on_key_pressed(key,unicode)
            return
        super()._on_key_pressed(key,unicode)
    
    def _on_key_released(self, key: int, unicode: str):
        if self._focused is not None:
            self._focused._on_key_released(key,unicode)
            return
        super()._on_key_released(key,unicode)