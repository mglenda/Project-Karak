from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Rect

class CombatScreen(Rect):
    def __init__(self, w: int, h: int, parent: Frame) -> None:
        self._alpha = 200
        super().__init__(w, h, (0,0,0), parent)
