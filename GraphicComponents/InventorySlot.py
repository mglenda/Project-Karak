from __future__ import annotations

from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicsEngine.ItemImage import ItemImage
from GameEngine.Constants import ItemTypes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from GameEngine.InventorySlot import InventorySlot as EngineInventorySlot

PATH = '_Textures\\Inventory\\'

class InventorySlot(Rect):
    selection_layer: Rect
    hover_layer: Rect
    theme: Image
    itemimg: ItemImage
    slot: EngineInventorySlot

    def __init__(self, w: int, h: int, color: tuple, parent: Frame, slot: EngineInventorySlot) -> None:
        super().__init__(w, h, color, parent)
        self.slot = slot

        self.selection_layer = Rect(self.w,self.h,(255,215,0),self)
        self.selection_layer.set_alpha(90)
        self.selection_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.selection_layer.set_visible(False)
        self.selection_layer.set_active(False)

        self.hover_layer = Rect(self.w,self.h,(255,255,255),self)
        self.hover_layer.set_alpha(55)
        self.hover_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.hover_layer.set_visible(False)
        self.hover_layer.set_active(False)

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

    def set_selected(self, selected: bool):
        self.selection_layer.set_visible(selected)

    def set_hovered(self, hovered: bool):
        self.hover_layer.set_visible(hovered)

    def update(self):
        if self.slot.get_item() is not None:
            color = 'Red' if self.slot.get_item().type == ItemTypes.WEAPON else 'Gold'
            self.itemimg.change(self.slot.get_item().get_path(),color,self.slot.get_item().get_power())
            self.itemimg.set_visible(True)
        else:
            self.itemimg.set_visible(False)
