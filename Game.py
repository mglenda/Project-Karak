import pygame
from GameLogic.Timer import Timer
from typing import Callable, List, Tuple

pygame.init()

class Game():
    def __init__(self) -> None:
        pass

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

        from GUI.Dice import DiceImages
        DiceImages._load()

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

        self.combat_screen = CombatScreen(self.screen.get_h(),self.screen.get_h(),self.screen)
        self.combat_screen.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.combat_screen.set_visible(False)

        from GUI.AbilitiesPanel import AbilitiesPanel

        self.abilities_panel = AbilitiesPanel()
        self.abilities_panel.reload()

        from GUI.RewardScreen import RewardScreen

        self.reward_screen = RewardScreen(self.screen.get_h(),self.screen.get_h(),self.screen)
        self.reward_screen.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.reward_screen.set_visible(False)

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

    def register_timer(self,millis: int,loop_operations: List[Tuple[Callable, Tuple]], loops: int = 0, loop_inc_millis: int = 0, exit_operations: List[Tuple[Callable, Tuple]] = []):
        self.timers.append(Timer(millis,loop_operations,loops,loop_inc_millis,exit_operations))
        
GAME = Game()