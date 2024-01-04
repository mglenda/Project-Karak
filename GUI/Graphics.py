import pygame
from GUI.Behaviors import MouseBehavior

FONT_PATH = 'Fonts\\BreatheFireIii-PKLOB.ttf'

ATTPOINT_TOP = 0
ATTPOINT_TOPLEFT = 1
ATTPOINT_TOPRIGHT = 2
ATTPOINT_CENTER = 3
ATTPOINT_LEFT = 4
ATTPOINT_RIGHT = 5
ATTPOINT_BOTTOM = 6
ATTPOINT_BOTTOMLEFT = 7
ATTPOINT_BOTTOMRIGHT = 8

class Element(MouseBehavior):
    active: bool
    visible: bool
    surface: pygame.Surface
    x: int
    y: int
    absx: int
    absy: int
    elements: list

    def draw(self):
        pass

    def coolide(self,x: int,y: int) -> bool:
        return x >= self.absx and x <= self.absx + self.surface.get_width() and y >= self.absy and y <= self.absy + self.surface.get_height() and self.is_visible()

    def set_active(self,active:bool):
        self.active = active

    def is_active(self) -> bool:
        return self.active
    
    def is_visible(self) -> bool:
        return self.visible
    
    def set_visible(self,visible: bool):
        self.visible = visible
    
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

    def add_attached(self,child):
        pass

    def get_attached(self):
        pass

    def attach(self,parent,attach_point_parent: int,attach_point_element: int,x_offset: int = 0,y_offset: int = 0):
        pass

    def get_elements(self):
        if hasattr(self,'elements'):
            return self.elements
        else:
            return []

class AttachableElement(Element):
    _attached_elements: list

    def __init__(self) -> None:
        self._attached_elements = []
        self.x = 0
        self.y = 0
        self.absx = 0
        self.absy = 0

    # Parent can only be his real parent, or his sibling
    def attach(self,parent:Element,attach_point_parent: int,attach_point_element: int,x_offset: int = 0,y_offset: int = 0):
        self.set_visible(True)
        is_child: bool = self in parent.get_elements()
        x:int = 0 if is_child else parent.get_x()
        y:int = 0 if is_child else parent.get_y()
        px:int = x
        py:int = y

        if attach_point_parent == ATTPOINT_CENTER:
            x += parent.get_surface().get_width() / 2
            y += parent.get_surface().get_height() / 2
        if attach_point_parent == ATTPOINT_TOP:
            x += parent.get_surface().get_width() / 2
        if attach_point_parent == ATTPOINT_TOPRIGHT:
            x += parent.get_surface().get_width()
        if attach_point_parent == ATTPOINT_BOTTOM:
            x += parent.get_surface().get_width() / 2
            y += parent.get_surface().get_height()
        if attach_point_parent == ATTPOINT_BOTTOMLEFT:
            y += parent.get_surface().get_height()
        if attach_point_parent == ATTPOINT_BOTTOMRIGHT:
            x += parent.get_surface().get_width()
            y += parent.get_surface().get_height()
        if attach_point_parent == ATTPOINT_LEFT:
            y += parent.get_surface().get_height() / 2
        if attach_point_parent == ATTPOINT_RIGHT:
            y += parent.get_surface().get_height() / 2
            x += parent.get_surface().get_width()
        
        if attach_point_element == ATTPOINT_TOP:
            x -= self.get_surface().get_width() / 2
        if attach_point_element == ATTPOINT_TOPRIGHT:
            x -= self.get_surface().get_width()
        if attach_point_element == ATTPOINT_CENTER:
            x -= self.get_surface().get_width() / 2
            y -= self.get_surface().get_height() / 2
        if attach_point_element == ATTPOINT_BOTTOM:
            x -= self.get_surface().get_width() / 2
            y -= self.get_surface().get_height()
        if attach_point_element == ATTPOINT_BOTTOMLEFT:
            y -= self.get_surface().get_height()
        if attach_point_element == ATTPOINT_BOTTOMRIGHT:
            x -= self.get_surface().get_width()
            y -= self.get_surface().get_height()
        if attach_point_element == ATTPOINT_LEFT:
            y -= self.get_surface().get_height() / 2
        if attach_point_element == ATTPOINT_RIGHT:
            y -= self.get_surface().get_height() / 2
            x -= self.get_surface().get_width()
        
        x += x_offset
        y += y_offset
        self.set_point(x,y)
        self.set_abs_point(parent.absx + (x - px),parent.absy + (y - py))
        parent.add_attached(self)

    def get_attached(self):
        return self._attached_elements
    
    def add_attached(self, child:Element):
        if child not in self._attached_elements:
            self._attached_elements.append(child)

    def set_abs_point(self, x: int, y: int):
        if self.absx != x or self.absy != y:
            super().set_abs_point(x, y)
            element:Element
            for element in self._attached_elements:
                is_child: bool = element in self.get_elements()
                px:int = 0 if is_child else self.get_x()
                py:int = 0 if is_child else self.get_y()
                element.set_abs_point(self.absx + (element.get_x() - px),self.absy + (element.get_y() - py))

