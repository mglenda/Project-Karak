from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.NumberImage import NumberImage
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class Placeable(Image):
    wheel_img: Image
    wheel_txt: NumberImage

    def __init__(self, w: int, h: int, path: str, parent: Frame) -> None:
        super().__init__(w, h, path, parent)

        self.wheel_img = Image(w=self.w*0.55,h=self.h*0.55,path='_Textures\\Minions\\PowerWheel.png',parent=self)
        self.wheel_img.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT)

        self.wheel_txt = NumberImage(w=self.w*0.35,h=self.h*0.35,color="Gold",value=0,parent=self.wheel_img)
        self.wheel_txt.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        
    def set_wheel_value(self, value: int):
        self.wheel_txt.set_value(value)

    def show_wheel(self):
        self.wheel_img.set_visible(True)

    def hide_wheel(self):
        self.wheel_img.set_visible(False)