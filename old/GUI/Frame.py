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

    def get_attached_parent(self) -> Element:
        pass

    def get_attached_point(self) -> int:
        pass

    def get_attached_point_parent(self) -> int:
        pass

    def set_point(self,att_point: int,parent: Element,att_point_parent: int,x_offset: int, y_offset: int):
        pass

    def set_abs_point(self,x: int,y :int):
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

    def move(self,x_offset: int, y_offset: int):
        pass

    def resize(self,w: int, h:int, refresh: bool = True):
        pass

    def set_alpha(self,alpha: int, refresh: bool = True):
        pass

    def destroy(self):
        pass

    def set_parent(self,p: Element):
        self._parent = p

    def get_parent(self) -> Element:
        return self._parent

    def get_children(self) -> list:
        pass

    def get_blits_children(self) -> list:
        pass

    def refresh(self):
        pass

class Frame(FrameInterface):
    _components: list[FrameInterface]
    _attached_elements: list[FrameInterface]
    _attached_point: int
    _attachet_point_parent: int
    _parent: FrameInterface
    _attached_parent: FrameInterface
    _alpha: int = 255
    def __init__(self,parent: FrameInterface) -> None:
        super().__init__()
        self._components = []
        self._attached_elements = []
        self._attached_parent = None
        self._attached_point = None
        self._attachet_point_parent = None
        if parent is not None:
            parent.add(self)
        else:
            self._parent = None

    def get_attached_parent(self) -> Element:
        return self._attached_parent

    def get_attached_point(self) -> int:
        return self._attached_point

    def get_attached_point_parent(self) -> int:
        return self._attachet_point_parent

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

    def set_abs_point(self,x: int,y :int):
        self._deattach()
        self.set_x(x)
        self.set_y(y)
        for c in self._attached_elements:
            c._attach()
        self.set_visible(True)

    def get_blits_children(self) -> list:
        children = []
        for e in self._components:
            if e.is_visible() and e.get_x() is not None and e.get_y() is not None:
                children.append((e.get_surface(),(e.get_x(),e.get_y())))
                children.extend(e.get_blits_children())
        return children

    def get_children(self) -> list:
        children = []
        for e in self._components:
            if e.is_visible() and e.get_x() is not None and e.get_y() is not None:
                children.append(e)
                children.extend(e.get_children())
        return children
    
    def destroy(self) -> bool:
        self._deattach()
        e:FrameInterface
        for e in reversed(self._attached_elements):
            e._deattach()

        for e in reversed(self._components):
            e.destroy()
        
        was_visible:bool = self.is_visible()
        if self._parent is not None:
            self._parent.remove(self)

        if self == GAME.screen._focused:
            GAME.screen._focused = None
            
        if self == GAME.screen._entered:
            GAME.screen._entered = None

        return was_visible

    def remove(self,component: FrameInterface):
        if component in self._components:
            self._components.remove(component)
            component.set_parent(None)

    def add(self,component: FrameInterface):
        if component not in self._components:
            self._components.append(component)
            component.set_parent(self)

    def attach(self,component: FrameInterface):
        if component not in self._attached_elements:
            self._attached_elements.append(component)

    def deattach(self,component: FrameInterface):
        self._attached_elements.remove(component)

    def get_point(self,att_point):
        x: int = self.get_x()
        y: int = self.get_y()
        if x is not None and y is not None:
            w: int = self.get_w()
            h: int = self.get_h()
            
            if att_point == FRAMEPOINT.CENTER:
                x += w / 2
                y += h / 2
            elif att_point == FRAMEPOINT.TOP:
                x += w / 2
            elif att_point == FRAMEPOINT.TOPRIGHT:
                x += w
            elif att_point == FRAMEPOINT.BOTTOM:
                x += w / 2
                y += h
            elif att_point == FRAMEPOINT.BOTTOMLEFT:
                y += h
            elif att_point == FRAMEPOINT.BOTTOMRIGHT:
                x += w
                y += h
            elif att_point == FRAMEPOINT.LEFT:
                y += h / 2
            elif att_point == FRAMEPOINT.RIGHT:
                x += w
                y += h / 2

        return x,y

    def _attach(self):
        if self._attached_parent is not None:
            x: int = self._attached_parent.get_x()
            y: int = self._attached_parent.get_y()
            if x is not None and y is not None:
                w: int = self._attached_parent.get_w()
                h: int = self._attached_parent.get_h()
                
                if self._attachet_point_parent == FRAMEPOINT.CENTER:
                    x += w / 2
                    y += h / 2
                elif self._attachet_point_parent == FRAMEPOINT.TOP:
                    x += w / 2
                elif self._attachet_point_parent == FRAMEPOINT.TOPRIGHT:
                    x += w
                elif self._attachet_point_parent == FRAMEPOINT.BOTTOM:
                    x += w / 2
                    y += h
                elif self._attachet_point_parent == FRAMEPOINT.BOTTOMLEFT:
                    y += h
                elif self._attachet_point_parent == FRAMEPOINT.BOTTOMRIGHT:
                    x += w
                    y += h
                elif self._attachet_point_parent == FRAMEPOINT.LEFT:
                    y += h / 2
                elif self._attachet_point_parent == FRAMEPOINT.RIGHT:
                    x += w
                    y += h / 2
                
                w = self.get_w()
                h = self.get_h()

                if self._attached_point == FRAMEPOINT.CENTER:
                    x -= w / 2
                    y -= h / 2
                elif self._attached_point == FRAMEPOINT.TOP:
                    x -= w / 2
                elif self._attached_point == FRAMEPOINT.TOPRIGHT:
                    x -= w
                elif self._attached_point == FRAMEPOINT.BOTTOM:
                    x -= w / 2
                    y -= h
                elif self._attached_point == FRAMEPOINT.BOTTOMLEFT:
                    y -= h
                elif self._attached_point == FRAMEPOINT.BOTTOMRIGHT:
                    x -= w
                    y -= h
                elif self._attached_point == FRAMEPOINT.LEFT:
                    y -= h / 2
                elif self._attached_point == FRAMEPOINT.RIGHT:
                    x -= w
                    y -= h / 2

            if x != self.get_x() or y != self.get_y():
                self.set_x(x)
                self.set_y(y)

                for c in self._attached_elements:
                    c._attach()

    def _deattach(self):
        if self._attached_parent is not None:
            self._attached_parent.deattach(self)
        self._attached_parent = None
        self._attached_point = None
        self._attached_parent = None

    def move(self,x_offset: int, y_offset: int):
        self._x_offset += x_offset
        self._y_offset += y_offset

        e:FrameInterface
        for e in self._attached_elements:
            e._attach()

    def resize(self,w: int, h:int, refresh: bool = True):
        if w != self.get_w() or h != self.get_h():
            w_ratio = w / self.get_w()
            h_ratio = h / self.get_h()
            self.set_w(w)
            self.set_h(h)
            self._attach()
            self._x_offset *= w_ratio
            self._y_offset *= h_ratio

            for e in self._components:
                e.resize(e.get_w() * w_ratio,e.get_h() * h_ratio)

            if refresh:
                self.refresh()

    def set_alpha(self, alpha: int, refresh:bool = True):
        if alpha != self._alpha:
            self._alpha = alpha
            for e in self._components:
                e.set_alpha(alpha)
            
            if refresh:
                self.refresh()