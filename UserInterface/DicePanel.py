from GraphicComponents.DiceGraphics import DiceGraphics,Frame,FRAMEPOINT,DiceScreen
from GameEngine.DiceManager import DiceManager,Dice
from GraphicsEngine.Constants import MouseEvent

from Game import GAME

class DicePanel():
    main: DiceScreen
    cached_dices: list[Dice]
    g_dices: list[DiceGraphics]

    def __init__(self, screen: Frame) -> None:
        self.main = DiceScreen(screen.get_w(), screen.get_h() * 0.25, screen)
        self.main.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.cached_dices = []
        self.g_dices = []

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()
    
    def update(self):
        dice_manager: DiceManager = GAME.get_dice_manager()
        if dice_manager is not None:
            if not self.is_visible():
                self.show()

            if self.cached_dices != dice_manager.get_dices():
                self.clear()
                self.cached_dices = dice_manager.get_dices()
            
                for i,d in enumerate(self.cached_dices):
                    g_dice = DiceGraphics(self.main.get_h()*0.5,self.main.get_h()*0.5,self.main)
                    if i == 0:
                        g_dice.set_point(att_point=FRAMEPOINT.CENTER,att_point_parent=FRAMEPOINT.CENTER,x_offset= - (g_dice.get_h()/2 + g_dice.get_h()*0.075) * (len(self.cached_dices) - 1))
                    else:
                        g_dice.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,g_dice.get_h()*0.075,0,self.g_dices[i-1])
                    self.g_dices.append(g_dice)
                    g_dice.register_mouse_event(MouseEvent.LEFTCLICK,self.reroll_dice,g_dice)
                    g_dice.set_active(False)
                
            for i,d in enumerate(self.cached_dices):
                self.g_dices[i].set_value(d.get_value())
        else:
            if self.is_visible():
                self.clear()
                self.hide()

    def clear(self):
        for d in reversed(self.g_dices):
            d.destroy()
            self.g_dices.remove(d)

        self.cached_dices = []

    def reroll_dice(self, g_dice: DiceGraphics):
        for i,d in enumerate(self.g_dices):
            if d == g_dice:
                self.cached_dices[i].roll()
            d.set_active(False)

    def activate_dices(self):
        for d in self.g_dices:
            d.set_active(True)

    def reroll(self):
        for d in self.cached_dices:
            d.roll()