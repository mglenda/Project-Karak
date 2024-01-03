import pygame
from GUI.Behaviors import MouseBehavior
import GUI.Behaviors as Behaviors

class Element(MouseBehavior):
    active: bool
    surface: pygame.Surface
    x: int
    y: int
    absx: int
    absy: int

    def draw(self):
        pass

    def coolide(self,x: int,y: int) -> bool:
        return x >= self.absx and x <= self.absx + self.surface.get_width() and y >= self.absy and y <= self.absy + self.surface.get_height()

    def set_active(self,active:bool):
        self.active = active

    def is_active(self) -> bool:
        return self.active
    
    def get_surface(self) -> pygame.Surface:
        return self.surface
    
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_point(self,x: int,y: int):
        self.x = x
        self.y = y
    
    def set_abs_point(self,x: int,y: int):
        self.absx = x
        self.absy = y


class Rect(Element):
    def __init__(self,w=0,h=0,rgb=(0,0,0),surface: pygame.Surface = None) -> None:
        self.surface = surface if surface is not None else pygame.Surface((w,h))
        self.rgb = rgb
        self.active = True

    def draw(self):
        pygame.draw.rect(self.get_surface(),self.rgb,(0,0,self.get_surface().get_width(),self.get_surface().get_height()))

    def change_background(self,rgb: tuple):
        self.rgb = rgb

class Image(Element):
    def __init__(self) -> None:
        self.active = True


class Panel(Rect):
    elements: list
    entered: Element
    is_entered: bool
    def __init__(self, w=0, h=0, rgb=(0, 0, 0), surface: pygame.Surface = None) -> None:
        super().__init__(w, h, rgb, surface)
        self.elements = []
        self.entered = None
        self.is_entered = False
        self.register_mouse_event(Behaviors.EVENT_MOUSE_ENTER,print,'enter')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_LEAVE,print,'leave')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_LEFTCLICK,print,'left_click')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_RIGHTCLICK,print,'right_click')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELUP,print,'wheel_up')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELDOWN,print,'wheel_down')
        self.register_mouse_event(Behaviors.EVENT_MOUSE_WHEELCLICK,print,'wheel_click')
      
    def add(self,element:Element,x: int,y: int):
        element.set_point(x,y)
        element.set_abs_point(self.absx + x,self.absy + y)
        if element not in self.elements:
            self.elements.append(element)

    def draw(self):
        pygame.draw.rect(self.surface,self.rgb,(0,0,self.surface.get_width(),self.surface.get_height()))
        e:Element
        for e in self.elements:
            e.draw()
            self.surface.blit(e.get_surface(),(e.get_x(),e.get_y()))

    def _on_mouse_enter(self):
        super()._on_mouse_enter()
        self.is_entered = True

    def _on_mouse_leave(self):
        super()._on_mouse_leave()
        self.is_entered = False

    def _on_mouse_motion(self, x, y) -> bool:
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                if self.entered != e:
                    if self.entered is not None:
                        self.entered._on_mouse_leave()
                    else:
                        self._on_mouse_leave()
                    e._on_mouse_enter()
                    self.entered = e
                e._on_mouse_motion(x,y)
                break
        if not collided:
            if self.entered is not None:
                self.entered._on_mouse_exit()
                self.entered = None
            elif not self.is_entered:
                self._on_mouse_enter()

    def _on_mouse_right_click(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_right_click(x,y)
                break
        if not collided:
            super()._on_mouse_right_click(x,y)

    def _on_mouse_left_click(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_left_click(x,y)
                break
        if not collided:
            super()._on_mouse_left_click(x,y)

    def _on_mouse_wheel_down(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_down(x,y)
                break
        if not collided:
            super()._on_mouse_wheel_down(x,y)

    def _on_mouse_wheel_up(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_up(x,y)
                break
        if not collided:
            super()._on_mouse_wheel_up(x,y)

    def _on_mouse_wheel_click(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_click(x,y)
                break
        if not collided:
            super()._on_mouse_wheel_click(x,y)

    def _on_mouse_exit(self):
        if self.entered is not None:
            self.entered._on_mouse_exit()
            self.entered = None
        super()._on_mouse_exit()