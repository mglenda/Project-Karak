from GraphicsEngine.Screen import Screen,Frame

class MouseController():
    screen: Screen
    entered: Frame
    def __init__(self, screen: Screen) -> None:
        self.screen = screen
        self.entered = None

    def on_mouse_motion(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                if self.entered != e:
                    if self.entered is not None and self.entered.is_active():
                        self.entered.on_mouse_leave()
                    self.entered = e
                    e.on_mouse_enter()
                e.on_mouse_motion(x,y)
                return
        if self.entered is not None and not self.entered.collide(x,y) and self.entered.is_active():
            self.entered.on_mouse_leave()
            self.entered = None
        self.screen.on_mouse_motion(x,y)
    
    def on_mouse_left_click(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_left_click(x,y)
                return
        self.screen.on_mouse_left_click(x, y)

    def on_mouse_left_press(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_left_press(x,y)
                return
        self.screen.on_mouse_left_press(x, y)
    
    def on_mouse_right_click(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_right_click(x,y)
                return
        self.screen.on_mouse_right_click(x, y)
    
    def on_mouse_right_press(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_right_press(x,y)
                return
        self.screen.on_mouse_right_press(x, y)
    
    def on_mouse_wheel_click(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_wheel_click(x,y)
                return
        self.screen.on_mouse_wheel_click(x, y)
    
    def on_mouse_wheel_press(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_wheel_press(x,y)
                return
        self.screen.on_mouse_wheel_press(x, y)
    
    def on_mouse_wheel_down(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_wheel_down(x,y)
                return
        self.screen.on_mouse_wheel_down(x, y)
    
    def on_mouse_wheel_up(self, x, y):
        for e in reversed(self.screen.get_abs_children()):
            if e.is_active() and e.collide(x,y):
                e.on_mouse_wheel_up(x,y)
                return
        self.screen.on_mouse_wheel_up(x, y)