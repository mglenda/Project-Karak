from __future__ import annotations

import math
from typing import TYPE_CHECKING

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT, MouseEvent
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField

if TYPE_CHECKING:
    from Game import Game


class ArenaLootPanel:
    def __init__(self, screen: Frame, game: Game) -> None:
        self.combat_service = game.combat_service
        self.main = Rect(screen.get_w() * 0.56, screen.get_h() * 0.34, (225, 205, 120), screen)
        self.main.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.background = Rect(self.main.get_w() * 0.985, self.main.get_h() * 0.975, (12, 12, 15), self.main)
        self.background.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.title = TextField(self.background, font_color=(255, 215, 90), font_size=32, text='Choose an item to steal')
        self.title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.main.get_h() * 0.08)
        self.item_buttons: list[Image] = []
        self.loaded_items: tuple[object, ...] = ()
        self.main.set_visible(False)

    def is_visible(self) -> bool:
        return self.main.is_visible()

    def clear_items(self) -> None:
        for button in reversed(self.item_buttons):
            button.destroy()
        self.item_buttons.clear()

    def reload(self, items: tuple[object, ...]) -> None:
        self.clear_items()
        self.loaded_items = items
        if not items:
            return
        column_count = min(5, len(items))
        row_count = math.ceil(len(items) / column_count)
        gap = self.main.get_h() * 0.035
        available_w = self.background.get_w() * 0.9
        available_h = self.background.get_h() * 0.68
        size = min(
            (available_w - gap * (column_count - 1)) / column_count,
            (available_h - gap * (row_count - 1)) / row_count,
        )
        grid_w = column_count * size + (column_count - 1) * gap
        grid_h = row_count * size + (row_count - 1) * gap
        start_x = -grid_w / 2 + size / 2
        start_y = -grid_h / 2 + size / 2 + self.main.get_h() * 0.07
        for i, item in enumerate(items):
            column = i % column_count
            row = i // column_count
            button = Image(size, size, item.get_path(), self.background)
            button.set_alpha(210)
            button.set_point(
                FRAMEPOINT.CENTER,
                FRAMEPOINT.CENTER,
                start_x + column * (size + gap),
                start_y + row * (size + gap),
            )
            button.register_mouse_event(MouseEvent.LEFTCLICK, self.combat_service.select_arena_loot, item)
            button.register_mouse_event(MouseEvent.ENTER, button.set_alpha, 255)
            button.register_mouse_event(MouseEvent.LEAVE, button.set_alpha, 210)
            self.item_buttons.append(button)

    def update(self) -> None:
        items = tuple(self.combat_service.arena_loot_items)
        if not items:
            if self.is_visible():
                self.main.set_visible(False)
                self.clear_items()
                self.loaded_items = ()
            return
        if not self.is_visible():
            self.main.set_visible(True)
        if items != self.loaded_items:
            self.reload(items)
