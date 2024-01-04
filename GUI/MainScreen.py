import pygame
import GUI.Graphics as G
from GUI.MainMenu import MainMenu
from Game import GAME

class MainScreen(G.Panel):
    is_shift_hold: bool
    text_input: G.TextField

    def __init__(self, w, h) -> None:
        self.last_hold = pygame.time.get_ticks()
        self.is_shift_hold = False
        self.text_input = None
        super().__init__(w=w, h=h, rgb=(0,0,0), surface=pygame.display.set_mode((w,h),pygame.FULLSCREEN))
        self.set_abs_point(0,0)

        self.main_menu = MainMenu(w,h)
        self.add(self.main_menu,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)
        self.set_text_input(self.main_menu.player_name_text)

    def set_text_input(self,text_input:G.TextField):
        self.text_input = text_input
    
    def get_text_input(self) -> G.TextField:
        return self.text_input
    
    def clear_text_input(self):
        self.text_input = None

    def _on_key_hold(self, key: int):
        if key == 119 or key == 82:
            #Up
            pass
        if key == 115 or key == 79:
            #Down
            pass
        if key == 97 or key == 80:
            #Left
            pass
        if key == 100 or key == 81:
            #Right
            pass
        if key == 42:
            now = pygame.time.get_ticks()
            if now - self.last_hold >= 150 and self.text_input is not None:
                self.last_hold = now
                self.text_input.set_text(self.text_input.get_text()[:-1])
    
    def _on_key_pressed(self, key: int):
        if key == pygame.K_LSHIFT:
            self.is_shift_hold = True
        if self.text_input is not None:
            if key == pygame.K_BACKSPACE:
                self.last_hold = pygame.time.get_ticks()
                self.text_input.set_text(self.text_input.get_text()[:-1])
            else:
                try:
                    char:str
                    if key >= 97 and key <= 122:
                        char = chr(key - 32 if self.is_shift_hold else key)
                    else:
                        char = chr(key)
                    self.text_input.set_text(self.text_input.get_text() + char)
                except:
                    pass
   
    def _on_key_released(self, key: int):
        if key == pygame.K_LSHIFT:
            self.is_shift_hold = False