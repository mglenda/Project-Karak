from GraphicComponents.InventorySlot import InventorySlot,FRAMEPOINT,Frame
from GameEngine.Constants import ItemTypes
from Interfaces.HeroInterface import HeroInterface

class InventoryPanel():
    slots: list[InventorySlot]
    parent: Frame
    att_point: int
    att_point_parent: int
    x_offset: int
    y_offset: int

    def __init__(self, parent: Frame, att_point: int, att_point_parent: int, x_offset: int = 0, y_offset: int = 0) -> None:
        self.slots: list[InventorySlot] = []
        self.parent: Frame = parent
        self.att_point = att_point
        self.att_point_parent = att_point_parent
        self.x_offset = x_offset
        self.y_offset = y_offset

    def verify(self, hero: HeroInterface) -> bool:
        slots = []
        for slot in self.slots:
            slots.append(slot.slot)
        for s in hero.inventory.slots:
            if s not in slots:
                return False
        return True
    
    def reload(self, hero: HeroInterface):
        for s in self.slots:
            s.destroy()
        self.slots.clear()

        w,h = self.parent.get_h() * 0.25,self.parent.get_h() * 0.25

        scroll_slots = hero.inventory.get_slots_by_type(ItemTypes.SCROLL)

        for i,ss in enumerate(scroll_slots):
            slot = InventorySlot(w,h,(0,0,0),self.parent,ss)
            if i == 0:
                slot.set_point(self.att_point,self.att_point_parent,self.x_offset,self.y_offset)
            else:
                slot.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self.slots[i-1])

            self.slots.append(slot)

        key_slots = hero.inventory.get_slots_by_type(ItemTypes.KEY)

        for i,ks in enumerate(key_slots):
            slot = InventorySlot(w,h,(0,0,0),self.parent,ks)
            if i == 0:
                if len(self.slots) == 0:
                    slot.set_point(self.att_point,self.att_point_parent,self.x_offset,self.y_offset)
                else:
                    slot.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT,0,0,self.slots[0])
            else:
                slot.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self.slots[len(self.slots) - 1])

            self.slots.append(slot)

        weapon_slots = hero.inventory.get_slots_by_type(ItemTypes.WEAPON)

        for i,ws in enumerate(weapon_slots):
            slot = InventorySlot(w,h,(0,0,0),self.parent,ws)
            if i == 0 and len(self.slots) == 0:
                slot.set_point(self.att_point,self.att_point_parent,self.x_offset,self.y_offset)
            elif i == 0 and len(key_slots) == 0:
                slot.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT,0,0,self.slots[0])
            else:
                slot.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,0,self.slots[len(self.slots) - 1])

            self.slots.append(slot)

    def update(self, hero: HeroInterface):
        if not self.verify(hero):
            self.reload(hero)
        for s in self.slots:
            s.update()