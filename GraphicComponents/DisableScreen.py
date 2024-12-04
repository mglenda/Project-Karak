from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class DisableScreen(Rect):
    def __init__(self, parent: Frame) -> None:
        super().__init__(parent.get_w(), parent.get_h(), (0,0,0), parent)
        self.set_alpha(150)

        self.set_visible(False)
        self.set_active(True)

        self.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)