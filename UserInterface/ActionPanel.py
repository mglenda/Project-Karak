from GraphicComponents.ActionScreen import ActionScreen,Frame,FRAMEPOINT,ActionButton
from GraphicsEngine.Constants import MouseEvent
from GameEngine.Action import Action
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class ActionPanel():
    main: ActionScreen
    loaded_actions: list[Action]
    hidden_by_roll: bool

    def __init__(self,screen: Frame, game: "Game") -> None:
        self.game = game
        self.context = game.context
        self.dice_service = game.dice_service
        self.main = ActionScreen(screen.get_w()*0.4, screen.get_h()*0.125,screen)
        self.main.set_point(att_point=FRAMEPOINT.BOTTOM,att_point_parent=FRAMEPOINT.BOTTOM,x_offset=0,y_offset=-self.main.get_h()*0.1)
        self.loaded_actions = []
        self.hidden_by_roll = False

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def clear_actions(self):
        self.main.destroy_children()
        self.loaded_actions = []

    def update(self):
        if self.dice_service.is_dice_rolling():
            if self.main.is_visible():
                self.hidden_by_roll = True
                self.hide()
            self.clear_actions()
            return
        elif self.hidden_by_roll:
            self.hidden_by_roll = False
            self.show()

        if self.main.is_visible():
            actions: list[Action] = self.context.get_current_hero_active().get_available_actions()
            if self.loaded_actions != actions:
                self.loaded_actions = actions
                self.main.destroy_children()
                
                a_button: ActionButton = None
                first_button: ActionButton = None
                i:int = 0
                for a in actions:
                    if not a.is_passive():
                        if i == 0:
                            x: int = self.main.get_h()*0.95
                            a_button = ActionButton(w=x,h=x,parent=self.main,focused_path=a.path_focused,normal_path=a.path)
                            a_button.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
                            first_button = a_button
                        else:
                            previous = a_button
                            a_button = ActionButton(w=self.main.get_h()*0.95,h=self.main.get_h()*0.95,parent=self.main,focused_path=a.path_focused,normal_path=a.path)
                            a_button.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,a_button.get_w()*0.15,0,previous)
                        a_button.register_mouse_event(MouseEvent.LEFTCLICK,a.run)
                        i += 1
                if i > 1:
                    offset_x: int = ((first_button.get_w() + first_button.get_w()*0.15) / 2) * (i-1)
                    first_button.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,-offset_x)

                self.game.force_mouse_motion()
