from __future__ import annotations

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT, MouseEvent
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField


class HeroSelectionOption:
    def __init__(self, w: int, h: int, parent: Frame, hero, on_select) -> None:
        self.hero = hero
        self.main = Rect(w, h, (55, 50, 35), parent)
        self.main.set_alpha(230)

        icon_size = min(w * 0.72, h * 0.68)
        self.icon = Image(icon_size, icon_size, hero.get_icon_path(), self.main)
        self.icon.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, h * 0.07)

        self.name = TextField(
            self.main,
            font_color=(255, 255, 255),
            font_size=max(18, int(h * 0.12)),
            text=hero.get_name(),
        )
        self.name.set_point(FRAMEPOINT.BOTTOM, FRAMEPOINT.BOTTOM, 0, -h * 0.07)

        self.main.register_mouse_event(MouseEvent.LEFTCLICK, on_select, hero)
        self.main.register_mouse_event(MouseEvent.ENTER, self.set_hovered, True)
        self.main.register_mouse_event(MouseEvent.LEAVE, self.set_hovered, False)

    def set_point(self, att_point: int, att_point_parent: int, x_offset: int = 0, y_offset: int = 0, parent: Frame = None) -> None:
        self.main.set_point(att_point, att_point_parent, x_offset, y_offset, parent)

    def set_hovered(self, hovered: bool) -> None:
        self.main.set_alpha(255 if hovered else 230)

    def destroy(self) -> None:
        self.main.destroy()
