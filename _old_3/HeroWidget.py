import GUI.Graphics as G
from GameLogic.Ability import Ability
from Hero import Hero

class HeroWidget(G.Panel):
    ability_widgets: list
    def __init__(self, w=0, h=0) -> None:
        super().__init__(w, h, img_path = 'Textures\\Heroes\\Retextured\\Wizard.png')
        self.ability_widgets = []

    def load_hero(self,hero:Hero):
        self.change_background(img_path=hero._background)

        for w in self.ability_widgets:
            self.remove(w)
        self.ability_widgets = []

        a:Ability
        for a in hero._abilities:
            self.load_ability(a)
        
        self.attach_ability_widgets()

    def load_ability(self,ability:Ability):
        ability_w = G.Image(self.h*0.16,self.h*0.16,ability._background)
        self.add(ability_w)
        self.ability_widgets.append(ability_w)

    def attach_ability_widgets(self):
        w:G.Image
        for i,w in enumerate(self.ability_widgets):
            if i == 0:
                w.attach(self,G.ATTPOINT_BOTTOMLEFT,G.ATTPOINT_BOTTOMLEFT,x_offset=self.w*0.05,y_offset=-self.h*0.025)
            else:            
                w.attach(self.ability_widgets[i-1],G.ATTPOINT_TOP,G.ATTPOINT_BOTTOM,y_offset=-self.h*0.01)