from GraphicComponents.RewardScreen import RewardScreen,Frame,FRAMEPOINT
from GraphicComponents.InventorySlot import InventorySlot
from GraphicsEngine.ItemImage import ItemImage
from GraphicsEngine.Constants import MouseEvent
from Interfaces.ItemInterface import ItemInterface
from Interfaces.InventorySlotInterface import InventorySlotInterface
from GameEngine.Constants import ItemTypes
from GameEngine.Reward import Reward
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class RewardPanel():
    main: RewardScreen
    item_image: ItemImage
    slots: list[InventorySlot]
    selected_slot: InventorySlotInterface

    def __init__(self,screen: Frame, game: "Game") -> None:
        self.reward_service = game.reward_service
        self.slots = []
        self.current_reward = None
        self.selected_slot = None
        height: int = screen.get_h()
        self.main = RewardScreen(height,height,screen)
        self.main.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
        self.main.set_visible(False)

        self.item_image = ItemImage(height*0.15,height*0.15,'_Textures\\Heroes\\Combat\\BeastHunter.png',self.main,'Red',0)
        self.item_image.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,0,-height*0.2,self.main.background)

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)
        self.clear_slots()
        self.current_reward = None
        self.selected_slot = None

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def get_selected_slot(self) -> InventorySlotInterface:
        return self.selected_slot

    def clear_slots(self):
        for slot in reversed(self.slots):
            slot.destroy()
        self.slots.clear()

    def select_slot(self, slot: InventorySlotInterface):
        self.selected_slot = slot
        for slot_component in self.slots:
            slot_component.set_selected(slot_component.slot == slot)

    def reload_slots(self, reward: Reward):
        self.clear_slots()
        self.selected_slot = None

        item = reward.get_item()
        hero = reward.get_hero()
        slot_size = self.main.get_h() * 0.12
        slot_gap = slot_size * 1.15
        slots_count = len(hero.inventory.slots)
        start_x = -((slots_count - 1) * slot_gap) / 2
        y_offset = self.main.get_h() * 0.28

        for i, slot in enumerate(hero.inventory.slots):
            slot_component = InventorySlot(slot_size,slot_size,(0,0,0),self.main,slot)
            slot_component.set_point(
                FRAMEPOINT.CENTER,
                FRAMEPOINT.CENTER,
                start_x + i * slot_gap,
                y_offset,
                self.main.background
            )
            if slot.verify_type(item.type):
                slot_component.register_mouse_event(MouseEvent.LEFTCLICK,self.select_slot,slot)
                slot_component.register_mouse_event(MouseEvent.ENTER,slot_component.set_hovered,True)
                slot_component.register_mouse_event(MouseEvent.LEAVE,slot_component.set_hovered,False)
                slot_component.set_alpha(220)
            else:
                slot_component.set_alpha(80)
            self.slots.append(slot_component)

    def update(self):
        reward = self.reward_service.get_reward()
        if reward is not None:
            if not self.is_visible():
                self.show()
            if reward != self.current_reward:
                self.current_reward = reward
                self.reload_slots(reward)

            item: ItemInterface = reward.get_item()
            if item is not None:
                color:str = 'Red' if item.type == ItemTypes.WEAPON else 'Gold'
                self.item_image.change(item.get_path(),color,item.get_power())
            for slot in self.slots:
                slot.update()

        else:
            if self.is_visible():
                self.hide()
