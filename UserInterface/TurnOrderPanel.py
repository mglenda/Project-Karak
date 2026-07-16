from __future__ import annotations

import math
from typing import TYPE_CHECKING

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField
from GraphicsEngine.NumberImage import NumberImage
from GraphicsEngine.TextColors import TextColors

if TYPE_CHECKING:
    from Game import Game
    from GameEngine.Hero import Hero


CURSE_ICON_PATH = '_Textures\\Abilities\\Curse.png'
HEALTH_ICON_PATH = '_Textures\\HeroPanel\\HitPoints_Green.png'
MOVE_ICON_PATH = '_Textures\\HeroPanel\\MovePoints.png'
CHEST_ICON_PATH = '_Textures\\ScorePanel\\ChestIcon.png'
ROW_COLOR = (10, 10, 12)
ROW_HIGHLIGHTED_COLOR = (30, 28, 18)


class TurnOrderRow:
    def __init__(self, parent: Frame, w: int, h: int) -> None:
        self.main = Rect(w, h, ROW_COLOR, parent)
        self.main.set_alpha(0)

        font_size = max(16, int(h * 0.34))
        hero_icon_size = h * 0.82
        stat_icon_size = h * 0.32

        row_padding = w * 0.018
        usable_w = w - row_padding * 2
        section_weights = (0.06, 0.12, 0.17, 0.13, 0.16, 0.16, 0.20)
        section_widths = [usable_w * weight for weight in section_weights]
        section_centers = []
        section_left = row_padding
        for section_w in section_widths:
            section_centers.append(section_left + section_w / 2)
            section_left += section_w

        order_center, icon_center, name_center, chest_center, health_center, move_center, _ = section_centers
        self.inventory_x = row_padding + sum(section_widths[:-1])
        self.inventory_w = section_widths[-1]
        self.group_gap = h * 0.06

        self.order_text = TextField(self.main, font_color=(255, 215, 90), font_size=font_size, text='1.')
        self.order_text.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.LEFT, order_center, 0)

        self.hero_icon = Image(hero_icon_size, hero_icon_size, '_Textures\\Heroes\\MyIcons\\Acrobat.png', self.main)
        self.hero_icon.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.LEFT, icon_center, 0)

        self.name_text = TextField(self.main, font_color=(255, 255, 255), font_size=font_size, text='Hero')
        self.name_text.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.LEFT, name_center, 0)

        self.health_center = health_center
        self.health_icon = Image(stat_icon_size, stat_icon_size, HEALTH_ICON_PATH, self.main)
        self.health_text = TextField(self.main, font_color=(120, 230, 120), font_size=font_size, text='0/0')

        self.move_center = move_center
        self.move_icon = Image(stat_icon_size, stat_icon_size, MOVE_ICON_PATH, self.main)
        self.move_text = TextField(self.main, font_color=(255, 255, 255), font_size=font_size, text='0/0')

        chest_icon_size = h * 0.44
        self.chest_center = chest_center
        self.chest_icon = Image(chest_icon_size, chest_icon_size, CHEST_ICON_PATH, self.main)
        self.chest_text = NumberImage(chest_icon_size,chest_icon_size,0,TextColors.GOLD,self.main)
        

        self.curse_icon = Image(hero_icon_size*0.75, hero_icon_size*0.75, CURSE_ICON_PATH, self.main)
        self.curse_icon.set_point(FRAMEPOINT.BOTTOMLEFT, FRAMEPOINT.BOTTOMLEFT, -hero_icon_size*0.2, hero_icon_size*0.1, self.hero_icon)
        self.curse_icon.set_visible(False)

        self._center_group(self.chest_center, self.chest_icon, self.chest_text)
        self._center_group(self.health_center, self.health_icon, self.health_text)
        self._center_group(self.move_center, self.move_icon, self.move_text)

        for e in self.main.get_children():
            e.set_alpha(255)

        self.item_icons: list[Image] = []
        self.loaded_slots: tuple[object | None, ...] = ()
        self.hero: Hero | None = None
        self.loaded_icon_path: str | None = None
        self.highlighted: bool | None = None

    def _center_group(self, center_x: float, icon: Image, text: TextField) -> None:
        group_w = icon.get_w() + self.group_gap + text.get_w()
        group_x = center_x - group_w / 2
        icon.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, group_x, 0)
        text.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, group_x + icon.get_w() + self.group_gap, 0)

    def set_point(self, att_point: int, att_point_parent: int, x_offset: int = 0, y_offset: int = 0, parent: Frame = None):
        self.main.set_point(att_point, att_point_parent, x_offset, y_offset, parent)

    def destroy(self) -> None:
        self.main.destroy()

    def update(self, order: int, hero: Hero, highlighted: bool) -> None:
        if self.hero is not hero:
            self.hero = hero
            self.name_text.set_text(hero.get_name())

        icon_path = hero.get_icon_path()
        if self.loaded_icon_path != icon_path:
            self.loaded_icon_path = icon_path
            self.hero_icon.set_texture(icon_path)

        self.order_text.set_text(f'{order}.')
        self.health_text.set_text(f'{hero.get_hit_points()}/{hero.get_max_hit_points()}')
        self.move_text.set_text(f'{hero.get_move_points()}/{hero.get_max_move_points()}')
        self.chest_text.set_value(hero.get_chest_score())
        self._center_group(self.chest_center, self.chest_icon, self.chest_text)
        self._center_group(self.health_center, self.health_icon, self.health_text)
        self._center_group(self.move_center, self.move_icon, self.move_text)
        self.curse_icon.set_visible(hero.is_cursed())

        if self.highlighted != highlighted:
            self.highlighted = highlighted
            self.main.color = ROW_HIGHLIGHTED_COLOR if highlighted else ROW_COLOR
            self.main.set_alpha(255 if highlighted else 0,True)
            self.main.refresh_surface()

        slots = tuple(slot.get_item() for slot in hero.inventory.slots)
        if self.loaded_slots != slots:
            self.reload_items(slots)

    def reload_items(self, slots: tuple[object | None, ...]) -> None:
        for icon in self.item_icons:
            icon.destroy()
        self.item_icons.clear()
        self.loaded_slots = slots

        if not slots:
            return

        column_count = min(3, len(slots))
        row_count = math.ceil(len(slots) / column_count)
        gap = self.main.get_h() * 0.04
        available_h = self.main.get_h() - gap * (row_count + 1)
        available_w = self.inventory_w - gap * (column_count + 1)
        item_icon_size = min(available_h / row_count, available_w / column_count)
        grid_w = column_count * item_icon_size + (column_count - 1) * gap
        grid_h = row_count * item_icon_size + (row_count - 1) * gap
        grid_x = self.inventory_x + (self.inventory_w - grid_w) / 2
        grid_y = (self.main.get_h() - grid_h) / 2

        for i, item in enumerate(slots):
            if item is None:
                continue

            column = i % column_count
            row = i // column_count
            icon = Image(item_icon_size, item_icon_size, item.definition.path, self.main)
            icon.set_point(
                FRAMEPOINT.TOPLEFT,
                FRAMEPOINT.TOPLEFT,
                grid_x + column * (item_icon_size + gap),
                grid_y + row * (item_icon_size + gap),
            )
            self.item_icons.append(icon)
            icon.set_alpha(255)


