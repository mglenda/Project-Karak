from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.Rect import Rect
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.NumberImage import NumberImage
from GraphicsEngine.TextColors import TextColors

class HeroPortrait(Image):
    stats_frame: Rect
    move_icon: Image
    health_icon: Image
    move_text: NumberImage
    hp_text: NumberImage

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w,h,'_Textures\\Heroes\\Retextured\\Acrobat.png',parent)

        self.stats_frame = Rect(self.w,self.h*0.4,(0,0,0),self)
        self.stats_frame.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
        self.stats_frame.set_alpha(180)

        self.move_icon = Image(self.h*0.1,self.h*0.1,'_Textures\\HeroPanel\\MovePoints.png',self)
        self.move_icon.set_point(FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.CENTER,self.h*0.1,-self.h*0.025,self.stats_frame)

        self.move_text = NumberImage(self.h*0.26,self.h*0.08,"{current} / {max}",TextColors.WHITE,self)
        self.move_text.set_values(current=4,max=4)
        self.move_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.h*0.035,self.move_icon)

        self.health_icon = Image(self.h*0.1,self.h*0.1,'_Textures\\HeroPanel\\HitPoints_Green.png',self)
        self.health_icon.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.CENTER,-self.h*0.1,-self.h*0.025,self.stats_frame)

        self.hp_text = NumberImage(self.h*0.26,self.h*0.08,"{current} / {max}",TextColors.GREEN,self)
        self.hp_text.set_values(current=5,max=5)
        self.hp_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.h*0.035,self.health_icon)

    def set_hp_values(self, hp: int, hp_max: int):
        if hp <= 0 or hp_max / hp > 2:
            color = TextColors.RED
        else:
            color = TextColors.GREEN
        self.hp_text.set_color(color)
        self.hp_text.set_values(current=hp,max=hp_max)

    def set_move_values(self, ms: int, ms_max: int):
        self.move_text.set_values(current=ms,max=ms_max)
