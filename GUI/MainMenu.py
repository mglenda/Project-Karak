import GUI.Graphics as G
from GUI.Buttons import Button,BUTTON_ARROWLEFT_GREEN,BUTTON_ARROWRIGHT_GREEN,BUTTON_CLASSIC_BLUE,BUTTON_CLASSIC_RED
from Player import Player
from GUI.Behaviors import EVENT_MOUSE_LEFTCLICK
from HeroSelector import HeroSelector
from Hero import Hero
from PlayerGroup import MAXIMUM_PLAYERS
from Game import GAME
import GUI.Behaviors as MouseEvents

class PlayerWidget(G.Panel):
    player:Player
    def __init__(self, w=0, h=0,player: Player = None):
        super().__init__(w, h*1.2, img_path = 'Textures\\Transparent.png')
        
        self.player_name_background = G.Image(w,h*0.2,'Textures\\PlayerName.png')
        self.add(self.player_name_background,G.ATTPOINT_TOPLEFT,G.ATTPOINT_TOPLEFT)

        self.player_name_text = G.TextField(font_rgb=(255,215,0),font_size=20,text=player.get_name())
        self.add(self.player_name_text)
        self.player_name_text.attach(self.player_name_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

        self.hero_panel_background = G.Image(w,h,'Textures\\HeroPanel.png')
        self.add(self.hero_panel_background)
        self.hero_panel_background.attach(self.player_name_background,G.ATTPOINT_BOTTOMLEFT,G.ATTPOINT_TOPLEFT)

        self.hero_image = G.Image(w=w*0.8,h=h*0.8,filepath=player.get_hero()._background)
        self.add(self.hero_image)
        self.hero_image.attach(self.hero_panel_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

        self.delete_button = Button(w=w*0.3,h=h*0.1,text='Delete',font_size=16,button_style=BUTTON_CLASSIC_RED)
        self.add(self.delete_button)
        self.delete_button.attach(self.hero_panel_background,G.ATTPOINT_BOTTOM,G.ATTPOINT_BOTTOM,0,-h*0.01)

        self.player = player


class MainMenu(G.Panel):
    player_widgets = []
    hero:Hero
    def __init__(self, w=0, h=0) -> None:
        super().__init__(w, h, img_path = 'Textures\\LoadingScreen.jpg')

        h = h * 0.5
        w = h / 1.375
        self.hero_panel_background = G.Image(w,h,'Textures\\HeroPanel.png')
        self.add(self.hero_panel_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

        self.hero_image = G.Image(w=w*0.8,h=h*0.8,filepath='Textures\\Heroes\\Retextured\\Wizard.png')
        self.add(self.hero_image)
        self.hero_image.attach(self.hero_panel_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

        h = h / 3.66

        self.player_name_background = G.Image(w,h,'Textures\\PlayerName.png')
        self.add(self.player_name_background)
        self.player_name_background.attach(self.hero_panel_background,G.ATTPOINT_TOP,G.ATTPOINT_BOTTOM)

        self.player_name_text = G.TextField(font_rgb=(255,215,0),font_size=45,text='Player 1')
        self.add(self.player_name_text)
        self.player_name_text.attach(self.player_name_background,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

        self.confirm_buttom = Button(w=w/1.39,h=h/1.74,text='Confirm',font_size=45)
        self.add(self.confirm_buttom)
        self.confirm_buttom.attach(self.hero_panel_background,G.ATTPOINT_BOTTOM,G.ATTPOINT_TOP,0,25)

        self.random_buttom = Button(w=w/1.39,h=h/1.74,text='Random',button_style=BUTTON_CLASSIC_BLUE,font_size=45)
        self.add(self.random_buttom)
        self.random_buttom.attach(self.confirm_buttom,G.ATTPOINT_BOTTOM,G.ATTPOINT_TOP,y_offset=25)

        self.next_button = Button(w=w/3.22,h=h/1.74,button_style=BUTTON_ARROWRIGHT_GREEN)
        self.add(self.next_button)
        self.next_button.attach(self.hero_panel_background,G.ATTPOINT_RIGHT,G.ATTPOINT_LEFT,x_offset = 20)

        self.previous_button = Button(w=w/3.22,h=h/1.74,button_style=BUTTON_ARROWLEFT_GREEN)
        self.add(self.previous_button)
        self.previous_button.attach(self.hero_panel_background,G.ATTPOINT_LEFT,G.ATTPOINT_RIGHT,x_offset= -20)

        self.hero_selector = HeroSelector()
        self.next_hero()

        self.next_button.register_mouse_event(MouseEvents.EVENT_MOUSE_LEFTCLICK,self.next_hero)
        self.previous_button.register_mouse_event(MouseEvents.EVENT_MOUSE_LEFTCLICK,self.prev_hero)
        self.confirm_buttom.register_mouse_event(MouseEvents.EVENT_MOUSE_LEFTCLICK,self.confirm_hero)
        self.random_buttom.register_mouse_event(MouseEvents.EVENT_MOUSE_LEFTCLICK,self.random_hero)

    def confirm_hero(self):
        if GAME.players.get_count() < MAXIMUM_PLAYERS:
            name = self.player_name_text.get_text()
            if len(name) == 0:
                return
            p = Player(name)
            GAME.players.add(p)
            p.set_hero(self.hero())
            self.create_player_widget(p)
            self.player_name_text.set_text('Player')   

    def random_hero(self):
        self.hero:Hero = self.hero_selector.get_random()
        self.hero_image.change_image(self.hero._background)
        self.confirm_hero()

    def next_hero(self):
        self.hero:Hero = self.hero_selector.get_next()
        self.hero_image.change_image(self.hero._background)

    def prev_hero(self):
        self.hero:Hero = self.hero_selector.get_previos()
        self.hero_image.change_image(self.hero._background)

    def create_player_widget(self,player:Player):
        widget = PlayerWidget(self.hero_panel_background.get_surface().get_width()*0.45,self.hero_panel_background.get_surface().get_height()*0.45,player)
        self.add(widget)
        self.player_widgets.append(widget)
        self.attach_player_widets()
        widget.delete_button.register_mouse_event(EVENT_MOUSE_LEFTCLICK,self.remove_player_widget,player)

    def attach_player_widets(self):
        w:PlayerWidget
        for i,w in enumerate(self.player_widgets):
            if i == 0:
                w.attach(self,G.ATTPOINT_TOPLEFT,G.ATTPOINT_TOPLEFT)
            else:
                if i % 2 == 0:
                    w.attach(self.player_widgets[i-2],G.ATTPOINT_BOTTOM,G.ATTPOINT_TOP)
                else:
                    w.attach(self.player_widgets[i-1],G.ATTPOINT_RIGHT,G.ATTPOINT_LEFT)

    def remove_player_widget(self,player:Player):
        w:PlayerWidget
        for w in self.player_widgets:
            if w.player == player:
                self.remove(w)
                self.player_widgets.remove(w)
                GAME.players.remove(player)
                break
        self.attach_player_widets()