from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField

CURSE_ICON_PATH = '_Textures\\Abilities\\Curse.png'


class CursePanel:
    def __init__(self, screen: Frame) -> None:
        self.main = Rect(screen.get_w() * 0.4, screen.get_h(), (0, 0, 0), screen)
        # self.main.set_alpha(190)
        self.main.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER, 0, 0)
        self.main.set_visible(False)
        self.main.set_active(False)

        icon_size = self.main.get_h() * 0.15
        self.icon = Image(icon_size, icon_size, CURSE_ICON_PATH, self.main)
        self.icon.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.main.get_h() * 0.08)

        self.message = TextField(self.main, font_color=(255, 255, 255), font_size=34, text='You resisted the curse')
        self.message.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.08, self.icon)

    def show_prompt(self):
        self.message.set_text('Roll 4 or higher to resist the curse')
        self.main.set_visible(True)

    def show_result(self, message: str):
        self.message.set_text(message)
        self.message.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.08, self.icon)
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self) -> bool:
        return self.main.is_visible()
