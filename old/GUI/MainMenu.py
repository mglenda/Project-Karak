from GUI.GraphicComponents import Image,TextField,FRAMEPOINT,Frame
from GUI.Button import Button,BUTTON_CLASSIC_BLUE,BUTTON_CLASSIC_GREEN,BUTTON_CLASSIC_YELLOW,BUTTON_ARROWRIGHT_GREEN,BUTTON_ARROWLEFT_GREEN
import GUI._const_mouseevents as MouseEvents
from GUI._ComponentListeners import KeyBoardListener
import pygame
from GUI.HeroWidget import HeroWidget
from GUI.PlayerWidget import PlayerWidget
from GameLogic.Player import Player
from GameLogic.PlayerGroup import MAXIMUM_PLAYERS
from GameLogic.Hero import Hero
from GameLogic.HeroSelector import HeroSelector
from Game import GAME

class MainMenu(Image,KeyBoardListener):
    _player_widgets: list
    _hero: Hero
    _hero_panel_background: Image
    _hero_widget: HeroWidget
    _player_name_background: Image
    _player_name_text: TextField
    _confirm_button: Button
    _random_button: Button
    _next_button: Button
    _previous_button: Button
    _play_button: Button
    _hero_selector: HeroSelector
    _now: int
    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w, h, '_Textures\\LoadingScreen.jpg', parent)
        self._player_widgets = []
        self._now = pygame.time.get_ticks()
        h = h * 0.5
        w = h / 1.375

        self._hero_panel_background = Image(w,h,'_Textures\\HeroPanel.png',self)
        self._hero_panel_background.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._hero_widget = HeroWidget(w*0.8,h*0.8,self)
        self._hero_widget.set_point(att_point=FRAMEPOINT.CENTER,att_point_parent=FRAMEPOINT.CENTER,parent=self._hero_panel_background)

        h = h / 3.66

        self._player_name_background = Image(w,h,'_Textures\\PlayerName.png',self)
        self._player_name_background.set_point(att_point=FRAMEPOINT.BOTTOM,att_point_parent=FRAMEPOINT.TOP,parent=self._hero_panel_background)

        self._player_name_text = TextField(font_size=35,text='Player 1',parent=self._player_name_background,max_length=8)
        self._player_name_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._confirm_button = Button(w=w/1.39,h=h/1.74,button_style=BUTTON_CLASSIC_GREEN,parent=self,text='Confirm',font_size=45)
        self._confirm_button.set_point(att_point=FRAMEPOINT.TOP,att_point_parent=FRAMEPOINT.BOTTOM,parent=self._hero_panel_background,y_offset=25)

        self._random_button = Button(w=w/1.39,h=h/1.74,button_style=BUTTON_CLASSIC_BLUE,parent=self,text='Random',font_size=45)
        self._random_button.set_point(att_point=FRAMEPOINT.TOP,att_point_parent=FRAMEPOINT.BOTTOM,parent=self._confirm_button,y_offset=25)

        self._next_button = Button(w=w/3.22,h=h/1.74,button_style=BUTTON_ARROWRIGHT_GREEN,parent=self)
        self._next_button.set_point(att_point=FRAMEPOINT.LEFT,att_point_parent=FRAMEPOINT.RIGHT,parent=self._hero_panel_background,x_offset=20)

        self._previous_button = Button(w=w/3.22,h=h/1.74,button_style=BUTTON_ARROWLEFT_GREEN,parent=self)
        self._previous_button.set_point(att_point=FRAMEPOINT.RIGHT,att_point_parent=FRAMEPOINT.LEFT,parent=self._hero_panel_background,x_offset=-20)

        self._play_button = Button(w=w,h=h,text='PLAY',button_style=BUTTON_CLASSIC_YELLOW,font_size=45,parent=self)
        self._play_button.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT,-20,-20)
        self._play_button.set_visible(False)

        self._hero_selector = HeroSelector()
        self.next_hero()

        self._next_button.register_mouse_event(MouseEvents.LEFTCLICK,self.next_hero)
        self._previous_button.register_mouse_event(MouseEvents.LEFTCLICK,self.prev_hero)
        self._confirm_button.register_mouse_event(MouseEvents.LEFTCLICK,self.confirm_hero)
        self._random_button.register_mouse_event(MouseEvents.LEFTCLICK,self.random_hero)
        self._play_button.register_mouse_event(MouseEvents.LEFTCLICK,GAME.spawn)

        self.set_active(True)

    def confirm_hero(self):
        if GAME.players.get_count() < MAXIMUM_PLAYERS:
            name = self._player_name_text.get_text()
            if len(name) == 0:
                return
            p = Player(name)
            GAME.players.add(p)
            p.set_hero(self._hero(p))
            self.create_player_widget(p)
            self._player_name_text.set_text('Player')   
            if GAME.players.get_count() >= 2:
                self._play_button.set_visible(True)

    def random_hero(self):
        self._hero = self._hero_selector.get_random()
        self._hero_widget.load_hero(self._hero)
        self.confirm_hero()

    def next_hero(self):
        self._hero = self._hero_selector.get_next()
        self._hero_widget.load_hero(self._hero)

    def prev_hero(self):
        self._hero = self._hero_selector.get_previos()
        self._hero_widget.load_hero(self._hero)

    def remove_player_widget(self,player: Player):
        w:PlayerWidget
        for w in self._player_widgets:
            if w.get_player() == player:
                w.destroy()
                self._player_widgets.remove(w)
                GAME.players.remove(player)
                break
        self.attach_player_widets()
        if GAME.players.get_count() < 2:
            self._play_button.set_visible(False)

    def create_player_widget(self,player: Player):
        widget = PlayerWidget(self._hero_panel_background.get_w()*0.45,self._hero_panel_background.get_h()*0.45,player,self)
        self._player_widgets.append(widget)
        self.attach_player_widets()
        widget.get_delete_button().register_mouse_event(MouseEvents.LEFTCLICK,self.remove_player_widget,player)

    def attach_player_widets(self):
        w:PlayerWidget
        for i,w in enumerate(self._player_widgets):
            if i == 0:
                w.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)
            else:
                if i % 2 == 0:
                    w.set_point(att_point=FRAMEPOINT.TOP,att_point_parent=FRAMEPOINT.BOTTOM,parent=self._player_widgets[i-2])
                else:
                    w.set_point(att_point=FRAMEPOINT.LEFT,att_point_parent=FRAMEPOINT.RIGHT,parent=self._player_widgets[i-1])

    def _on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        now = pygame.time.get_ticks()
        if now - self._now >= 50:
            self._now = now
            if keys[pygame.K_BACKSPACE]:
                self._player_name_text.set_text(self._player_name_text.get_text()[:-1])
            else:
                self._player_name_text.set_text(self._player_name_text.get_text() + unicode)
    
    def _on_key_pressed(self, key: int, unicode: str):
        self._now = pygame.time.get_ticks() + 200
        if key == pygame.K_BACKSPACE:
            self._player_name_text.set_text(self._player_name_text.get_text()[:-1])
        else:
            self._player_name_text.set_text(self._player_name_text.get_text() + unicode)