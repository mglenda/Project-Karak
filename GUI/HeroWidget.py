from GUI.GraphicComponents import Image,Frame
import GUI._const_framepoints as FRAMEPOINT
from GameLogic.Ability import Ability
from GameLogic.Hero import Hero

class HeroWidget(Image):
    _ability_widgets: list
    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w, h, '_Textures\\Heroes\\Retextured\\Wizard.png', parent)
        self._ability_widgets = []

    def load_hero(self,hero:Hero):
        self.set_texture(hero._background)

        w: Image
        for w in self._ability_widgets:
            w.destroy()
        self._ability_widgets = []

        a: Ability
        for a in hero._abilities:
            self.load_ability(a)
        
        self.attach_ability_widgets()

    def load_ability(self,ability: Ability):
        w = Image(self.get_h()*0.16,self.get_h()*0.16,ability._background,self)
        self._ability_widgets.append(w)
        
    def attach_ability_widgets(self):
        w:Image
        for i,w in enumerate(self._ability_widgets):
            if i == 0:
                w.set_point(att_point=FRAMEPOINT.BOTTOMLEFT,att_point_parent=FRAMEPOINT.BOTTOMLEFT,x_offset=self.get_w()*0.05,y_offset=-self.get_h()*0.025)
            else:     
                w.set_point(att_point=FRAMEPOINT.BOTTOM,att_point_parent=FRAMEPOINT.TOP,y_offset=-self.get_h()*0.01,parent=self._ability_widgets[i-1])    