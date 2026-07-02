from GraphicComponents.DiceGraphics import DiceGraphics,Frame,FRAMEPOINT,DiceScreen
from GameEngine.DiceManager import DiceManager,Dice
from GraphicsEngine.Constants import MouseEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class DicePanel():
    main: DiceScreen
    cached_dices: list[Dice]
    cached_values: list[int]
    cached_roll_ids: list[int]
    g_dices: list[DiceGraphics]

    def __init__(self, screen: Frame, game: "Game") -> None:
        self.dice_service = game.dice_service
        self.main = DiceScreen(screen.get_w(), screen.get_h() * 0.25, screen)
        self.main.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self.cached_dices = []
        self.cached_values = []
        self.cached_roll_ids = []
        self.g_dices = []

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()
    
    def update(self):
        dice_manager: DiceManager = self.dice_service.get_dice_manager()
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
                    self.cached_values.append(d.get_value())
                    self.cached_roll_ids.append(None)
                    g_dice.set_value(d.get_value())
                    g_dice.register_mouse_event(MouseEvent.LEFTCLICK,self.reroll_dice,g_dice)
                    g_dice.set_active(False)

            if dice_manager.is_rolling():
                self.update_rolling_dices(dice_manager)
            else:
                self.update_committed_dices()
        else:
            if self.is_visible():
                self.clear()
                self.hide()

    def update_rolling_dices(self, dice_manager: DiceManager):
        for i,d in enumerate(self.cached_dices):
            self.g_dices[i].update_animation()
            target_value = d.get_pending_value() if d.get_pending_value() is not None else d.get_value()
            if dice_manager.is_dice_rolling(i):
                if self.cached_roll_ids[i] != dice_manager.get_roll_id():
                    self.cached_roll_ids[i] = dice_manager.get_roll_id()
                    self.cached_values[i] = target_value
                    self.g_dices[i].start_animation(target_value, d.definition.values)
            elif self.cached_values[i] != target_value:
                self.cached_values[i] = target_value
                self.g_dices[i].set_value(target_value)

        if not self.has_active_animation(dice_manager):
            self.dice_service.finish_dice_roll()

    def update_committed_dices(self):
        for i,d in enumerate(self.cached_dices):
            current_value = d.get_value()
            if self.cached_values[i] != current_value:
                self.cached_values[i] = current_value
                self.g_dices[i].set_value(current_value)

    def has_active_animation(self, dice_manager: DiceManager) -> bool:
        for i,g_dice in enumerate(self.g_dices):
            if dice_manager.is_dice_rolling(i) and g_dice.is_animating:
                return True
        return False

    def clear(self):
        for d in reversed(self.g_dices):
            d.destroy()
            self.g_dices.remove(d)

        self.cached_dices = []
        self.cached_values = []
        self.cached_roll_ids = []

    def reroll_dice(self, g_dice: DiceGraphics):
        for i,d in enumerate(self.g_dices):
            if d == g_dice:
                self.dice_service.start_dice_reroll(i)
            d.set_active(False)

    def activate_dices(self):
        for d in self.g_dices:
            d.set_active(True)