class ElementContainer(AttachableElement):
    entered: Element
    is_entered: bool
    def __init__(self):
        super().__init__()
        self.elements = []
        self.entered = None
        self.is_entered = False

    def add(self,element:AttachableElement,attach_point_panel: int = None,attach_point_element: int = None,x_offset: int = 0,y_offset: int = 0):
        if attach_point_panel is not None and attach_point_element is not None:
            element.attach(self,attach_point_panel,attach_point_element,x_offset,y_offset)
        if element not in self.elements:
            self.elements.append(element)

    def remove(self,element:Element):
        self.elements.remove(element)
        element.set_visible(False)

    def remove_all(self):
        element:Element
        for element in self.elements:
            element.set_visible(False)
        self.elements = []

    def draw(self):
        e:Element
        for e in self.elements:
            if e.is_visible():
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
        if self.is_active():
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
        if not collided and self.is_active():
            super()._on_mouse_right_click(x,y)

    def _on_mouse_left_click(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_left_click(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_left_click(x,y)

    def _on_mouse_wheel_down(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_down(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_wheel_down(x,y)

    def _on_mouse_wheel_up(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_up(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_wheel_up(x,y)

    def _on_mouse_wheel_click(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_click(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_wheel_click(x,y)

    def _on_mouse_left_press(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_left_press(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_left_press(x,y)

    def _on_mouse_right_press(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_right_press(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_right_press(x,y)

    def _on_mouse_wheel_press(self,x,y):
        e:Element
        collided: bool = False
        for e in reversed(self.elements):
            collided = e.is_active() and e.coolide(x,y)
            if collided:
                e._on_mouse_wheel_press(x,y)
                break
        if not collided and self.is_active():
            super()._on_mouse_wheel_press(x,y)

    def _on_mouse_exit(self):
        if self.entered is not None:
            self.entered._on_mouse_exit()
            self.entered = None
        super()._on_mouse_exit()

class Rect(AttachableElement):
    def __init__(self,w=0,h=0,rgb=(0,0,0),surface: pygame.Surface = None) -> None:
        super().__init__()
        self.surface = surface if surface is not None else pygame.Surface((w,h))
        self.rgb = rgb
        self.active = False
        self.visible = False

    def draw(self):
        pygame.draw.rect(self.get_surface(),self.rgb,(0,0,self.get_surface().get_width(),self.get_surface().get_height()))

    def change_background(self,rgb: tuple):
        self.rgb = rgb

class Image(AttachableElement):
    def __init__(self,w: int,h :int,filepath: str) -> None:
        super().__init__()
        self.active = False
        self.visible = False
        self._stored = pygame.image.load(filepath).convert_alpha()
        self.surface = self._stored
        self.w = w
        self.h = h
        self.angle = 0
        self.refresh()

    def refresh(self):
        self.surface = self._stored
        self.surface = pygame.transform.scale(self.surface,(self.w,self.h))
        if self.angle != 0:
            self.surface = pygame.transform.rotate(self.surface,self.angle)

    def resize(self,w: int,h: int):
        self.w = w
        self.h = h
        self.refresh()

    def change_image(self,filepath: str):
        self._stored = pygame.image.load(filepath).convert_alpha()
        self.refresh()


class Panel(ElementContainer):
    entered: Element
    is_entered: bool
    def __init__(self, w=0, h=0, rgb=(0, 0, 0), surface: pygame.Surface = None,img_path: str = None) -> None:
        super().__init__()
        self.rgb = rgb
        self.active = True
        self.visible = False
        self.w = w
        self.h = h
        self.angle = 0
        self.img_path = img_path
        if surface is None:
            if self.img_path is not None:
                self._stored = pygame.image.load(img_path).convert_alpha()
                self.surface = self._stored
            else:
                self.surface = pygame.Surface((w,h))
        else:
            self.surface = surface
        self.refresh()

    def change_background(self,rgb: tuple = None,img_path: str = None):
        if img_path is not None:
            self.img_path = img_path
            self._stored = pygame.image.load(img_path).convert_alpha()
        else:
            self.rgb = rgb
        self.refresh()

    def resize(self,w: int,h: int):
        self.w = w
        self.h = h
        if self.img_path is not None:
            self.refresh()
        else:
            self.surface = pygame.Surface(w,h)

    def refresh(self):
        if self.img_path is not None:
            self.surface = self._stored 
            self.surface = pygame.transform.scale(self.surface,(self.w,self.h))
            if self.angle != 0:
                self.surface = pygame.transform.rotate(self.surface,self.angle)

    def draw(self):
        if self.img_path is None:
            pygame.draw.rect(self.surface,self.rgb,(0,0,self.surface.get_width(),self.surface.get_height()))
        else:
            self.refresh()
        super().draw()

class TextField(AttachableElement):
    def __init__(self, font_rgb: tuple = (255,255,255),font_size: int = 15,text:str = '',max_length:int = 15) -> None:
        super().__init__()
        self.font = pygame.font.Font(FONT_PATH,font_size)
        self.font_rgb = font_rgb
        self.text = text
        self.visible = False
        self.active = False
        self.max_length = max_length
        self.set_text(text)
        self.surface = self.font.render(self.text,False,self.font_rgb)
        
    def set_text(self,text:str):
        if len(text) > self.max_length:
            text = text[:self.max_length]
        self.text = text

    def set_color(self,font_rgb:tuple):
        self.font_rgb = font_rgb
        
    def set_font_size(self,font_size:int):
        self.font = pygame.font.Font(FONT_PATH,font_size)

    def get_text(self) -> str:
        return self.text

    def draw(self):
        w = self.surface.get_width()/2
        self.surface = self.font.render(self.text,False,self.font_rgb)
        if w != self.surface.get_width():
            self.x = self.x + (w - (self.surface.get_width()/2))