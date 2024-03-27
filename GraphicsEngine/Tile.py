from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT,MouseEvent

class Tile(Image):
    focus_layer: Rect
    active_layer: Rect

    def __init__(self, size: int, path: str, parent: Frame) -> None:
        super().__init__(size, size, path, parent)

        self.active_layer = Rect(size,size,(0,150,0),self)
        self.active_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.active_layer.set_alpha(100)
        self.active_layer.set_visible(False)

        self.focus_layer = Rect(size,size,(255,215,0),self)
        self.focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.focus_layer.set_alpha(100)
        self.focus_layer.set_visible(False)

    def set_active(self, active: bool):
        super().set_active(active)
        self.active_layer.set_visible(active)
        if active == False: 
            self.focus_layer.set_visible(False)

    def on_mouse_enter(self):
        self.focus_layer.set_visible(True)
        super().on_mouse_enter()
    
    def on_mouse_leave(self):
        self.focus_layer.set_visible(False)
        super().on_mouse_leave()