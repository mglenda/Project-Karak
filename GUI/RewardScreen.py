from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Rect,Image,TextField,FONT_PATH_NUMBERS
from GameLogic.Items import Item,TYPE_KEY,TYPE_SCROLL,TYPE_WEAPON
from GameLogic.Hero import Hero
from GameLogic.Minion import Minion
from GameLogic.Combatiant import Combatiant
from GameLogic.Ability import STAGE_REWARD_GATHER
from GUI.Button import Button,BUTTON_CLASSIC_BLUE
from GUI._const_mouseevents import LEFTCLICK
from Game import GAME
PATH = '_Textures\\PlayerPanel\\'

class RewardButton(Image):
    _item: Item
    _focus_layer: Image
    _selection_image: Image

    def __init__(self,parent: Frame,item: Item) -> None:
        super().__init__(parent.get_h()*0.1, parent.get_h()*0.1, item.get_icon(), parent)
        self._item = item

        self._power_wheel = Image(w=self.get_w()*0.35,h=self.get_h()*0.35,path='_Textures\\PowerWheel.png',parent=self)
        self._power_wheel.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)

        self._power_text = TextField(parent=self._power_wheel,font_size=30,text='1',font_path=FONT_PATH_NUMBERS)
        self._power_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._power_text.resize(self.get_w()*0.24,self.get_h()*0.24)

        pv = item.get_power_wheel_value()
        if pv is not None:
            self._power_wheel.set_visible(True)
            self._power_text.set_text(pv)
        else:
            self._power_wheel.set_visible(False)

        self._focus_layer = Image(w=self.get_w(),h=self.get_h(),parent=self,path = PATH + 'FocusLayer.png')
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._focus_layer.set_visible(False)

        self._selection_image = Image(w=self.get_w()*0.5,h=self.get_h()*0.5,parent=self,path = PATH + 'Confirm.png')
        self._selection_image.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._selection_image.set_visible(False)

        self.register_mouse_event(LEFTCLICK,self.on_click)

        self.set_active(True)

    def toggle(self, toggled: bool = True):
        self._selection_image.set_visible(toggled)
        self.set_active(not toggled)

    def set_active(self, active: bool):
        super().set_active(active)
        if not active:
            self._focus_layer.set_visible(False)

    def get_item(self) -> Item:
        return self._item

    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        super()._on_mouse_leave()

    def on_click(self):
        self.get_parent().select_reward(self)


class InventoryButton(Image):
    _icon: Image
    _type: int
    _focus_layer: Rect
    _active_layer: Rect
    _item: Item

    def __init__(self,parent: Frame,type: int) -> None:
        self._type = type
        background = 'KeySlot.png'
        if type == TYPE_WEAPON:
            background = 'WeaponSlot.png'
        elif type == TYPE_SCROLL:
            background = 'ScrollSlot.png'

        super().__init__(parent.get_h()*0.12, parent.get_h()*0.12, PATH + background, parent)

        self._icon = Image(self.get_w()*0.8,self.get_h()*0.8,'_Textures\\Items\\Retextured\\FrostFist.png',self)
        self._icon.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._power_wheel = Image(w=self.get_w()*0.3,h=self.get_h()*0.3,path='_Textures\\PowerWheel.png',parent=self._icon)
        self._power_wheel.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)

        self._power_text = TextField(parent=self._power_wheel,font_size=30,text='1',font_path=FONT_PATH_NUMBERS)
        self._power_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._power_text.resize(self.get_w()*0.24,self.get_h()*0.24)

        self._power_wheel.set_visible(False)
        self._icon.set_visible(False)

        self._focus_layer = Rect(self.get_w(),self.get_h(),(0,150,0),self)
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._focus_layer.set_alpha(100)

        self._active_layer = Rect(self.get_w(),self.get_h(),(0,150,0),self)
        self._active_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._active_layer.set_alpha(50)

        self._focus_layer.set_visible(False)
        self._active_layer.set_visible(False)

        self.set_active(False)
        self._item = None
        self.register_mouse_event(LEFTCLICK,self.on_click)

    def set_active(self, active: bool):
        super().set_active(active)
        self._active_layer.set_visible(active)
        if not active:
            self._focus_layer.set_visible(False)

    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        super()._on_mouse_leave()

    def get_item(self) -> Item:
        return self._item

    def load_item(self,item: Item):
        self._icon.set_texture(item.get_icon())
        self._icon.set_visible(True)
        self._item = item

        pv = item.get_power_wheel_value()
        if pv is not None:
            self._power_wheel.set_visible(True)
            self._power_text.set_text(pv)
        else:
            self._power_wheel.set_visible(False)

    def on_click(self):
        self.get_parent().select_slot(self)


