import GUI._const_mouseevents as MouseEvent
import pygame

class MouseListener():
    _mouse_events: bool
    def _on_mouse_enter(self):
        self._execute(MouseEvent.ENTER)

    def _on_mouse_leave(self):
        self._execute(MouseEvent.LEAVE)

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

    def _execute(self,evt:int):
        if hasattr(self,'_mouse_events') and self._mouse_events[evt] is not None:
            func = self._mouse_events[evt]['func']
            args = self._mouse_events[evt]['args']
            if len(args) == 0:
                func()
            else:
                if isinstance(args,str):
                    func(args)
                else:
                    func(*args)

    def register_mouse_event(self,evt: int,func,*args: list):
        if not hasattr(self,'_mouse_events'):
            self._mouse_events = [None,None,None,None,None,None,None,None,None,None]
        self._mouse_events[evt] = {"func": func
                                    ,'args': args}
        
    def clear_mouse_event(self,evt: int):
        if hasattr(self,'_mouse_events'):
            self._mouse_events[evt] = None

class KeyBoardListener():
    _is_focused: bool
    def set_focus(self, focus: bool):
        self._is_focused = focus

    def _on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        pass
    
    def _on_key_pressed(self, key: int, unicode: str):
        pass
   
    def _on_key_released(self, key: int, unicode: str):
        pass