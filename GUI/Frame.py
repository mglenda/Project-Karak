from GUI.Element import Element
import GUI._const_framepoints as FRAMEPOINT
from Game import GAME

class FrameInterface(Element):
    _parent: Element
    _components: list
    _attached_elements: list
    _attached_parent: Element
    _attached_point: int
    _attachet_point_parent: int
    def __init__(self) -> None:
        super().__init__()

    def set_point(self,att_point: int,parent: Element,att_point_parent: int,x_offset: int, y_offset: int):
        pass

    def set_abs_point(self,x: int,y :int):
        pass

    def move(self,x_offset: int, y_offset: int):
        pass

    def resize(self,w: int, h:int):
        pass

    def remove(self,component: Element):
        pass

    def add(self,component: Element):
        pass

    def attach(self,component: Element):
        pass

    def deattach(self,component: Element):
        pass

    def _deattach(self):
        pass

    def _attach(self, parent: Element,att_point: int,att_point_parent: int):
        pass

    def _move(self,x_offset: int, y_offset: int):
        pass

    def _resize(self,w: int, h:int):
        pass
    
    def is_visible(self) -> bool:
        return self._parent is not None and super().is_visible() and self._parent.is_visible()
    
    def is_active(self) -> bool:
        return self._parent is not None and super().is_active() and self._parent.is_active()
    
    def destroy(self):
        pass

    def _destroy(self):
        pass

    def set_parent(self,p: Element):
        self._parent = p

    def get_children(self) -> list:
        pass


class Frame(FrameInterface):
    _parent: FrameInterface
    _attached_parent: FrameInterface
    def __init__(self,parent: FrameInterface) -> None:
        super().__init__()
        self._components = []
        self._attached_elements = []
        self._attached_parent = None
        self._attached_point = None
        self._attachet_point_parent = None
        if parent is not None:
            parent.add(self)

    def set_point(self,att_point: int,att_point_parent: int,x_offset: int = 0, y_offset: int = 0,parent: FrameInterface = None):
        self._deattach()
        self.set_x_offset(x_offset)
        self.set_y_offset(y_offset)
        if parent is None:
            parent = self._parent
        parent.attach(self)
        self._attached_parent = parent
        self._attached_point = att_point
        self._attachet_point_parent = att_point_parent
        self._attach()
        self.set_visible(True)
        self.draw()

    def destroy(self):
        if self._destroy():
            GAME.get_screen().draw()

    def get_children(self) -> list:
        children = []
        e:FrameInterface
        for e in self._components:
            children.append(e)
            children.extend(e.get_children())
        return children
    
    def _destroy(self) -> bool:
        self._deattach()
        e:FrameInterface
        for e in reversed(self._attached_elements):
            e._deattach()

        for e in reversed(self._components):
            e._destroy()
        
        was_visible:bool = self.is_visible()
        if self._parent is not None:
            self._parent.remove(self)

        return was_visible

    def remove(self,component: FrameInterface):
        if component in self._components:
            self._components.remove(component)
            component.set_parent(None)

    def add(self,component: FrameInterface):
        if component not in self._components:
            self._components.append(component)
            component.set_parent(self)
        if self != GAME.get_screen():
            GAME.get_screen().draw()

    def attach(self,component: FrameInterface):
        if component not in self._attached_elements:
            self._attached_elements.append(component)

    def deattach(self,component: FrameInterface):
        self._attached_elements.remove(component)

    def draw(self):
        if self in GAME.get_screen()._components:
            GAME.get_screen().draw()

    def _attach(self):
        x: int = self._attached_parent.get_x()
        y: int = self._attached_parent.get_y()
        if x is not None and y is not None:
            w: int = self._attached_parent.get_w()
            h: int = self._attached_parent.get_h()
            point: int = self._attachet_point_parent
            if point == FRAMEPOINT.CENTER:
                x += w / 2
                y += h / 2
            if point == FRAMEPOINT.TOP:
                x += w / 2
            if point == FRAMEPOINT.TOPRIGHT:
                x += w
            if point == FRAMEPOINT.BOTTOM:
                x += w / 2
                y += h
            if point == FRAMEPOINT.BOTTOMLEFT:
                y += h
            if point == FRAMEPOINT.BOTTOMRIGHT:
                x += w
                y += h
            if point == FRAMEPOINT.LEFT:
                y += h / 2
            if point == FRAMEPOINT.RIGHT:
                x += w
                y += h / 2
            
            w = self.get_w()
            h = self.get_h()
            point: int = self._attached_point

            if point == FRAMEPOINT.CENTER:
                x -= w / 2
                y -= h / 2
            if point == FRAMEPOINT.TOP:
                x -= w / 2
            if point == FRAMEPOINT.TOPRIGHT:
                x -= w
            if point == FRAMEPOINT.BOTTOM:
                x -= w / 2
                y -= h
            if point == FRAMEPOINT.BOTTOMLEFT:
                y -= h
            if point == FRAMEPOINT.BOTTOMRIGHT:
                x -= w
                y -= h
            if point == FRAMEPOINT.LEFT:
                y -= h / 2
            if point == FRAMEPOINT.RIGHT:
                x -= w
                y -= h / 2

        if x != self.get_x() or y != self.get_y():
            self.set_x(x)
            self.set_y(y)

            c:FrameInterface
            for c in self._attached_elements:
                c._attach()

    def _deattach(self):
        if self._attached_parent is not None:
            self._attached_parent.deattach(self)
        self._attached_parent = None
        self._attached_point = None
        self._attached_parent = None

    def set_abs_point(self,x: int,y :int):
        self._deattach()
        self.set_x(x)
        self.set_y(y)
        self.set_visible(True)
        self.draw()

    def move(self, x_offset: int, y_offset: int):
        self._move(x_offset,y_offset)
        self.draw()
    
    def resize(self, w: int, h: int):
        self._resize(w,h)
        self.draw()

    def _move(self,x_offset: int, y_offset: int):
        self._x_offset += x_offset
        self._y_offset += y_offset

        e:FrameInterface
        for e in self._attached_elements:
            e._move(x_offset,y_offset)

    def _resize(self,w: int, h:int):
        if w != self.get_w() or h != self.get_h():
            w_ratio = w / self.get_w()
            h_ratio = h / self.get_h()
            self.set_w(w)
            self.set_h(h)
            self._attach() 
            
            e:FrameInterface
            for e in self._attached_elements:
                e._attach()

            for e in self._components:
                e.resize(e.get_w() * w_ratio,e.get_h() * h_ratio)