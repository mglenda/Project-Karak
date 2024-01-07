import pygame

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

    def spawn(self):
        from GUI.CastleScreen import CastleScreen
        self.flush_main_menu()
        self.castle = CastleScreen()
        self.screen.set_focus(self.castle)

    def get_castle(self):
        return self.castle

    def flush_main_menu(self):
        self.main_menu.destroy()
        del self.main_menu

    def get_screen(self):
        return self.screen
    
    def get_players(self):
        return self.players

GAME = Game()