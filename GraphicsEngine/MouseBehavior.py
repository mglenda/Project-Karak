from GraphicsEngine.Constants import MouseEvent
from GraphicsEngine.KeyboardBehavior import FOCUSED
from core.Function import Function

class MouseBehavior():
    def __init__(self) -> None:
        self.mouse_events: list[Function] = [None,None,None,None,None,None,None,None,None,None,None]
        self.active = False

    def is_active(self) -> bool:
        return self.active
    
    def set_active(self, active: bool):
        self.active = active

    def on_mouse_enter(self):
        self.mouse_event_execute(MouseEvent.ENTER)

    def on_mouse_leave(self):
        self.mouse_event_execute(MouseEvent.LEAVE)

    def on_mouse_right_click(self,x,y):
        self.mouse_event_execute(MouseEvent.RIGHTCLICK)

    def on_mouse_left_click(self,x,y):
        self.mouse_event_execute(MouseEvent.LEFTCLICK)

    def on_mouse_wheel_up(self,x,y):
        self.mouse_event_execute(MouseEvent.WHEELUP)

    def on_mouse_wheel_down(self,x,y):
        self.mouse_event_execute(MouseEvent.WHEELDOWN)

    def on_mouse_wheel_click(self,x,y):
        self.mouse_event_execute(MouseEvent.WHEELCLICK)
    
    def on_mouse_left_press(self,x,y):
        FOCUSED.set(self)
        self.mouse_event_execute(MouseEvent.LEFTPRESS)

    def on_mouse_right_press(self,x,y):
        self.mouse_event_execute(MouseEvent.RIGHTPRESS)

    def on_mouse_wheel_press(self,x,y):
        self.mouse_event_execute(MouseEvent.WHEELPRESS)
    
    def on_mouse_motion(self,x,y):
        self.mouse_event_execute(MouseEvent.MOTION)

    def mouse_event_execute(self,evt:int):
        if self.mouse_events[evt] is not None:
            self.mouse_events[evt].execute()

    def register_mouse_event(self,evt: int,func,*args):       
        self.mouse_events[evt] = Function(func,*args)
        
    def clear_mouse_event(self,evt: int):
        self.mouse_events[evt] = None

    def clear_all_events(self):
        self.mouse_events = [None,None,None,None,None,None,None,None,None,None,None]