class TurnOrderPanel:
    def __init__(self, screen: Frame, game: Game) -> None:
        self.context = game.context
        self.main = Rect(screen.get_w() * 0.368, screen.get_h() * 0.176, (0, 0, 0), screen)
        self.main.set_alpha(150)
        self.main.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.TOPLEFT)
        self.rows: list[TurnOrderRow] = []
        self.loaded_hero_count: int | None = None

    def update(self) -> None:
        ranking = self.context.get_hero_ranking()
        current_hero = self.context.get_current_hero() if self.context.heroes else None
        if self.loaded_hero_count != len(ranking):
            self.reload(len(ranking))

        for i, hero in enumerate(ranking):
            self.rows[i].update(i + 1, hero, hero is current_hero)

    def reload(self, hero_count: int) -> None:
        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.loaded_hero_count = hero_count

        if hero_count == 0:
            return

        row_gap = 0
        row_h = (self.main.get_h() - row_gap * (hero_count + 1)) / hero_count
        row_w = self.main.get_w() - row_gap * 2

        for i in range(hero_count):
            row = TurnOrderRow(self.main, row_w, row_h)
            if i == 0:
                row.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.TOPLEFT, row_gap, row_gap)
            else:
                row.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, row_gap, self.rows[-1].main)
            self.rows.append(row)
