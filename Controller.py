import pygame
from GUI.Behaviors import MouseBehavior
from GUI.Graphics import Panel

class MainScreen(Panel):
    def __init__(self, w, h) -> None:
        self.set_abs_point(0,0)
        super().__init__(w=w, h=h, rgb=(0,0,0), surface=pygame.display.set_mode((w,h),pygame.FULLSCREEN))

    def _on_mouse_leave(self):
        pass

    def _on_mouse_enter(self):
        pass

class Main(MouseBehavior):
    screen_width: int
    screen_height: int
    screen: MainScreen
    def __init__(self) -> None:
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = MainScreen(self.screen_width,self.screen_height)

        w = self.screen_width / 4.096
        h = self.screen_height / 1.73
        x = self.screen_width / 2 - w / 2
        y = self.screen_height / 2 - h / 2
        self.screen.add(Panel(w=w,h=h,rgb=(50,50,50)),x+200,y-100)
        self.screen.add(Panel(w=w,h=h,rgb=(50,50,50)),x,y)
        p = Panel(w=w,h=h,rgb=(50,50,50))
        self.screen.add(p,x-200,y+100)
        pp = Panel(w=100,h=100,rgb=(255,0,0))
        p.add(pp,0,0)
        pp.add(Panel(w=25,h=25,rgb=(0,255,0)),0,0)

    def draw(self):
        self.screen.draw()

    def _on_mouse_right_click(self,x,y):
        self.screen._on_mouse_right_click(x,y)

    def _on_mouse_left_click(self,x,y):
        self.screen._on_mouse_left_click(x,y)

    def _on_mouse_wheel_up(self,x,y):
        self.screen._on_mouse_wheel_up(x,y)

    def _on_mouse_wheel_down(self,x,y):
        self.screen._on_mouse_wheel_down(x,y)

    def _on_mouse_motion(self,x,y):
        self.screen._on_mouse_motion(x,y)

    def _on_mouse_wheel_click(self,x,y):
        self.screen._on_mouse_wheel_click(x,y)