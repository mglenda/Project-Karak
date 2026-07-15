from __future__ import annotations

from typing import TYPE_CHECKING

from GraphicComponents.HeroSelectionOption import HeroSelectionOption
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField

if TYPE_CHECKING:
    from Game import Game


class HeroSelectionPanel:
    def __init__(self, screen: Frame, game: Game) -> None:
        self.service = game.hero_selection_service
        self.main = Rect(screen.get_w() * 0.56, screen.get_h() * 0.34, (225, 205, 120), screen)
        self.main.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)

        self.background = Rect(self.main.get_w() * 0.985, self.main.get_h() * 0.975, (12, 12, 15), self.main)
        self.background.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)

        self.title = TextField(
            self.background,
            font_color=(255, 215, 90),
            font_size=max(24, int(self.main.get_h() * 0.1)),
            text='Choose a hero',
        )
        self.title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.main.get_h() * 0.08)

        self.options: list[HeroSelectionOption] = []
        self.loaded_selection_id: int | None = None
        self.main.set_visible(False)

    def show(self) -> None:
        self.main.set_visible(True)

    def hide(self) -> None:
        self.main.set_visible(False)
        self.clear_options()
        self.loaded_selection_id = None

    def is_visible(self) -> bool:
        return self.main.is_visible()

    def clear_options(self) -> None:
        for option in reversed(self.options):
            option.destroy()
        self.options.clear()

    def reload(self) -> None:
        self.clear_options()
        self.loaded_selection_id = self.service.selection_id
        self.title.set_text(self.service.prompt)

        candidates = self.service.candidates
        if not candidates:
            return

        gap = self.main.get_w() * 0.025
        available_w = self.background.get_w() - gap * (len(candidates) + 1)
        option_w = min(self.main.get_w() * 0.23, available_w / len(candidates))
        option_h = self.main.get_h() * 0.62
        total_w = option_w * len(candidates) + gap * (len(candidates) - 1)
        start_x = -total_w / 2 + option_w / 2
        y_offset = self.main.get_h() * 0.08

        for i, hero in enumerate(candidates):
            option = HeroSelectionOption(option_w, option_h, self.background, hero, self.service.select_hero)
            option.set_point(
                FRAMEPOINT.CENTER,
                FRAMEPOINT.CENTER,
                start_x + i * (option_w + gap),
                y_offset,
            )
            self.options.append(option)

    def update(self) -> None:
        if not self.service.is_active():
            if self.is_visible():
                self.hide()
            return

        if not self.is_visible():
            self.show()
        if self.loaded_selection_id != self.service.selection_id:
            self.reload()
