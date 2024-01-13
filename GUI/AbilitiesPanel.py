from GUI.Frame import Frame
from Game import GAME
from GameLogic.Hero import Hero
from GameLogic.Ability import Ability,STAGE_FIGHT,STAGE_EXPLORING,STAGE_ALWAYS,STAGE_FIGHT_AFTERMATH,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_TURNBEGIN
from GUI.GraphicComponents import Rect,Image,TextField,FRAMEPOINT
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
    def __init__(self) -> None:
        self._buttons = []

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

        i: int = 0
        for a in reversed(self._abilities):
            if a.is_usable() and not a.is_passive():
                b = AbilityButton(a)
                b.register_mouse_event(MouseEvent.LEFTCLICK,a.use)
                b.set_active(True)
                self._buttons.append(b)
                if i == 0:
                    if GAME.get_castle().get_stage() in (STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH):
                        b.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM,0,-b.get_h()*1.5)
                    else:
                        b.set_point(FRAMEPOINT.TOP,FRAMEPOINT.TOP)
                else:
                    if GAME.get_castle().get_stage() in (STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH):
                        b.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,0,-b.get_h()*0.1,self._buttons[i-1])
                    else:
                        b.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,b.get_h()*0.1,self._buttons[i-1])
                i += 1