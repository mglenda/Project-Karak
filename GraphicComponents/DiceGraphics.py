from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

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

        self.focus_layer = Image(w,h,PATH + 'FocusLayer.png',self)
        self.focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.focus_layer.set_visible(False)

        self.set_alpha(255)

    def set_value(self, value: int):
        if value is not None:
            self.set_texture(PATH + PATH_DICE_SIDES[value])
        else:
            self.set_texture(PATH + 'None.png')

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