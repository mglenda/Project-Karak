from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from random import choice
import pygame

PATH = '_Textures\\Dice\\'
PATH_DICE_SIDES = [
    'Zero.png'
    ,'One.png'
    ,'Two.png'
    ,'Three.png'
    ,'Four.png'
    ,'Five.png'
    ,'Six.png'
]

class DiceGraphics(Image):
    focus_layer: Image

    def __init__(self, w, h, parent):
        super().__init__(w, h, PATH + 'None.png', parent)
        self.value = None
        self.final_value = None
        self.animation_values = []
        self.is_animating = False
        self.animation_finishing = False
        self.animation_next_tick = 0
        self.animation_end_tick = 0
        self.animation_interval = 50
        self.animation_interval_step = 10

        self.focus_layer = Image(w,h,PATH + 'FocusLayer.png',self)
        self.focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.focus_layer.set_visible(False)

        self.set_alpha(255)

    def set_value(self, value: int):
        self.value = value
        if value is not None:
            self.set_texture(PATH + PATH_DICE_SIDES[value])
        else:
            self.set_texture(PATH + 'None.png')

    def start_animation(self, final_value: int, animation_values: list[int], duration: int = 2000, start_interval: int = 50, interval_step: int = 10):
        self.final_value = final_value
        self.animation_values = animation_values
        self.is_animating = True
        self.animation_finishing = False
        self.animation_interval = start_interval
        self.animation_interval_step = interval_step
        now = pygame.time.get_ticks()
        self.animation_next_tick = now
        self.animation_end_tick = now + duration

    def update_animation(self):
        if not self.is_animating:
            return

        now = pygame.time.get_ticks()
        if self.animation_finishing:
            if now >= self.animation_next_tick:
                self.is_animating = False
                self.set_value(self.final_value)
            return

        if now >= self.animation_next_tick:
            self.set_value(choice(self.animation_values))
            self.animation_next_tick = now + self.animation_interval
            self.animation_interval += self.animation_interval_step

            if self.animation_next_tick >= self.animation_end_tick:
                self.animation_finishing = True

    def on_mouse_enter(self):
        self.focus_layer.set_visible(True)
        self.focus_layer.set_alpha(255)
        return super().on_mouse_enter()
    
    def on_mouse_leave(self):
        self.focus_layer.set_visible(False)
        return super().on_mouse_leave()
    
    def on_mouse_left_press(self, x, y):
        self.focus_layer.set_alpha(140)
        return super().on_mouse_left_press(x, y)
    
    def on_mouse_left_click(self, x, y):
        self.focus_layer.set_alpha(255)
        return super().on_mouse_left_click(x, y)
    
class DiceScreen(Rect):
    def __init__(self,w: int, h: int, parent: Frame) -> None:
        super().__init__(w,h, (0,0,0), parent)
        self.set_alpha(0)

        self.set_visible(False)
        self.set_active(False)

        self.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

