from GUI.Button import Button,BUTTON_CLASSIC_RED
from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Image,TextField
from GUI.HeroWidget import HeroWidget
from GameLogic.Player import Player

class PlayerWidget(Image):
    _player: Player
    _player_name_background: Image
    _player_name_text: TextField
    _hero_panel_background: Image
    _hero_widget: HeroWidget
    _delete_button: Button
    def __init__(self, w: int, h: int,player: Player, parent: Frame):
        super().__init__(w, h*1.2,'_Textures\\Transparent.png', parent)
        
        self._player_name_background = Image(w,h*0.2,'_Textures\\PlayerName.png',self)
        self._player_name_background.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)

        self._player_name_text = TextField(font_color=(255,215,0),font_size=15,text=player.get_name(),parent=self)
        self._player_name_text.set_point(att_point=FRAMEPOINT.CENTER,att_point_parent=FRAMEPOINT.CENTER,parent=self._player_name_background)

        self._hero_panel_background = Image(w,h,'_Textures\\HeroPanel.png',self)
        self._hero_panel_background.set_point(att_point=FRAMEPOINT.TOPLEFT,att_point_parent=FRAMEPOINT.BOTTOMLEFT,parent=self._player_name_background)

        self._hero_widget = HeroWidget(w*0.8,h*0.8,self)
        self._hero_widget.set_point(att_point=FRAMEPOINT.CENTER,att_point_parent=FRAMEPOINT.CENTER,parent=self._hero_panel_background)

        self._delete_button = Button(w*0.3,h*0.1,BUTTON_CLASSIC_RED,self,'Delete',16)
        self._delete_button.set_point(att_point=FRAMEPOINT.BOTTOM,att_point_parent=FRAMEPOINT.BOTTOM,y_offset=-h*0.01,parent=self._hero_panel_background)
        
        self._player = player
        self._hero_widget.load_hero(player.get_hero())

        self.set_active(True)

    def get_player(self):
        return self._player
    
    def get_delete_button(self):
        return self._delete_button