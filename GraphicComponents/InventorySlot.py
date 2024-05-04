from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.ItemImage import ItemImage
from GameEngine.Constants import ItemTypes
from Interfaces.InventorySlotInterface import InventorySlotInterface

PATH = '_Textures\\Inventory\\'

class InventorySlot(Rect):
    theme: Image
    itemimg: ItemImage
    slot: InventorySlotInterface

    def __init__(self, w: int, h: int, color: tuple, parent: Frame, slot: InventorySlotInterface) -> None:
        super().__init__(w, h, color, parent)
        self.slot = slot

        path = PATH + 'ScrollSlot.png'
        if slot.get_type() == ItemTypes.KEY:
            path = PATH + 'KeySlot.png'
        elif slot.get_type() == ItemTypes.WEAPON:
            path = PATH + 'WeaponSlot.png'

        self.theme = Image(self.w*0.6,self.h*0.6,path,self)
        self.theme.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.set_alpha(200)

        self.itemimg = ItemImage(self.w*0.9,self.h*0.9,'_Textures\\Items\\Retextured\\Axe.png',self,"Red",0)
        self.itemimg.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.itemimg.set_visible(False)

    def update(self):
        if self.slot.get_item() is not None:
            color = 'Red' if self.slot.get_item().type == ItemTypes.WEAPON else 'Gold'
            self.itemimg.change(self.slot.get_item().get_path(),color,self.slot.get_item().get_power())
            self.itemimg.set_visible(True)
        else:
            self.itemimg.set_visible(False)