from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Rect,Image,TextField
from GUI.Button import Button,BUTTON_CLASSIC_YELLOW
from GUI._const_mouseevents import LEFTCLICK
from GUI._const_combat_modifiers import MODIFIER_ABILITY,MODIFIER_BASE,MODIFIER_DICE,MODIFIER_SCROLL
from GameLogic.Hero import Hero
from GameLogic.Minion import Minion
from GameLogic.Combatiant import Combatiant
from GameLogic.Ability import STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH,STAGE_FLEEING
from GameLogic.DiceRoller import DiceRoller,DICE_NORMAL,DICE_WARLOCK
from Game import GAME

PATH = '_Textures\\CombatScreen\\'

MODIFIERS = [
    {
    "icon": PATH + 'Modifier_Base.png'
    ,'color': (255,255,255)
    }
    ,{
        "icon": PATH + 'Modifier_Dice.png'
        ,'color': (255,215,0)
    }
    ,{
        "icon": PATH + 'Modifier_Scroll.png'
        ,'color': (186,187,218)
    }
    ,{
        "icon": PATH + 'Modifier_Ability.png'
        ,'color': (248,183,127)
    }
]

class CombatModifier(Rect):
    _icon: Image
    _text: TextField
    _power: int
    _type: int

    def __init__(self, w: int, power: int, type: int, parent: Frame) -> None:
        self._alpha = 0
        super().__init__(w*1.3, w/2, (0,0,0), parent)
        self._type = type
        self._power = power

        self._icon = Image(self.get_h(),self.get_h(),MODIFIERS[type]['icon'],self)
        self._icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.LEFT)

        self._text = TextField(self,MODIFIERS[type]['color'],24,str(power))
        self._text.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,w*0.3,0,self._icon)

    def set_power(self, power: int):
        self._power = power
        self._text.set_text(str(self._power))

    def get_power(self) -> int:
        return self._power

