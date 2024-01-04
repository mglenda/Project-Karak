import pygame

pygame.init()

class Game():
    def __init__(self) -> None:
        pass

    def start(self):
        from GUI.MainScreen import MainScreen
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = MainScreen(self.screen_width,self.screen_height) 

        from PlayerGroup import PlayerGroup
        self.players = PlayerGroup()

    def get_screen(self):
        return self.screen
    
    def get_players(self):
        return self.players

GAME = Game()