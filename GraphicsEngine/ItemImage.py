from GraphicsEngine.Image import Image,Frame
from GraphicsEngine.NumberImage import NumberImage
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT

class ItemImage(Image):
    value_img: NumberImage
    color: str
    value: int

    def __init__(self, w: int, h: int, path: str, parent: Frame, color: str, value: int) -> None:
        super().__init__(w, h, path, parent)

        self.value_img = NumberImage(w=self.w*0.35,h=self.h*0.35,color=color,value=value,parent=self)
        self.value_img.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT,self.value_img.w*0.15,self.value_img.h*0.15)
        self.color = color
        self.value = value
        self.value_img.set_visible(value > 0)
        self.set_alpha(255)
        
    def change(self, path: str, color: str, value: int):
        self.set_texture(path)
        if self.color != color or self.value != value:
            self.value = value
            self.color = color
            self.value_img.change(color,value)
            self.value_img.set_visible(self.value > 0)
            
