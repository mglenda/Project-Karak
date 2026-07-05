from __future__ import annotations

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField
from GraphicsEngine.NumberImage import NumberImage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game
    from GameEngine.Hero import Hero

PLACEHOLDER_ICON_PATH = '_Textures\\Heroes\\MyIcons\\Acrobat.png'
CHEST_ICON_PATH = '_Textures\\ScorePanel\\ChestIcon.png'


class RankingRow:
    def __init__(self, parent: Frame, rank: int, w: int, h: int) -> None:
        self.rank = rank
        self.main = Rect(w, h, (10, 10, 12), parent)
        self.main.set_alpha(255)

        padding = h * 0.12
        rank_w = w * 0.14
        icon_size = h * 0.74

        self.rank_text = NumberImage(rank_w,h*0.65,rank,'White',self.main)
        self.rank_text.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, padding, 0)

        self.icon = Image(icon_size, icon_size, PLACEHOLDER_ICON_PATH, self.main)
        self.icon.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.RIGHT, padding, 0, self.rank_text)

        self.name_text = TextField(self.main, font_color=(255, 255, 255), font_size=35, text='HeroName')
        self.name_text.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.RIGHT, padding*3, 0, self.icon)

        self.score_text = NumberImage(rank_w,h*0.65,rank,'White',self.main)
        self.score_text.set_point(FRAMEPOINT.RIGHT, FRAMEPOINT.RIGHT, -padding, 0)

        self.chest_icon = Image(icon_size, icon_size, CHEST_ICON_PATH, self.main)
        self.chest_icon.set_point(FRAMEPOINT.RIGHT, FRAMEPOINT.LEFT, - padding, 0, self.score_text)


        self.hero: Hero = None
        self.score: float = None

    def set_point(self, att_point: int, att_point_parent: int, x_offset: int = 0, y_offset: int = 0, parent: Frame = None):
        self.main.set_point(att_point, att_point_parent, x_offset, y_offset, parent)

    def destroy(self):
        self.main.destroy()

    def update(self, hero: Hero):
        score = hero.get_chest_score()
        if self.hero != hero:
            self.hero = hero
            self.icon.set_texture(hero.get_icon_path())
            self.name_text.set_text(hero.get_name())

        if self.score != score:
            self.score = score
            self.score_text.set_value(int(score))


class RankingPanel:
    rows: list[RankingRow]

    def __init__(self, screen: Frame, game: "Game") -> None:
        self.context = game.context
        self.main = Rect(screen.get_w() * 0.22, screen.get_h() * 0.16, (0, 0, 0), screen)
        self.main.set_alpha(120)
        self.main.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.TOPLEFT)
        self.rows = []
        self.loaded_hero_count = None

    def update(self):
        ranking = self.context.get_hero_ranking()

        if self.loaded_hero_count != len(ranking):
            self.reload(len(ranking))

        for i, hero in enumerate(ranking):
            self.rows[i].update(hero)

    def reload(self, hero_count: int):
        for row in self.rows:
            row.destroy()
        self.rows.clear()

        self.loaded_hero_count = hero_count
        if hero_count == 0:
            return

        row_gap = self.main.get_h() * 0.045
        row_h = (self.main.get_h() - row_gap * (hero_count + 1)) / hero_count
        row_w = self.main.get_w() - row_gap * 2

        for i in range(hero_count):
            row = RankingRow(self.main, i + 1, row_w, row_h)
            if i == 0:
                row.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.TOPLEFT, row_gap, row_gap)
            else:
                row.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, row_gap, self.rows[i - 1].main)
            self.rows.append(row)
