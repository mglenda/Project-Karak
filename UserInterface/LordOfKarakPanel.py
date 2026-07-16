from __future__ import annotations

from typing import TYPE_CHECKING

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT, MouseEvent
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField

if TYPE_CHECKING:
    from Game import Game


class LordOfKarakPanel:
    def __init__(self, screen: Frame, game: Game) -> None:
        self.service = game.lord_of_karak_service
        self.main = Rect(screen.get_w() * 0.68, screen.get_h() * 0.62, (225, 205, 120), screen)
        self.main.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.background = Rect(self.main.get_w() * 0.985, self.main.get_h() * 0.98, (12, 12, 15), self.main)
        self.background.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.title = TextField(self.background, font_color=(255, 215, 90), font_size=44, text='The Lord of Karak has risen')
        self.title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.main.get_h() * 0.05)
        self.hero_icon = Image(self.main.get_h() * 0.2, self.main.get_h() * 0.2, '_Textures\\Heroes\\MyIcons\\LordOfKarak.png', self.background)
        self.hero_icon.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.035, self.title)
        self.hero_name = TextField(self.background, font_color=(255, 255, 255), font_size=34, text='Hero')
        self.hero_name.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.02, self.hero_icon)
        self.former_label = TextField(self.background, font_color=(190, 190, 190), font_size=25, text='Former special actions')
        self.former_label.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, self.main.get_w() * 0.07, self.main.get_h() * 0.12)
        self.new_label = TextField(self.background, font_color=(255, 215, 90), font_size=25, text='New special actions')
        self.new_label.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, self.main.get_w() * 0.07, self.main.get_h() * 0.31)
        self.continue_text = TextField(self.background, font_color=(180, 180, 180), font_size=22, text='Click anywhere to continue')
        self.continue_text.set_point(FRAMEPOINT.BOTTOM, FRAMEPOINT.BOTTOM, 0, -self.main.get_h() * 0.04)
        self.action_icons: list[Image] = []
        self.loaded = False
        self.main.register_mouse_event(MouseEvent.LEFTCLICK, self.service.dismiss)
        self.main.set_visible(False)

    def is_visible(self) -> bool:
        return self.main.is_visible()

    def clear_icons(self) -> None:
        for icon in reversed(self.action_icons):
            icon.destroy()
        self.action_icons.clear()

    def _add_action_icons(self, action_types, y_offset: float) -> None:
        if not action_types:
            return
        size = self.main.get_h() * 0.105
        gap = size * 0.18
        for i, action_type in enumerate(action_types):
            icon = Image(size, size, action_type.path, self.background)
            icon.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, self.main.get_w() * 0.38 + i * (size + gap), y_offset)
            self.action_icons.append(icon)

    def reload(self) -> None:
        self.clear_icons()
        self.hero_icon.set_texture(self.service.hero.get_icon_path())
        self.hero_name.set_text(f'{self.service.hero.get_name()} became the Lord of Karak')
        self._add_action_icons(self.service.former_action_types, self.main.get_h() * 0.12)
        self._add_action_icons(self.service.new_action_types, self.main.get_h() * 0.31)
        self.loaded = True

    def update(self) -> None:
        if not self.service.is_active():
            if self.is_visible():
                self.main.set_visible(False)
            self.loaded = False
            return
        if not self.loaded:
            self.reload()
        self.main.set_visible(True)