class CombatScreen(Rect):
    _modifiers_1: list[CombatModifier]
    _modifiers_2: list[CombatModifier]
    _combat_icon: Image
    _combatant1_icon: Image
    _combatant2_icon: Image
    _combatant_1_power_text: TextField
    _combatant_2_power_text: TextField
    _combatiant_1: Combatiant
    _combatiant_2: Combatiant
    _active_combatant: Combatiant
    _end_turn_button: Button

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        self._alpha = 230
        super().__init__(w, h, (0,0,0), parent)

        self._combat_icon = Image(self.get_h()*0.10,self.get_h()*0.10,PATH + 'CombatIcon.png',self)
        self._combat_icon.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,0,-self.get_h()*0.3)

        self._combatant1_icon = Image(self.get_h()*0.15,self.get_h()*0.15,PATH + 'CombatIcon.png',self)
        self._combatant1_icon.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,-self.get_h()*0.05,0,self._combat_icon)

        self._combatant2_icon = Image(self.get_h()*0.15,self.get_h()*0.15,PATH + 'CombatIcon.png',self)
        self._combatant2_icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_h()*0.05,0,self._combat_icon)

        self._combatant_1_power_text = TextField(parent=self,font_size=70,text='10')
        self._combatant_1_power_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.get_h()*0.025,self._combatant1_icon)

        self._combatant_2_power_text = TextField(parent=self,font_size=70,text='10')
        self._combatant_2_power_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.get_h()*0.025,self._combatant2_icon)

        self._end_turn_button = Button(self.get_h()*0.25,self.get_h()*0.12,BUTTON_CLASSIC_YELLOW,self,'End Turn',50)
        self._end_turn_button.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT,-self.get_h()*0.025,-self.get_h()*0.025)
        self._end_turn_button.register_mouse_event(LEFTCLICK,self._end_turn)

        self._modifiers_1 = []
        self._modifiers_2 = []

        self._active_combatant = None

    def _end_turn(self):
        self._dice_roller.destroy()
        if self._active_combatant == self._combatiant_1 and isinstance(self._combatiant_2,Hero):
            self._active_combatant = self._combatiant_2
            GAME.get_castle().set_stage(STAGE_FIGHT_START,self._active_combatant)
            GAME.get_abilities_panel().use_passives()

            self._dice_roller = DiceRoller(DICE_NORMAL,DICE_NORMAL)
        else:
            result = self._recalculate()
            victor = self._combatiant_1
            loser = self._combatiant_2
            if result[0] < result[1]:
                victor = self._combatiant_2
                loser = self._combatiant_1

            draw = result[0] == result[1]

            self._flush()
            self.set_visible(False)

            hero = GAME.get_castle().get_current_hero()
            hero.set_move_points(0)

            if isinstance(victor,Hero) and isinstance(loser,Hero):
                if not draw:
                    loser.hurt()
                    GAME.get_reward_screen().load(victor,loser)
                else:
                    GAME.get_castle().next_action()
            else:
                if isinstance(victor,Minion) or draw:
                    #hero lost the fight
                    if not draw:
                        hero.hurt()
                    if hero.get_previous_tile() is not None:
                        hero.set_tile(hero.get_previous_tile())
                        GAME.get_castle().next_action()
                    else:
                        GAME.get_castle().flee()
                else:
                    #hero won the fight
                    GAME.get_reward_screen().load(victor,loser)

    def _recalculate(self):
        p1 = 0 
        for m in self._modifiers_1:
            p1 += m._power

        self._combatant_1_power_text.set_text(str(p1))
        
        p2 = 0
        for m in self._modifiers_2:
            p2 += m._power

        self._combatant_2_power_text.set_text(str(p2)) 

        return (p1,p2)

    def get_active_combatiant(self) -> Combatiant:
        return self._active_combatant

    def _load(self,combatiant_1: Combatiant, combatiant_2: Combatiant):
        self._combatiant_1 = combatiant_1
        self._combatiant_2 = combatiant_2
        self._active_combatant = combatiant_1

        self._combatant1_icon.set_texture(combatiant_1.get_icon())
        self._combatant2_icon.set_texture(combatiant_2.get_icon())

        self.add_modifier(combatiant_1.get_power(),MODIFIER_BASE,combatiant_1)
        self.add_modifier(0,MODIFIER_DICE,combatiant_1)
        self.add_modifier(0,MODIFIER_SCROLL,combatiant_1)
        self.add_modifier(0,MODIFIER_ABILITY,combatiant_1)

        self.add_modifier(combatiant_2.get_power(),MODIFIER_BASE,combatiant_2)

        if isinstance(combatiant_2,Hero):
            self.add_modifier(0,MODIFIER_DICE,combatiant_2)
            self.add_modifier(0,MODIFIER_SCROLL,combatiant_2)
            self.add_modifier(0,MODIFIER_ABILITY,combatiant_2)

        self._attach_modifiers()
        self._recalculate()

        GAME.get_castle().set_stage(STAGE_FIGHT_START,self._active_combatant)
        GAME.get_abilities_panel().use_passives()

        self._dice_roller = DiceRoller(DICE_NORMAL,DICE_NORMAL)
    
    def dice_roll(self):
        GAME.register_timer(10,[
            (self._dice_roller.roll,())
        ],30,5
        ,[
            (self.roll_end,())
        ])
        self._end_turn_button.set_active(False)

    def roll_end(self):
        power = self._dice_roller.get_result()
        self.set_modifier(power,MODIFIER_DICE,self._active_combatant)
        GAME.get_castle().set_stage(STAGE_FIGHT_END,self._active_combatant)
        GAME.get_abilities_panel().use_passives()
        self._end_turn_button.set_active(True)

    def _flush(self):
        for m in self._modifiers_1:
            m.destroy()

        for m in self._modifiers_2:
            m.destroy()

        self._modifiers_1: list[CombatModifier] = []
        self._modifiers_2: list[CombatModifier] = []

    def _attach_modifiers(self):
        for i,m in enumerate(self._modifiers_1):
            y_offset: int = self.get_h()*0.02
            if i == 0:
                m.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,y_offset,self._combatant_1_power_text)
            else:
                m.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,y_offset,self._modifiers_1[i-1])

        for i,m in enumerate(self._modifiers_2):
            y_offset: int = self.get_h()*0.02
            if i == 0:
                m.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,y_offset,self._combatant_2_power_text)
            else:
                m.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,y_offset,self._modifiers_2[i-1])

    def add_modifier(self,power: int, type: dict, combatiant: Combatiant):
        mod = CombatModifier(self._combat_icon.get_w()*0.4,power,type,self)
        if combatiant == self._combatiant_1:
            self._modifiers_1.append(mod)
        else:
            self._modifiers_2.append(mod)

    def set_modifier(self,power: int, type: int, combatiant: Combatiant):
        if combatiant == self._combatiant_1:
            self._modifiers_1[type].set_power(power)
        else:
            self._modifiers_2[type].set_power(power)
        self._recalculate()

    def inc_modifier(self, power: int, type: int, combatiant: Combatiant):
        if combatiant == self._combatiant_1:
            self._modifiers_1[type].set_power(self._modifiers_1[type].get_power() + power)
        else:
            self._modifiers_2[type].set_power(self._modifiers_2[type].get_power() + power)
        self._recalculate()
        