EVENT_MOUSE_ENTER = 0
EVENT_MOUSE_LEAVE = 1
EVENT_MOUSE_RIGHTCLICK = 2
EVENT_MOUSE_LEFTCLICK = 3
EVENT_MOUSE_WHEELUP = 4
EVENT_MOUSE_WHEELDOWN = 5
EVENT_MOUSE_WHEELCLICK = 6

class MouseBehavior():
    def _on_mouse_enter(self):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_ENTER] is not None:
            func = self.mouse_events[EVENT_MOUSE_ENTER]['func']
            args = self.mouse_events[EVENT_MOUSE_ENTER]['args']
            func(args)

    def _on_mouse_leave(self):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_LEAVE] is not None:
            func = self.mouse_events[EVENT_MOUSE_LEAVE]['func']
            args = self.mouse_events[EVENT_MOUSE_LEAVE]['args']
            func(args)

    def _on_mouse_right_click(self,x,y):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_RIGHTCLICK] is not None:
            func = self.mouse_events[EVENT_MOUSE_RIGHTCLICK]['func']
            args = self.mouse_events[EVENT_MOUSE_RIGHTCLICK]['args']
            func(args)

    def _on_mouse_left_click(self,x,y):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_LEFTCLICK] is not None:
            func = self.mouse_events[EVENT_MOUSE_LEFTCLICK]['func']
            args = self.mouse_events[EVENT_MOUSE_LEFTCLICK]['args']
            func(args)

    def _on_mouse_wheel_up(self,x,y):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_WHEELUP] is not None:
            func = self.mouse_events[EVENT_MOUSE_WHEELUP]['func']
            args = self.mouse_events[EVENT_MOUSE_WHEELUP]['args']
            func(args)

    def _on_mouse_wheel_down(self,x,y):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_WHEELDOWN] is not None:
            func = self.mouse_events[EVENT_MOUSE_WHEELDOWN]['func']
            args = self.mouse_events[EVENT_MOUSE_WHEELDOWN]['args']
            func(args)

    def _on_mouse_wheel_click(self,x,y):
        if hasattr(self,'mouse_events') and self.mouse_events[EVENT_MOUSE_WHEELCLICK] is not None:
            func = self.mouse_events[EVENT_MOUSE_WHEELCLICK]['func']
            args = self.mouse_events[EVENT_MOUSE_WHEELCLICK]['args']
            func(args)

    def _on_mouse_motion(self,x,y):
        pass

    def _on_mouse_exit(self):
        self._on_mouse_leave()

    def register_mouse_event(self,evt: int,func,*args: list):
        if not hasattr(self,'mouse_events'):
            self.mouse_events = [None,None,None,None,None,None,None]
        self.mouse_events[evt] = {"func": func
                                    ,'args': args}
        
    def clear_mouse_event(self,evt: int):
        if hasattr(self,'mouse_events'):
            self.mouse_events[evt] = None