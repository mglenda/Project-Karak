from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class CombatScreen(Rect):
    background:Rect

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w, h, (255,255,255), parent)

        self.background = Rect(w-w*0.01,h-h*0.01,(0,0,0),self)
        self.background.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)