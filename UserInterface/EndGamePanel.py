from __future__ import annotations

from typing import TYPE_CHECKING

from GraphicsEngine.Constants import Framepoint as FRAMEPOINT, MouseEvent
from GraphicsEngine.Frame import Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Rect import Rect
from GraphicsEngine.TextField import TextField

if TYPE_CHECKING:
    from Game import Game
    from GameEngine.Hero import Hero


GOLD = (255, 215, 90)
WHITE = (245, 245, 245)
MUTED = (175, 175, 185)
PANEL = (20, 20, 28)


class AwardCard:
    def __init__(self, parent: Frame, title: str, hero: Hero | None, subtitle: str,
                 width: float, height: float) -> None:
        self.main = Rect(width, height, PANEL, parent)
        self.title = TextField(self.main, font_color=GOLD, font_size=25, text=title)
        self.title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, height * 0.1)
        name = hero.get_name() if hero is not None else 'No contender'
        self.hero_name = TextField(self.main, font_color=WHITE, font_size=30, text=name)
        self.hero_name.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER, 0, -height * 0.03)
        self.subtitle = TextField(self.main, font_color=MUTED, font_size=19, text=subtitle)
        self.subtitle.set_point(FRAMEPOINT.BOTTOM, FRAMEPOINT.BOTTOM, 0, -height * 0.1)


class EndGameReportRow:
    def __init__(self, parent: Frame, rank: int, hero: Hero, width: float, height: float,
                 on_click) -> None:
        color = (45, 37, 18) if rank == 1 else PANEL
        self.main = Rect(width, height, color, parent)
        self.main.register_mouse_event(MouseEvent.LEFTCLICK, on_click, hero)
        self.icon = Image(height * 0.76, height * 0.76, hero.get_icon_path(), self.main)
        self.icon.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, height * 0.14)
        self.name = TextField(self.main, font_color=GOLD if rank == 1 else WHITE, font_size=27,
                              text=f'{rank}. {hero.get_name()}')
        self.name.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.RIGHT, height * 0.18, 0, self.icon)
        summary = f'Score {hero.get_chest_score()}  |  Weapon {hero.get_weapon_power()}  |  Click for details'
        self.summary = TextField(self.main, font_color=MUTED, font_size=20, text=summary)
        self.summary.set_point(FRAMEPOINT.RIGHT, FRAMEPOINT.RIGHT, -height * 0.18)

    def destroy(self) -> None:
        self.main.destroy()


