import pygame
import GUI.Graphics as G

class MainScreen(G.Panel):
    is_shift_hold: bool
    text_input: G.TextField

    def __init__(self, w, h) -> None:
        self.last_hold = pygame.time.get_ticks()
        self.is_shift_hold = False
        self.text_input = None
        super().__init__(w=w, h=h, rgb=(0,0,0), surface=pygame.display.set_mode((w,h),pygame.FULLSCREEN))
        self.set_abs_point(0,0)

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
            if now - self.last_hold >= 50 and self.text_input is not None:
                self.last_hold = now
                self.text_input.set_text(self.text_input.get_text()[:-1])
    
    def _on_key_pressed(self, key: int):
        if key == pygame.K_LSHIFT:
            self.is_shift_hold = True
        if self.text_input is not None:
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

    # self.register_mouse_event(Behaviors.EVENT_MOUSE_ENTER,print,'enter')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_LEAVE,print,'leave')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_LEFTCLICK,print,'left_click')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_RIGHTCLICK,print,'right_click')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELUP,print,'wheel_up')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELDOWN,print,'wheel_down')
    # self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELCLICK,print,'wheel_click')

class Main():
    screen_width: int
    screen_height: int
    screen: MainScreen
    def __init__(self) -> None:
        self.screen_width = pygame.display.Info().current_w
        self.screen_height = pygame.display.Info().current_h
        self.screen = MainScreen(self.screen_width,self.screen_height)
        self.main_menu = MainMenu(self,self.screen_width,self.screen_height)
        self.screen.add(self.main_menu,G.ATTPOINT_TOPLEFT,G.ATTPOINT_TOPLEFT)

    def get_screen(self) -> MainScreen:
        return self.screen

    def draw(self):
        self.screen.draw()

    def _on_mouse_right_click(self,x,y):
        self.screen._on_mouse_right_click(x,y)

    def _on_mouse_left_click(self,x,y):
        self.screen._on_mouse_left_click(x,y)

    def _on_mouse_wheel_up(self,x,y):
        self.screen._on_mouse_wheel_up(x,y)

    def _on_mouse_wheel_down(self,x,y):
        self.screen._on_mouse_wheel_down(x,y)

    def _on_mouse_motion(self,x,y):
        self.screen._on_mouse_motion(x,y)

    def _on_mouse_wheel_click(self,x,y):
        self.screen._on_mouse_wheel_click(x,y)

    def _on_key_hold(self, key: int):
        self.screen._on_key_hold(key)
    
    def _on_key_pressed(self, key: int):
        self.screen._on_key_pressed(key)
    
    def _on_key_released(self, key: int):
        self.screen._on_key_released(key)

class MainMenu(G.Panel):
    def __init__(self, main:Main, w=0, h=0, rgb=(0,0,0)) -> None:
        super().__init__(w, h, rgb)
        self.background = G.Image(w,h,'Textures\\LoadingScreen.jpg')
        self.add(self.background,G.ATTPOINT_TOPLEFT,G.ATTPOINT_TOPLEFT)
        self.main = main

        h = h * 0.5
        w = h / 1.375
        self.hero_panel_background = G.Image(w,h,'Textures\\HeroPanel.png')
        self.add(self.hero_panel_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER,y_offset=h*0.1)

        h = h / 3.66

        self.player_name_background = G.Image(w,h,'Textures\\PlayerName.png')
        self.add(self.player_name_background)
        self.player_name_background.attach(self.hero_panel_background,G.ATTPOINT_TOP,G.ATTPOINT_BOTTOM)

        self.player_name_text = G.TextField(font_rgb=(255,215,0),font_size=45,text='Player 1')
        self.add(self.player_name_text)
        self.player_name_text.attach(self.player_name_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)
        self.main.get_screen().set_text_input(self.player_name_text)