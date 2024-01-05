FOCUS_CASTLE_SCREEN = 1
FOCUS_NONE = 0
STATE_DEFAULT = 0
STATE_TILE_SPAWN = 1

class Game():
    def __init__(self):
        self.mouse_motion_lock = False
        self.focused_layer = FOCUS_NONE
        self.state = STATE_DEFAULT

    def lock_mouse_motion(self):
        self.mouse_motion_lock = True
    
    def unlock_mouse_motion(self):
        self.mouse_motion_lock = False

    def is_mouse_motion_locked(self):
        return self.mouse_motion_lock
    
    def set_focused_layer(self,focus_const):
        self.focused_layer = focus_const

    def get_focused_layer(self):
        return self.focused_layer
    
    def set_state(self,state):
        self.state = state

    def get_state(self):
        return self.state