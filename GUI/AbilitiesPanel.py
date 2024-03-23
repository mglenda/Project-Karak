from GUI.Frame import Frame
from Game import GAME
from GameLogic.Hero import Hero
from GameLogic.Ability import Ability,STAGE_FIGHT,STAGE_EXPLORING,STAGE_ALWAYS,STAGE_FIGHT_AFTERMATH,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_TURNBEGIN,STAGE_REWARD_GATHER
from GameLogic.Minion import ChestClosed
from GameLogic.Items import Key,Item
from GUI.GraphicComponents import Rect,Image,TextField,FRAMEPOINT
from GUI._const_mouseevents import LEFTCLICK
from GUI.Button import Button,BUTTON_CLASSIC_YELLOW
import GUI._const_mouseevents as MouseEvent

class AbilityButton(Image):
    _ability_icon: Image
    _ability_name: TextField
    _ability_focus_layer: Image
    _focus_layer: Rect
    _press_layer: Rect
    _ability: Ability
    def __init__(self,ability: Ability) -> None:
        w = GAME.get_screen().get_w()*0.11
        h = w / 5
        super().__init__(w, h, '_Textures\\Abilities\\AbilityBorder.png', GAME.get_screen())

        self._ability_icon = Image(h,h,ability.get_icon(),self)
        self._ability_icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.LEFT)
        
        self._ability_name = TextField(self,(255,255,255),16,ability.get_name(),30)
        self._ability_name.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._focus_layer = Image(self.get_w(),self.get_h(),'_Textures\\Abilities\\AbilityBorderFocusLayer.png',self)
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer = Image(self.get_w(),self.get_h(),'_Textures\\Abilities\\AbilityBorderFocusLayer.png',self)
        self._press_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer.set_visible(False)
        self._focus_layer.set_visible(False)

        self._ability = ability

    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(False)
        super()._on_mouse_leave()

    def _on_mouse_left_press(self, x, y):
        self._press_layer.set_visible(True)
        super()._on_mouse_left_press(x, y)

    def _on_mouse_left_click(self, x, y):
        self._press_layer.set_visible(False)
        return super()._on_mouse_left_click(x, y)

class AbilitiesPanel:
    _abilities: list[Ability]
    _buttons: list[AbilityButton]
    _visible: bool
    _pick_item_button: Button

    def __init__(self) -> None:
        self._buttons = []
        self._visible = True

        w = GAME.get_screen().get_w()*0.2
        h = w / 5
        self._pick_item_button = Button(w=w,h=h,button_style=BUTTON_CLASSIC_YELLOW,parent=GAME.get_screen(),text='Pick Up Item',font_size=45)
        self._pick_item_button.set_point(FRAMEPOINT.TOP,FRAMEPOINT.TOP,0,GAME.get_screen().get_h()*0.02)
        self._pick_item_button.set_visible(False)
        self._pick_item_button.register_mouse_event(LEFTCLICK,self.pick_item)

    def pick_item(self):
        GAME.get_castle().get_current_hero().pick_item_from_tile()
        GAME.get_castle().refresh_player_panels()
        self.reload()

    def use_passives(self):
        for a in self._abilities:
            if a.is_passive() and a.is_active():
                a.use()

    def reload(self, hero: Hero = None):
        hero = hero if hero is not None else GAME.get_castle().get_current_hero()
        self._abilities = hero.get_abilities()

        for b in self._buttons:
            b.destroy()

        self._buttons = []

        if ((isinstance(hero.get_tile().get_placeable(),ChestClosed) and hero.has_item(Key)) or (isinstance(hero.get_tile().get_placeable(),Item) and not isinstance(hero.get_tile().get_placeable(),Key)) or (isinstance(hero.get_tile().get_placeable(),Key) and not hero.has_item(Key)) ) and GAME.get_castle().get_stage() in (STAGE_TURNBEGIN,STAGE_EXPLORING):
            self._pick_item_button.set_visible(True)
        else:
            self._pick_item_button.set_visible(False)
        
        i: int = 0
        for a in reversed(self._abilities):
            if a.is_usable() and not a.is_passive():
                b = AbilityButton(a)
                b.register_mouse_event(MouseEvent.LEFTCLICK,a.use)
                b.set_active(True)
                b.set_visible(self._visible)
                self._buttons.append(b)
                if i == 0:
                    if GAME.get_castle().get_stage() in (STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH,STAGE_REWARD_GATHER):
                        b.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM,0,-b.get_h()*1.5)
                    else:
                        if self._pick_item_button.is_visible():
                            b.set_point(FRAMEPOINT.TOP,FRAMEPOINT.TOP,0,GAME.get_screen().get_h()*0.01,self._pick_item_button)
                        else:
                            b.set_point(FRAMEPOINT.TOP,FRAMEPOINT.TOP,0,GAME.get_screen().get_h()*0.02)
                else:
                    if GAME.get_castle().get_stage() in (STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH,STAGE_REWARD_GATHER):
                        b.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,-b.get_h()*0.1,self._buttons[i-1])
                    else:
                        b.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,b.get_h()*0.1,self._buttons[i-1])
                i += 1
            

    def set_visible(self, visible: bool):
        self._visible = visible
        for b in self._buttons:
            b.set_visible(self._visible)