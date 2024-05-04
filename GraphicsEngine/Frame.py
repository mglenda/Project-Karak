from GraphicsEngine.FrameInterface import FrameInterface
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
import pygame

class Frame(FrameInterface):
    parent: FrameInterface
    att_parent: FrameInterface
    att_point: int
    att_point_parent: int
    att_children: list[FrameInterface]
    children: list[FrameInterface]
    surface: pygame.Surface
    factor: float

    def __init__(self,parent: FrameInterface):
        super().__init__()
        self.surface = None
        self.att_parent = None
        self.att_point = None
        self.att_point_parent = None
        self.att_children = []
        self.children = []
        self.factor = 1.0

        self.parent = parent
        if parent is not None:
            parent.add(self)
            self.alpha = parent.alpha

    def get_surface(self) -> pygame.Surface:
        return self.surface

    def remove(self, child: FrameInterface):
        self.children.remove(child)

    def add(self, child: FrameInterface):
        self.children.append(child)

    def destroy(self):
        self.deattach()
        for c in reversed(self.children):
            c.destroy()

        for s in reversed(self.att_children):
            s.deattach()

        self.parent.remove(self)
        del self

    def get_parent(self) -> FrameInterface:
        return self.parent

    def get_children(self) -> list[FrameInterface]:
        return self.children
    
    def get_blits_children(self) -> list[FrameInterface]:
        children = []
        for e in self.children:
            if e.is_visible():
                children.append((e.get_surface(),(e.get_x(),e.get_y())))
                children.extend(e.get_blits_children())
        return children
    
    def get_abs_children(self) -> list[FrameInterface]:
        abs_children = []
        for c in self.children:
            abs_children.append(c)
            abs_children.extend(c.get_abs_children())
        return abs_children

    def set_abs_point(self,x: int,y: int):
        self.set_xy(x,y)
        self.set_visible(True)

    def set_point(self,att_point: int,att_point_parent: int,x_offset: int = 0, y_offset: int = 0,parent: FrameInterface = None):
        #you can attach elements only with siblings or their parents
        if self.att_parent is not None:
            self.deattach()
        self.set_x_offset(x_offset)
        self.set_y_offset(y_offset)
        self.att_parent = parent if parent is not None else self.parent
        self.att_parent.attach_child(self)
        self.att_point = att_point
        self.att_point_parent = att_point_parent
        self.attach()
        self.set_visible(True)

        for c in self.get_abs_att_children():
            c.attach()

    def attach_child(self, child: FrameInterface):
        if child not in self.att_children:
            self.att_children.append(child)

    def deattach_child(self, child: FrameInterface):
        if child in self.att_children:
            self.att_children.remove(child)

    def deattach(self):
        if self.att_parent is not None:
            self.att_parent.deattach_child(self)
        self.att_parent = None
        self.att_point = None
        self.att_point_parent = None

    def attach(self):
        if self.att_parent is not None:
            x: int = self.att_parent.get_x()
            y: int = self.att_parent.get_y()
            w: int = self.att_parent.get_w()
            h: int = self.att_parent.get_h()

            if self.att_point_parent in (FRAMEPOINT.CENTER,FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM):
                x += w / 2
            elif self.att_point_parent in (FRAMEPOINT.TOPRIGHT,FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.RIGHT):
                x += w

            if self.att_point_parent in (FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,FRAMEPOINT.CENTER):
                y += h / 2
            elif self.att_point_parent in (FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT):
                y += h
            
            w = self.get_w()
            h = self.get_h()

            if self.att_point in (FRAMEPOINT.CENTER,FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM):
                x -= w / 2
            elif self.att_point in (FRAMEPOINT.TOPRIGHT,FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.RIGHT):
                x -= w

            if self.att_point in (FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,FRAMEPOINT.CENTER):
                y -= h / 2
            elif self.att_point in (FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOMLEFT,FRAMEPOINT.BOTTOMRIGHT):
                y -= h

            self.set_x(x)
            self.set_y(y)

    def get_abs_att_children(self) -> list[FrameInterface]:
        att_siblings = []
        for c in self.att_children:
            att_siblings.append(c)
            att_siblings.extend(c.get_abs_att_children())
        return att_siblings

    def move(self,x_offset: int, y_offset: int):
        self.x_offset += x_offset
        self.y_offset += y_offset

        for s in self.get_abs_att_children():
            s.attach()

    def collide(self,x: int,y: int) -> bool:
        return x >= self.get_x() and x <= self.get_x() + self.get_w() and y >= self.get_y() and y <= self.get_y() + self.get_h()
    
    def resize(self,factor: float):
        self.set_w((self.w / self.factor) * factor)
        self.set_h((self.h / self.factor) * factor)

        self.factor = factor
        
        self.attach()
        for c in self.children:
            c.resize(factor)
            c.attach()

    def set_size(self,w: int, h: int):
        factor_w = w / self.w
        factor_h = h / self.h

        self.set_w(w)
        self.set_h(h)
        self.factor = 1.0

        self.attach()
        for c in self.children:
            c.set_size(c.get_w()*factor_w,c.get_h()*factor_h)
            c.attach()

    def set_alpha(self, alpha: int):
        if alpha != self.alpha:
            self.alpha = alpha
            self.refresh_surface()
            self.surface.set_alpha(alpha)
            
            for c in self.children:
                c.set_alpha(alpha)

    def refresh_alpha(self):
        if self.alpha < 255:
            self.surface.set_alpha(self.alpha)

    def refresh_surface(self):
        pass

    def rotate(self, angle: int):
        super().rotate(angle)

        for c in self.children:
            c.rotate(angle)