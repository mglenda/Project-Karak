import pygame
from typing import Callable, List, Tuple
from operator import itemgetter
from CustomTimer.Timer import Timer

pygame.init()

class Game():
    def __init__(self) -> None:
        self.spawned = False

    def start(self):
        import GUI._const_framepoints as FRAMEPOINT
        from GUI.MainScreen import MainScreen
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = MainScreen()

        from GUI.MainMenu import MainMenu

        self.main_menu = MainMenu(self.screen.get_w(),self.screen.get_h(),self.screen)
        self.main_menu.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.screen.set_focus(self.main_menu)

        from GameLogic.PlayerGroup import PlayerGroup
        self.players = PlayerGroup()

        self.timers = []
        self.player_panels = []

    def spawn(self):
        from GUI.CastleScreen import CastleScreen
        self.flush_main_menu()
        self.castle = CastleScreen()
        self.screen.set_focus(self.castle)

        from GUI.PlayerPanel import PlayerPanel,FRAMEPOINT
        h = self.screen.get_h() * 0.24
        w = h * 1.58
        for pl in self.players.get_all():
            p = PlayerPanel(w*0.9,h*0.9,self.screen)
            p.load_player(pl)
            self.player_panels.append(p)

        p: PlayerPanel
        for i,p in enumerate(self.player_panels):
            if i == 0:
                p.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
            else:
                p.resize(p.get_w()*0.7,p.get_h()*0.7)
                if i == 1 or i == 2:
                    p.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT,-p.get_w() / 5,0,self.player_panels[i-1])
                elif i == 3:
                    p.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT,p.get_w() / 5,0,self.player_panels[0])
                elif i == 4:
                    p.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT,p.get_w() / 5,0,self.player_panels[i-1])

        from GUI.CombatScreen import CombatScreen,FRAMEPOINT

        self.combat_screen = CombatScreen(self.screen.get_w(),self.screen.get_h(),self.screen)
        self.combat_screen.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.combat_screen.set_visible(False)

        from GUI.AbilitiesPanel import AbilitiesPanel

        self.abilities_panel = AbilitiesPanel()
        self.abilities_panel.reload()

        from GUI.RewardScreen import RewardScreen

        self.reward_screen = RewardScreen(self.screen.get_w(),self.screen.get_h(),self.screen)
        self.reward_screen.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.reward_screen.set_visible(False)

        from GUI.PlayerScoreWidget import PlayerScoreWidget

        self.score_widgets: list[PlayerScoreWidget] = []

        for p in self.players.get_all():
            sw = PlayerScoreWidget(self.screen.get_w()*0.17,self.screen.get_h()*0.06,self.screen)
            if len(self.score_widgets) > 0:
                sw.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.BOTTOMLEFT,0,0,self.score_widgets[len(self.score_widgets)-1])
            else:
                sw.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)
            self.score_widgets.append(sw)

        self.spawned = True

    def refresh(self):
        if self.spawned:
            self.refresh_players_data()
            self.reload_player_widgets()

    def reload_player_widgets(self):
        for i,d in enumerate(self._players_data):
            self.score_widgets[i].load(d['player'],d['order'])

    def get_abilities_panel(self):
        return self.abilities_panel

    def get_combat_screen(self):
        return self.combat_screen
    
    def get_reward_screen(self):
        return self.reward_screen

    def get_player_panels(self) -> list:
        return self.player_panels

    def get_castle(self):
        return self.castle

    def flush_main_menu(self):
        self.main_menu.destroy()
        del self.main_menu

    def get_screen(self):
        return self.screen
    
    def get_players(self):
        return self.players
    
    def run_timers(self):
        t: Timer
        for t in reversed(self.timers):
            if t.is_alive():
                t._run()
            else:
                self.timers.remove(t)
                t.destroy()

    def register_timer(self,millis: int,loop_operations: List[Tuple[Callable, Tuple]], loops: int = 0, loop_inc_millis: int = 0, exit_operations: List[Tuple[Callable, Tuple]] = []) -> Timer:
        timer = Timer(millis,loop_operations,loops,loop_inc_millis,exit_operations)
        self.timers.append(timer)
        return timer

    def refresh_players_data(self):
        self._players_data = []
        tmp_data = []

        for p in self.players.get_all():
            tmp_data.append(self.get_player_data(p))

        o = 1
        score = 0
        for d in sorted(tmp_data, key=itemgetter('score'), reverse=True):
            if d['score'] < score:
                o += 1
            d['order'] = o
            self._players_data.append(d)
            score = d['score']

    def get_first_players(self) -> list:
        first_players = []

        for d in self._players_data:
            if d['order'] == 1:
                first_players.append(d)

        return first_players

    def get_last_players(self) -> list:
        last_players = []

        if len(self._players_data) > 0:
            last_order = self._players_data[len(self._players_data)-1]['order']

            for d in self._players_data:
                if d['order'] == last_order:
                    last_players.append(d)
        
        return last_players

    def get_players_data(self):
        return self._players_data
        
    def get_player_data(self, p) -> dict:
        from GameLogic.Player import Player

        data = {}

        if isinstance(p,Player):
            h = p.get_hero()
            data['player'] = p
            data['order'] = 1
            data['score'] = h.get_treasure_value() * 10000 + h.get_power() * 100 + h.get_trash_items_count()

        return data


GAME = Game()