from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.NumberImage import NumberImage

class HeroPortrait(Image):
    stats_frame: Rect
    move_icon: Image
    health_icon: Image
    move_number: NumberImage
    move_mid_icon: NumberImage
    move_max_number: NumberImage
    hp_number: NumberImage
    hp_mid_icon: NumberImage
    hp_max_number: NumberImage

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w,h,'_Textures\\Heroes\\Retextured\\Acrobat.png',parent)

        self.stats_frame = Rect(self.w,self.h*0.4,(0,0,0),self)
        self.stats_frame.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
        self.stats_frame.set_alpha(180)

        self.move_icon = Image(self.h*0.1,self.h*0.1,'_Textures\\HeroPanel\\MovePoints.png',self)
        self.move_icon.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.CENTER,self.h*0.1,-self.h*0.025,self.stats_frame)

        self.move_mid_icon = NumberImage(self.h*0.08,self.h*0.08,1000,"White",self)
        self.move_mid_icon.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.h*0.035,self.move_icon)

        self.move_number = NumberImage(self.h*0.08,self.h*0.08,4,"White",self)
        self.move_number.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,self.h*0.015,0,self.move_mid_icon)

        self.move_max_number = NumberImage(self.h*0.08,self.h*0.08,4,"White",self)
        self.move_max_number.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,-self.h*0.015,0,self.move_mid_icon)

        self.health_icon = Image(self.h*0.1,self.h*0.1,'_Textures\\HeroPanel\\HitPoints_Green.png',self)
        self.health_icon.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.CENTER,-self.h*0.1,-self.h*0.025,self.stats_frame)

        self.hp_mid_icon = NumberImage(self.h*0.08,self.h*0.08,1000,"Green",self)
        self.hp_mid_icon.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.h*0.035,self.health_icon)

        self.hp_number = NumberImage(self.h*0.08,self.h*0.08,5,"Green",self)
        self.hp_number.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,self.h*0.015,0,self.hp_mid_icon)

        self.hp_max_number = NumberImage(self.h*0.08,self.h*0.08,5,"Green",self)
        self.hp_max_number.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,-self.h*0.015,0,self.hp_mid_icon)

    def set_hp_values(self, hp: int, hp_max: int):
        if hp <= 0 or hp_max / hp > 2:
            color = 'Red'
        else:
            color = 'Green'
        self.hp_mid_icon.set_color(color)
        self.hp_number.change(color,hp)
        self.hp_max_number.change(color,hp_max)

    def set_move_values(self, ms: int, ms_max: int):
        self.move_number.set_value(ms)
        self.move_max_number.set_value(ms_max)