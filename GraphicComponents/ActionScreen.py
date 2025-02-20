from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class ActionButton(Image):
    normal_path: str
    focused_path: str
    focus_layer_path: str = '_Textures\\Abilities\\FocusLayer.png'
    focus_layer: Image

    def __init__(self, w, h, parent,focused_path: str, normal_path: str):
        self.normal_path = normal_path
        self.focused_path = focused_path
        super().__init__(w, h, normal_path, parent)

        self.set_active(True)
        self.set_alpha(255)
        self.focus_layer = Image(w*0.95,h*0.95,self.focus_layer_path,self)
        self.focus_layer.set_alpha(50)

        self.focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.focus_layer.set_visible(False)
        self.focus_layer.set_active(False)

    def on_mouse_enter(self):
        self.set_texture(self.focused_path)
        self.focus_layer.set_alpha(50)
        self.focus_layer.set_visible(True)
        return super().on_mouse_enter()
    
    def on_mouse_leave(self):
        self.set_texture(self.normal_path)
        self.focus_layer.set_visible(False)
        return super().on_mouse_leave()
    
    def on_mouse_left_press(self, x, y):
        self.focus_layer.set_alpha(100)
        return super().on_mouse_left_press(x, y)
    
    def on_mouse_left_click(self, x, y):
        self.set_texture(self.focused_path)
        self.focus_layer.set_alpha(50)
        return super().on_mouse_left_click(x, y)

class ActionScreen(Rect):
    def __init__(self,w: int, h: int, parent: Frame) -> None:
        super().__init__(w,h, (255,255,255), parent)
        self.set_alpha(0)

        self.set_visible(False)
        self.set_active(False)