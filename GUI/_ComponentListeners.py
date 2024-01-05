import GUI._const_mouseevents as MouseEvent

class MouseListener():
    def _on_mouse_enter(self):
        self._execute(MouseEvent.ENTER)
        print('enter' + str(self))

    def _on_mouse_leave(self):
        self._execute(MouseEvent.LEAVE)
        print('leave' + str(self))

    def _on_mouse_right_click(self,x,y):
        self._execute(MouseEvent.RIGHTCLICK)

    def _on_mouse_left_click(self,x,y):
        self._execute(MouseEvent.LEFTCLICK)

    def _on_mouse_wheel_up(self,x,y):
        self._execute(MouseEvent.WHEELUP)

    def _on_mouse_wheel_down(self,x,y):
        self._execute(MouseEvent.WHEELDOWN)

    def _on_mouse_wheel_click(self,x,y):
        self._execute(MouseEvent.WHEELCLICK)
    
    def _on_mouse_left_press(self,x,y):
        self._execute(MouseEvent.LEFTPRESS)

    def _on_mouse_right_press(self,x,y):
        self._execute(MouseEvent.RIGHTPRESS)

    def _on_mouse_wheel_press(self,x,y):
        self._execute(MouseEvent.WHEELPRESS)
    
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

class KeyBoardListener():
    def _on_key_hold(self, key: int):
        pass
    
    def _on_key_pressed(self, key: int):
        pass
   
    def _on_key_released(self, key: int):
        pass