from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Image,TextField
from GUI.HeroWidget import HeroWidget
from GameLogic.Player import Player
PATH = '_Textures\\PlayerPanel\\'

class ScrollSlot(Image):
    _icon: Image
    def __init__(self,parent: Frame) -> None:
        super().__init__(parent.get_h()/3.4, parent.get_h()/3.4, PATH + 'ScrollSlot.png', parent)

        self._icon = Image(self.get_w()*0.8,self.get_h()*0.8,'_Textures\\Items\\Retextured\\FrostFist.png',self)
        self._icon._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)


class WeaponSlot(Image):
    _icon: Image
    def __init__(self,parent: Frame) -> None:
        super().__init__(parent.get_h()/3.4, parent.get_h()/3.4, PATH + 'WeaponSlot.png', parent)

        self._icon = Image(self.get_w()*0.8,self.get_h()*0.8,'_Textures\\Items\\Retextured\\Axe.png' ,self)
        self._icon._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)


class KeySlot(Image):
    _icon: Image
    def __init__(self,parent: Frame) -> None:
        super().__init__(parent.get_h()/3.4, parent.get_h()/3.4, PATH + 'KeySlot.png', parent)

        self._icon = Image(self.get_w()*0.8,self.get_h()*0.8,'_Textures\\Items\\Retextured\\Key.png',self)
        self._icon._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

class HealthSlot(Image):
    _icon: Image
    def __init__(self,parent: Frame) -> None:
        super().__init__(parent.get_h()/5.66, parent.get_h()/5.66, PATH + 'HealthSlot.png', parent)

        self._icon = Image(self.get_w()*0.8,self.get_h()*0.8,PATH + 'HealthPositive.png',self)
        self._icon._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

    def set_positive(self):
        self._icon.set_texture(PATH + 'HealthPositive.png')
    
    def set_negative(self):
        self._icon.set_texture(PATH + 'HealthNegative.png')

class PlayerPanel(Image):
    _health_slots: list[HealthSlot]
    _weapon_slots: list[WeaponSlot]
    _key_slot: KeySlot
    _scroll_slots: list[ScrollSlot]
    _hero_widget: HeroWidget
    _hero_background: Image
    _player_name_back: Image
    _player_name_text: TextField
    _player: Player
    def __init__(self,w: int,h: int,parent: Frame) -> None:
        super().__init__(w, h, PATH + 'Background.png', parent)
        h = h*0.88
        self._hero_background = Image(h  / 1.375,h,PATH + 'HeroPanel.png',self)
        self._hero_background.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM,-parent.get_w()*0.028,-parent.get_h()*0.012)

        self._hero_widget = HeroWidget(self._hero_background.get_w()*0.8,self._hero_background.get_h()*0.8,self._hero_background)
        self._hero_widget.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._player_name_back = Image(self.get_w()*0.3,self.get_h()*0.12,PATH + 'Background.png',self)
        self._player_name_back.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,self.get_h()*0.02)

        self._player_name_text = TextField(parent=self._player_name_back,font_size = 20,text='Player')
        self._player_name_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._health_slots = []
        self._weapon_slots = []
        self._scroll_slots = []

        self._key_slot = KeySlot(self)
        self._key_slot.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT,0,0,self._hero_background)

        for i in range(2):
            w_slot = WeaponSlot(self)
            self._weapon_slots.append(w_slot)
            if i == 0:
                w_slot._set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self._key_slot)
            else:
                w_slot._set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self._weapon_slots[i-1])

        for i in range(3):
            s_slot = ScrollSlot(self)
            self._scroll_slots.append(s_slot)
            if i == 0:
                s_slot._set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT,0,0,self._key_slot)
            else:
                s_slot._set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self._scroll_slots[i-1])

        for i in range(5):
            h_slot = HealthSlot(self)
            self._health_slots.append(h_slot)
            if i == 0:
                h_slot._set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT,0,0,self._hero_background)
            else:
                h_slot._set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self._health_slots[i-1])


    def load_player(self,player: Player):
        self._player = player
        self._hero_widget.load_hero(player.get_hero())
        self._player_name_text.set_text(player.get_name())

        hs: HealthSlot
        for i,hs in enumerate(self._health_slots):
            if i >= player.get_hero().get_hit_points():
                hs.set_negative()
            else:
                hs.set_positive()