class EndGamePanel:
    def __init__(self, screen: Frame, game: Game) -> None:
        self.service = game.end_game_service
        self.statistics_service = game.statistics_service
        self.main = Rect(screen.get_w(), screen.get_h(), (8, 8, 12), screen)
        self.main.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)

        self.announcement = Rect(self.main.get_w(), self.main.get_h(), (8, 8, 12), self.main)
        self.announcement.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.announcement_title = TextField(self.announcement, font_color=GOLD, font_size=64,
                                            text='The Dragon has fallen')
        self.announcement_title.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER, 0, -self.main.get_h() * 0.09)
        self.announcement_message = TextField(self.announcement, font_color=WHITE, font_size=34, text='')
        self.announcement_message.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0,
                                            self.main.get_h() * 0.05, self.announcement_title)
        self.continue_text = TextField(self.announcement, font_color=MUTED, font_size=25,
                                       text='Click anywhere to continue...')
        self.continue_text.set_point(FRAMEPOINT.BOTTOM, FRAMEPOINT.BOTTOM, 0, -self.main.get_h() * 0.08)
        self.announcement.register_mouse_event(MouseEvent.LEFTCLICK, self.service.continue_to_report)

        self.report = Rect(self.main.get_w(), self.main.get_h(), (8, 8, 12), self.main)
        self.report.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.report_title = TextField(self.report, font_color=GOLD, font_size=52, text='END GAME REPORT')
        self.report_title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.main.get_h() * 0.025)
        self.reason = TextField(self.report, font_color=MUTED, font_size=23, text='')
        self.reason.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.01, self.report_title)

        self.winner_card = Rect(self.main.get_w() * 0.54, self.main.get_h() * 0.16, (45, 37, 18), self.report)
        self.winner_card.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.018, self.reason)
        self.winner_icon = Image(self.winner_card.get_h() * 0.8, self.winner_card.get_h() * 0.8,
                                 '_Textures\\Heroes\\MyIcons\\Acrobat.png', self.winner_card)
        self.winner_icon.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.LEFT, self.winner_card.get_h() * 0.14)
        self.winner_name = TextField(self.winner_card, font_color=GOLD, font_size=37, text='Winner')
        self.winner_name.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.RIGHT, self.winner_card.get_h() * 0.22,
                                   -self.winner_card.get_h() * 0.14, self.winner_icon)
        self.winner_score = TextField(self.winner_card, font_color=WHITE, font_size=26, text='Final score: 0')
        self.winner_score.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.BOTTOMLEFT, 0,
                                    self.winner_card.get_h() * 0.08, self.winner_name)

        self.awards_label = TextField(self.report, font_color=WHITE, font_size=29, text='FUN AWARDS')
        self.awards_label.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.main.get_h() * 0.018,
                                    self.winner_card)
        self.awards: list[AwardCard] = []
        self.ranking_label = TextField(self.report, font_color=WHITE, font_size=29, text='FINAL RANKING')
        self.rows: list[EndGameReportRow] = []

        self.detail = Rect(self.main.get_w() * 0.84, self.main.get_h() * 0.82, (14, 14, 20), self.main)
        self.detail.set_point(FRAMEPOINT.CENTER, FRAMEPOINT.CENTER)
        self.detail.register_mouse_event(MouseEvent.LEFTCLICK, self.service.close_hero_detail)
        self.detail_title = TextField(self.detail, font_color=GOLD, font_size=48, text='Player statistics')
        self.detail_title.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, self.detail.get_h() * 0.06)
        self.detail_icon = Image(self.detail.get_h() * 0.18, self.detail.get_h() * 0.18,
                                 '_Textures\\Heroes\\MyIcons\\Acrobat.png', self.detail)
        self.detail_icon.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.detail.get_h() * 0.035,
                                   self.detail_title)
        self.detail_lines: list[TextField] = []
        self.detail_hint = TextField(self.detail, font_color=MUTED, font_size=21,
                                     text='Click anywhere to return to the End Game Report')
        self.detail_hint.set_point(FRAMEPOINT.BOTTOM, FRAMEPOINT.BOTTOM, 0, -self.detail.get_h() * 0.045)

        self.loaded_report = False
        self.loaded_detail_hero = None
        self.announcement.set_visible(False)
        self.main.set_visible(False)
        self.report.set_visible(False)
        self.detail.set_visible(False)

    def is_visible(self) -> bool:
        return self.main.is_visible()

    def _clear_report(self) -> None:
        for award in reversed(self.awards):
            award.main.destroy()
        self.awards.clear()
        for row in reversed(self.rows):
            row.destroy()
        self.rows.clear()

    def _award_data(self):
        heroes = self.service.ranking
        master = self.statistics_service.get_master_of_combat(heroes)
        giant = self.statistics_service.get_giant_slayer(heroes)
        high = self.statistics_service.get_high_roller(heroes)
        unlucky = self.statistics_service.get_unlucky_soul(heroes)
        return [
            ('Master of Combat', master, f'{self.statistics_service.get(master).wins} wins' if master else 'No combats'),
            ('Giant Slayer', giant, f'Power {self.statistics_service.get(giant).strongest_minion_defeated}' if giant else 'No minions defeated'),
            ('High Roller', high, f'Average {self.statistics_service.get(high).get_average_roll():.1f}' if high else 'No rolls'),
            ('Unlucky Soul', unlucky, f'Average {self.statistics_service.get(unlucky).get_average_roll():.1f}' if unlucky else 'No rolls'),
        ]

    def _load_report(self) -> None:
        self._clear_report()
        ranking = self.service.ranking
        self.reason.set_text(self.service.reason)
        if ranking:
            winner = ranking[0]
            self.winner_icon.set_texture(winner.get_icon_path())
            self.winner_name.set_text(winner.get_name())
            self.winner_score.set_text(f'Final score: {winner.get_chest_score()}')

        card_gap = self.main.get_w() * 0.012
        card_w = (self.main.get_w() * 0.9 - card_gap * 3) / 4
        card_h = self.main.get_h() * 0.135
        previous = None
        for title, hero, subtitle in self._award_data():
            card = AwardCard(self.report, title, hero, subtitle, card_w, card_h)
            if previous is None:
                card.main.set_point(FRAMEPOINT.TOPLEFT, FRAMEPOINT.BOTTOMLEFT,
                                    -self.main.get_w() * 0.45, self.main.get_h() * 0.012, self.awards_label)
            else:
                card.main.set_point(FRAMEPOINT.LEFT, FRAMEPOINT.RIGHT, card_gap, 0, previous)
            self.awards.append(card)
            previous = card.main

        ranking_y = self.main.get_h() * 0.685
        self.ranking_label.set_point(FRAMEPOINT.TOP, FRAMEPOINT.TOP, 0, ranking_y, self.report)
        count = len(ranking)
        if count:
            gap = self.main.get_h() * 0.009
            available = self.main.get_h() * 0.245
            row_h = min(self.main.get_h() * 0.07, (available - gap * (count - 1)) / count)
            previous = None
            for rank, hero in enumerate(ranking, 1):
                row = EndGameReportRow(self.report, rank, hero, self.main.get_w() * 0.8, row_h,
                                       self.service.show_hero_detail)
                if previous is None:
                    row.main.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, gap, self.ranking_label)
                else:
                    row.main.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, gap, previous)
                self.rows.append(row)
                previous = row.main
        self.loaded_report = True

    def _load_detail(self, hero: Hero) -> None:
        for line in reversed(self.detail_lines):
            line.destroy()
        self.detail_lines.clear()
        statistics = self.statistics_service.get(hero)
        self.detail_title.set_text(hero.get_name())
        self.detail_icon.set_texture(hero.get_icon_path())
        values = [
            f'Combats: {statistics.combats}    Wins: {statistics.wins}    Losses: {statistics.losses}    Draws: {statistics.draws}',
            f'Win rate: {statistics.get_win_rate():.1f}%',
            f'Against minions: {statistics.minion_combats}    Against heroes: {statistics.hero_combats}',
            f'Average combat power: {statistics.get_average_combat_power():.1f}',
            f'Highest combat power: {statistics.highest_combat_power}',
            f'Average dice roll: {statistics.get_average_roll():.1f}',
            f'Highest dice roll: {statistics.highest_roll}    Full rolls: {statistics.full_rolls}',
            f'Rerolled dice: {statistics.rerolled_dice}',
            f'Chests: {hero.inventory.get_chest_count()}    Chest score: {hero.get_chest_score()}',
            f'Final weapon power: {hero.get_weapon_power()}',
            f'Other items: {hero.get_non_chest_non_weapon_slot_item_count()}',
        ]
        previous = self.detail_icon
        for value in values:
            line = TextField(self.detail, font_color=WHITE, font_size=25, text=value)
            line.set_point(FRAMEPOINT.TOP, FRAMEPOINT.BOTTOM, 0, self.detail.get_h() * 0.025, previous)
            self.detail_lines.append(line)
            previous = line
        self.loaded_detail_hero = hero

    def update(self) -> None:
        if not self.service.is_active():
            self.announcement.set_visible(False)
            self.report.set_visible(False)
            self.detail.set_visible(False)
            for row in self.rows:
                row.main.set_visible(False)
            self.main.set_visible(False)
            return
        self.main.set_visible(True)
        if self.service.is_announcement():
            self.announcement_message.set_text(self.service.reason)
            self.announcement.set_visible(True)
            self.report.set_visible(False)
            self.detail.set_visible(False)
            return

        self.announcement.set_visible(False)
        if not self.loaded_report:
            self._load_report()
        selected = self.service.selected_hero
        if selected is not None:
            if selected is not self.loaded_detail_hero:
                self._load_detail(selected)
            for row in self.rows:
                row.main.set_visible(False)
            self.report.set_visible(False)
            self.detail.set_visible(True)
        else:
            self.detail.set_visible(False)
            self.report.set_visible(True)
            for row in self.rows:
                row.main.set_visible(True)
