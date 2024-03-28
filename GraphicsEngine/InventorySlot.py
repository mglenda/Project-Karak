from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GameEngine.Constants import ItemTypes

PATH = '_Textures\\Inventory\\'

class InventorySlot(Rect):
    theme: Image
    type: int

    def __init__(self, w: int, h: int, color: tuple, parent: Frame, type: int) -> None:
        super().__init__(w, h, color, parent)
        self.type = type

        path = PATH + 'ScrollSlot.png'
        if type == ItemTypes.KEY:
            path = PATH + 'KeySlot.png'
        elif type == ItemTypes.WEAPON:
            path = PATH + 'WeaponSlot.png'

        self.theme = Image(self.w*0.6,self.h*0.6,path,self)
        self.theme.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)