from GraphicComponents.CombatScreen import CombatScreen,Frame,FRAMEPOINT
from GraphicsEngine.Constants import MouseEvent

class CombatPanel():
    main: CombatScreen

    def __init__(self,screen: Frame) -> None:
        self.main = CombatScreen(screen.get_h(),screen.get_h(),screen)
        self.main.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.main.set_visible(False)

        self.main.register_mouse_event(MouseEvent.LEFTCLICK,self.hide)

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def update(self):
        if self.main.is_visible():
            pass