class RewardScreen(Rect):
    _victor: Hero
    _loser: Combatiant
    _caption: TextField
    _pass_button: Button
    _rewards: list[RewardButton] = []
    _inventory: list[InventoryButton] = []
    _selected_reward: RewardButton
    _leftover: Item

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        self._alpha = 230
        super().__init__(w, h, (0,0,0), parent)

        self._caption = TextField(parent=self,font_size=70,text='Reward')
        self._caption.set_point(FRAMEPOINT.TOP,FRAMEPOINT.TOP,0,self.get_h()*0.025)

        self._pass_button = Button(self.get_h()*0.20,self.get_h()*0.1,BUTTON_CLASSIC_BLUE,self,'Pass',50)
        self._pass_button.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM,0,-self.get_h()*0.025)
        self._pass_button.register_mouse_event(LEFTCLICK,self.reward_pass)
        self._selected_reward = None
        self._leftover = None

    def load(self,victor: Hero, loser: Combatiant = None):
        self._victor = victor
        self._loser = loser
        self.set_visible(True)
        GAME.get_castle().set_stage(STAGE_REWARD_GATHER,victor)

        self.get_rewards()
        self.get_inventory()

        if len(self._rewards) == 1:
            self.select_reward(self._rewards[0])


    def select_reward(self,reward: RewardButton):
        if self._selected_reward is not None:
            self._selected_reward.toggle(False)
        reward.toggle()
        self._selected_reward = reward

        for i in self._inventory:
            if i._type == self._selected_reward.get_item().get_type():
                i.set_active(True)
            else:
                i.set_active(False)

    def select_slot(self,slot: InventoryButton):
        self._leftover = slot.get_item()

        if isinstance(self._loser,Hero):
            self._loser.remove_item(self._selected_reward.get_item())
        
        if self._leftover is not None:
            self._victor.remove_item(self._leftover)

        self._victor.add_item(self._selected_reward.get_item())

        self._victor.set_move_points(0)

        self.finalize()

    def reward_pass(self):
        if self._loser is None or isinstance(self._loser,Minion):
            self._leftover = self._selected_reward.get_item()
        self.finalize()

    def finalize(self):
        if self._leftover is not None:
            self._victor.get_tile().add_placeable(self._leftover)
        else:
            self._victor.get_tile().remove_placeable()

        GAME.get_castle().refresh_player_panels()

        self.close()
        GAME.get_castle().next_action()

    def close(self):
        self.flush()
        self.set_visible(False)

    def flush(self):
        for rb in self._rewards:
            rb.destroy()

        for ib in self._inventory:
            ib.destroy()

        self._rewards: list[RewardButton] = []
        self._inventory: list[InventoryButton] = []

    def get_rewards(self):
        rewards: list[Item] = []
        if isinstance(self._loser,Minion):
            rewards.append(self._loser.get_reward())
        elif isinstance(self._loser,Hero):
            rewards = self._loser.get_items()
        elif self._loser is None:
            rewards.append(self._victor.get_tile().get_placeable())

        for i,r in enumerate(rewards):
            rb = RewardButton(self,r)
            self._rewards.append(rb)
            if (i + 5) % 5 == 0:
                if i == 0:
                    x_off = 4 if len(rewards) >= 5 else len(rewards) - 1 
                    rb.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,-self.get_h()*0.055*x_off,-self.get_h()*0.32)
                else:
                    rb.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,rb.get_h()*0.1,self._rewards[i-5])
            else:
                rb.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_h()*0.01,0,self._rewards[i-1])
            

    def get_inventory(self):
        for i,s in enumerate(self._victor.get_scrolls()):
            ib = InventoryButton(self,TYPE_SCROLL)
            if s is not None:
                ib.load_item(s)
            self._inventory.append(ib)
            if i == 0:
                ib.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,-ib.get_w(),self.get_h()*0.1)
            else:
                ib.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,0,0,self._inventory[i-1])
        
        i = 0
        for w in self._victor.get_weapons():
            ib = InventoryButton(self,TYPE_WEAPON)
            if w is not None:
                ib.load_item(w)
            self._inventory.append(ib)
            ib.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,0,self._inventory[i])
            i+=1

        for k in self._victor.get_keys():
            ib = InventoryButton(self,TYPE_KEY)
            if k is not None:
                ib.load_item(k)
            self._inventory.append(ib)
            ib.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,0,self._inventory[i])
            i+=1
            
