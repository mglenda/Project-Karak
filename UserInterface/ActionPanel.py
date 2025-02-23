from GraphicComponents.ActionScreen import ActionScreen,Frame,FRAMEPOINT,ActionButton
from GraphicsEngine.Constants import MouseEvent
from GameEngine.Action import Action

from Game import GAME

class ActionPanel():
    main: ActionScreen
    loaded_actions: list[Action]

    def __init__(self,screen: Frame) -> None:
        self.main = ActionScreen(screen.get_w()*0.4, screen.get_h()*0.125,screen)
        self.main.set_point(att_point=FRAMEPOINT.BOTTOM,att_point_parent=FRAMEPOINT.BOTTOM,x_offset=0,y_offset=-self.main.get_h()*0.1)
        self.loaded_actions = []

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def update(self):
        if self.main.is_visible():
            actions: list[Action] = GAME.get_current_hero_active().get_available_actions()
            if self.loaded_actions != actions:
                self.loaded_actions = actions
                self.main.destroy_children()
                
                a_button: ActionButton = None
                i:int = 0
                for a in actions:
                    if not a.is_passive():
                        if i == 0: 
                            a_button = ActionButton(w=self.main.get_h(),h=self.main.get_h(),parent=self.main,focused_path=a.path_focused,normal_path=a.path)
                            a_button.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
                        else:
                            previous = a_button
                            a_button = ActionButton(w=self.main.get_h()*0.6,h=self.main.get_h()*0.6,parent=self.main,focused_path=a.path_focused,normal_path=a.path)
                            a_button.set_point(FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,a_button.get_w()*0.15,0,previous)
                        a_button.register_mouse_event(MouseEvent.LEFTCLICK,a.run)
                        i += 1

                GAME.force_mouse_motion()
                    