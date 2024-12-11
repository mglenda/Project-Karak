
from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.TextField import TextField
from GraphicsEngine.NumberImage import NumberImage
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class DamageIndicator(Rect):
    icon: Image
    text: NumberImage
    def __init__(self, w: int, h: int,img_path: str,font_color: str, parent: Frame, type_id: int) -> None:
        super().__init__(w, h, (80,80,80), parent)

        self.icon = Image(h,h,img_path,self)
        self.icon.set_point(FRAMEPOINT.TOPRIGHT if type_id == 0 else FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPRIGHT if type_id == 0 else FRAMEPOINT.TOPLEFT)

        self.text = NumberImage(h,h,0,font_color,self)
        self.text.set_point(FRAMEPOINT.RIGHT if type_id == 0 else FRAMEPOINT.LEFT,FRAMEPOINT.LEFT if type_id == 0 else FRAMEPOINT.RIGHT,w* (-0.1 if type_id == 0 else 0.1),0,self.icon)

    def set_alpha(self, alpha: int):
        self.alpha = 0
        self.refresh_surface()
        self.surface.set_alpha(0)
        for c in self.children:
                c.set_alpha(alpha)

    def set_value(self,value: int):
        self.text.set_value(value)

class DuelistScreen(Rect):
    portrait: Image
    ability_indicator: DamageIndicator
    base_indicator: DamageIndicator
    dice_indicator: DamageIndicator
    scroll_indicator: DamageIndicator
    total_text: NumberImage
    total_circle: Image

    def __init__(self, w: int, h: int, color: tuple, parent: Frame, type_id: int) -> None:
        super().__init__(w, h, color, parent)

        self.portrait = Image(h,h,'_Textures\\Heroes\\Combat\\BeastHunter.png',self)
        self.portrait.set_point(FRAMEPOINT.LEFT if type_id == 0 else FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT if type_id == 0 else FRAMEPOINT.RIGHT)

        self.dice_indicator = DamageIndicator(w*0.3,h*0.1,'_Textures\\Combat\\Modifier_Dice.png','White',self,type_id)
        self.dice_indicator.set_point(FRAMEPOINT.TOPRIGHT if type_id == 0 else FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPRIGHT if type_id == 0 else FRAMEPOINT.TOPLEFT,w*(-0.08 if type_id == 0 else 0.08),h*0.08)

        self.base_indicator = DamageIndicator(w*0.3,h*0.1,'_Textures\\Combat\\Modifier_Base.png','Red',self,type_id)
        self.base_indicator.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,h*0.02,self.dice_indicator)

        self.ability_indicator = DamageIndicator(w*0.3,h*0.1,'_Textures\\Combat\\Modifier_Ability.png','Green',self,type_id)
        self.ability_indicator.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,h*0.02,self.base_indicator)

        self.scroll_indicator = DamageIndicator(w*0.3,h*0.1,'_Textures\\Combat\\Modifier_Scroll.png','Purple',self,type_id)
        self.scroll_indicator.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,h*0.02,self.ability_indicator)

        self.total_circle = Image(h*0.4,h*0.4,'_Textures\\Combat\\Total_Circle.png',self)
        self.total_circle.set_point(FRAMEPOINT.BOTTOMRIGHT if type_id == 0 else FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT if type_id == 0 else FRAMEPOINT.BOTTOMLEFT,w*(0.04 if type_id == 0 else -0.04),0)

        self.total_text = NumberImage(h*0.2,h*0.2,0,'Gold',self)
        self.total_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,0,0,self.total_circle)

        self.set_alpha(0)
        for c in self.children:
            c.set_alpha(255)

    def update(self,base_value: int = 0,dice_value: int = 0,ability_value: int = 0,scroll_value: int = 0,total_value: int = 0,portrait: str = None):
        self.dice_indicator.set_value(dice_value)
        self.base_indicator.set_value(base_value)
        self.ability_indicator.set_value(ability_value)
        self.scroll_indicator.set_value(scroll_value)
        self.total_text.set_value(total_value)
        if portrait is not None or self.portrait.path != portrait:
            self.portrait.set_texture(portrait)