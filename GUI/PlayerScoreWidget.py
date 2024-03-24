from GUI.Frame import Frame
from GUI.GraphicComponents import Rect,FRAMEPOINT,Image,TextField,FONT_PATH_NUMBERS
from GameLogic.Player import Player

class PlayerScoreWidget(Rect):
    _order_text: TextField
    _hero_icon: Image
    _player_name: TextField
    _chest_icon: Image
    _chest_text: TextField

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        self._alpha = 0
        super().__init__(w, h, (255,255,255), parent)

        self._order_text = TextField(parent=self,text='1.',font_size=35,font_color=(255,255,255))
        self._order_text.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.LEFT,self.get_w()*0.025)

        self._hero_icon = Image(self.get_h()*0.9,self.get_h()*0.9,'_Textures\\Heroes\\MyIcons\\Acrobat.png',self)
        self._hero_icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_w()*0.025,0,self._order_text)

        self._player_name = TextField(parent=self,text='Player',font_size=30,font_color=(255,255,255))
        self._player_name.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_w()*0.025,0,self._hero_icon)

        self._chest_icon = Image(self.get_h()*0.8,self.get_h()*0.8,'_Textures\\PlayerPanel\\ChestIcon.png',self)
        self._chest_icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_w()*0.12,0,self._player_name)

        self._chest_text = TextField(parent=self,text = '1.0',font_size=30)
        self._chest_text.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_w()*0.025,0,self._chest_icon)


    def load(self,p: Player,order: int, ):
        self._order_text.set_text(str(order) + '.')
        self._hero_icon.set_texture(p.get_hero().get_icon())
        self._player_name.set_text(p.get_name())
        self._chest_text.set_text(str(p.get_hero().get_treasure_value()))
