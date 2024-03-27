from GraphicsEngine.MouseBehavior import MouseBehavior

class Element(MouseBehavior):
    x: int
    y: int
    x_offset: int
    y_offset: int
    w: int
    h: int
    angle: int
    visible: bool
    alpha: int

    def __init__(self) -> None:
        super().__init__()
        self.visible = False
        self.active = False
        self.angle = 0
        self.x = 0
        self.y = 0
        self.x_offset = 0
        self.y_offset = 0
        self.w = 0
        self.h = 0
        self.alpha = 255
    
    def set_xy(self,x: int, y: int):
        self.x = x
        self.y = y

    def set_x(self,x: int):
        self.x = x

    def set_x_offset(self,x_offset: int):
        self.x_offset = x_offset
    
    def set_y(self,y: int):
        self.y = y

    def set_y_offset(self,y_offset: int):
        self.y_offset = y_offset

    def set_w(self,w: int):
        self.w = w

    def set_h(self,h: int):
        self.h = h

    def set_visible(self,visible: bool):
        self.visible = visible
    
    def rotate(self,angle: int):
        self.angle = (self.angle + angle) % 360

    def get_angle(self) -> int:
        return self.angle

    def get_x(self) -> int:
        return self.x + self.x_offset
    
    def get_x_offset(self) -> int:
        return self.x_offset
    
    def get_y(self) -> int:
        return self.y + self.y_offset
    
    def get_y_offset(self) -> int:
        return self.y_offset
    
    def get_w(self) -> int:
        return self.w
    
    def get_h(self) -> int:
        return self.h
    
    def get_alpha(self) -> int:
        return self.alpha

    def is_visible(self) -> bool:
        return self.visible