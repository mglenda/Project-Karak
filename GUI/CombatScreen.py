from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Rect,Image,TextField
from GUI._const_combat_modifiers import MODIFIER_ABILITY,MODIFIER_BASE,MODIFIER_DICE,MODIFIER_SCROLL
from GameLogic.Hero import Warrior,Hero
from GameLogic.Minion import SkeletonMage,Minion
from GameLogic.Combatiant import Combatiant
from GameLogic.Ability import STAGE_FIGHT,STAGE_FIGHT_END,STAGE_FIGHT_START,STAGE_FIGHT_AFTERMATH
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
        self._power += power
        self._text.set_text(str(self._power))

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

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        self._alpha = 230
        super().__init__(w, h, (0,0,0), parent)

        self._combat_icon = Image(self.get_h()*0.10,self.get_h()*0.10,PATH + 'CombatIcon.png',self)
        self._combat_icon.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,0,-self.get_h()*0.3)

        self._combatant1_icon = Image(self.get_h()*0.15,self.get_h()*0.15,Warrior._icon,self)
        self._combatant1_icon.set_point(FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,-self.get_h()*0.05,0,self._combat_icon)

        self._combatant2_icon = Image(self.get_h()*0.15,self.get_h()*0.15,SkeletonMage._background,self)
        self._combatant2_icon.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,self.get_h()*0.05,0,self._combat_icon)

        self._combatant_1_power_text = TextField(parent=self,font_size=70,text='10')
        self._combatant_1_power_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.get_h()*0.025,self._combatant1_icon)

        self._combatant_2_power_text = TextField(parent=self,font_size=70,text='10')
        self._combatant_2_power_text.set_point(FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,0,self.get_h()*0.025,self._combatant2_icon)

        self._modifiers_1 = []
        self._modifiers_2 = []

        self._active_combatant = None

    def _recalculate(self):
        p = 0 
        for m in self._modifiers_1:
            p += m._power

        self._combatant_1_power_text.set_text(str(p))
        
        p = 0
        for m in self._modifiers_2:
            p += m._power

        self._combatant_2_power_text.set_text(str(p)) 

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

        GAME.get_castle().set_stage(STAGE_FIGHT_START)
        GAME.get_abilities_panel().use_passives()


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

    def set_modifier(self,power: int, type: dict, combatiant: Combatiant):
        if combatiant == self._combatiant_1:
            self._modifiers_1[type].set_power(power)
        else:
            self._modifiers_2[type].set_power(power)
        self._recalculate()