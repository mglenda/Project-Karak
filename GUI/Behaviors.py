EVENT_MOUSE_ENTER = 0
EVENT_MOUSE_LEAVE = 1
EVENT_MOUSE_RIGHTCLICK = 2
EVENT_MOUSE_LEFTCLICK = 3
EVENT_MOUSE_WHEELUP = 4
EVENT_MOUSE_WHEELDOWN = 5
EVENT_MOUSE_WHEELCLICK = 6
EVENT_MOUSE_LEFTPRESS = 7
EVENT_MOUSE_RIGHTPRESS = 8
EVENT_MOUSE_WHEELPRESS = 9

class MouseBehavior():
    def _on_mouse_enter(self):
        self._execute(EVENT_MOUSE_ENTER)

    def _on_mouse_leave(self):
        self._execute(EVENT_MOUSE_LEAVE)

    def _on_mouse_right_click(self,x,y):
        self._execute(EVENT_MOUSE_RIGHTCLICK)

    def _on_mouse_left_click(self,x,y):
        self._execute(EVENT_MOUSE_LEFTCLICK)

    def _on_mouse_wheel_up(self,x,y):
        self._execute(EVENT_MOUSE_WHEELUP)

    def _on_mouse_wheel_down(self,x,y):
        self._execute(EVENT_MOUSE_WHEELDOWN)

    def _on_mouse_wheel_click(self,x,y):
        self._execute(EVENT_MOUSE_WHEELCLICK)
    
    def _on_mouse_left_press(self,x,y):
        self._execute(EVENT_MOUSE_LEFTPRESS)

    def _on_mouse_right_press(self,x,y):
        self._execute(EVENT_MOUSE_RIGHTPRESS)

    def _on_mouse_wheel_press(self,x,y):
        self._execute(EVENT_MOUSE_WHEELPRESS)
    
    def _on_mouse_motion(self,x,y):
        pass

    def _on_mouse_exit(self):
        self._on_mouse_leave()

    def _execute(self,evt:int):
        if hasattr(self,'mouse_events') and self.mouse_events[evt] is not None:
            func = self.mouse_events[evt]['func']
            args = self.mouse_events[evt]['args']
            if len(args) == 0:
                func()
            else:
                func(*args)

    def register_mouse_event(self,evt: int,func,*args: list):
        if not hasattr(self,'mouse_events'):
            self.mouse_events = [None,None,None,None,None,None,None,None,None,None]
        self.mouse_events[evt] = {"func": func
                                    ,'args': args}
        
    def clear_mouse_event(self,evt: int):
        if hasattr(self,'mouse_events'):
            self.mouse_events[evt] = None