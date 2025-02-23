from GraphicsEngine.Element import Element
import pygame

class FrameInterface(Element):
    def __init__(self):
        super().__init__()

    def get_surface(self) -> pygame.Surface:
        pass

    def remove(self, child: Element):
        pass

    def add(self, child: Element):
        pass

    def destroy_children(self):
        pass

    def destroy(self):
        pass

    def get_parent(self):
        pass

    def get_children(self):
        pass

    def get_blits_children(self) -> list[Element]:
        pass

    def get_abs_children(self):
        pass

    def set_abs_point(self,x: int,y: int):
        pass

    def set_point(self,att_point: int,att_point_parent: int,x_offset: int, y_offset: int,parent: Element):
        pass

    def attach_child(self, child: Element):
        pass

    def deattach_child(self, child: Element):
        pass

    def deattach(self):
        pass

    def attach(self):
        pass

    def get_abs_att_children(self) -> list[Element]:
        pass

    def move(self,x_offset: int, y_offset: int):
        pass

    def get_abs_x(self) -> int:
        pass

    def get_abs_y(self) -> int:
        pass

    def collide(self,x: int,y: int) -> bool:
        pass

    def collides_with(self, other: Element) -> bool:
        pass

    def resize(self,factor: float):
        pass

    def set_size(self,w: int, h: int):
        pass

    def set_alpha(self, alpha: int):
        pass