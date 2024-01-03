import pygame

TOPLEFT = 0
TOP = 1
TOPRIGHT = 2
LEFT = 3
CENTER = 4
RIGHT = 5
BOTTOMLEFT = 6
BOTTOM = 7
BOTTOMRIGHT = 8

class GraphicElement():
    x,y = None,None
    visible = True
    parent = None
    def __init__(self,img:str,w=50,h=50):
        """
        Parameters
        ----------
        surf : pygame.Surface optional
            undefined = pygame.Surface((w,h))
        w (width) : int optional
            undefined = 50 or surf.get_width() if surf was passed
        h (height): int optional
            undefined = 50 or surf.get_height() if surf was passed
        rect : tuple optional (r,g,b) 
            if defined than rectangle will be drawn as background
        img : str optional (filepath)
            if defined it will try to load file and use it as content
        """
        self.img = pygame.image.load(img).convert_alpha()
        self.surf = self.img
        self.w = w
        self.h = h
        self.angle = 0

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y

    def get_surf(self):
        return self.surf

    def set_visible(self,visible):
        self.visible = visible

    def is_visible(self):
        return self.visible
    
    def set_parent(self,parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def draw(self):
        if self.get_x() is not None and self.get_y() is not None:
            self.surf = self.img
            self.surf = pygame.transform.scale(self.surf,(self.w,self.h))
            self.surf = pygame.transform.rotate(self.surf,self.angle)

class Background():
    def __init__(self,w,h,rgb):
        self.surf = pygame.Surface((w,h))
        self.rgb = rgb

    def get_surf(self):
        return self.surf
    
    def set_rgb(self,rgb):
        self.rgb = rgb

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def set_x(self,x):
        self.x = x

    def set_y(self,y):
        self.y = y
    
    def draw(self):
        pygame.draw.rect(self.surf,self.rgb,(0,0,self.surf.get_width(),self.surf.get_height()))
    
class GraphicLayout():
    elements = []
    at_x,at_y = None,None
    parent = None
    def __init__(self,main:Background) -> None:
        self.main = main

    def add(self,child:GraphicElement,align_parent:int = None,align_child:int = None):
        align_child = TOPLEFT if align_child is None else align_child
        align_parent = TOPLEFT if align_parent is None else align_parent
        self.elements.append({'element': child
                              ,'align_child': align_child
                              ,'align_parent': align_parent})
        child.set_parent(self)

    def remove(self,child:GraphicElement):
        self.elements.remove(child)
        child.set_parent(None)

    def get_elements(self):
        return self.elements
    
    def set_abs_point(self,x,y):
        self.main.set_x(x)
        self.main.set_y(y)
        self.at_x = x
        self.at_y = y

    def get_x(self):
        return self.main.get_x()
    
    def get_y(self):
        return self.main.get_y()
    
    def get_surf(self):
        return self.main.get_surf()
    
    def set_parent(self,parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def align(self,element:GraphicElement,align_parent:int,align_child:int):
        x:int
        y:int
        if align_parent == TOPLEFT:
            x,y = self.get_x(),self.get_y()
        element.set_x(x)
        element.set_y(y)

    def draw(self):
        self.main.draw()
        for d in self.elements:
            element:GraphicElement = d['element']
            if element.is_visible():
                self.align(element,d['align_parent'],d['align_child'])
                element.draw()
                if element.get_x() is not None and element.get_y() is not None:
                    self.main.get_surf().blit(element.get_surf(),(0,0))

    def set_background(self,rgb:tuple):
        self.main.set_rgb(rgb)

    def _collides(self,x,y):
        if self.at_y is None or self.at_x is None:
            return False
        ax,ay = self.at_x,self.at_y
        ax += self.get_parent().at_x
        ay += self.get_parent().at_y
        x -= ax
        y -= ay
        return self.get_surf().get_rect().collidepoint(x,y)
    
    def _on_mouse_enter(self,coords: tuple):
        pass

    def _on_mouse_leave(self):
        pass

    def _on_mouse_click(self,coords: tuple):
        pass

class GraphicLayoutContainer():
    layouts = []
    at_x,at_y = None,None
    _focused_layout:GraphicLayout = None
    def __init__(self,main:Background):
        self.main = main

    def add(self,child:GraphicLayout):
        self.layouts.append(child)
        child.set_parent(self)

    def remove(self,child:GraphicLayout):
        self.layouts.remove(child)
        child.set_parent(None)

    def get_layouts(self):
        return self.layouts
    
    def set_abs_point(self,x,y):
        self.main.set_x(x)
        self.main.set_y(y)
        self.at_x = x
        self.at_y = y

    def get_x(self):
        return self.main.get_x()
    
    def get_y(self):
        return self.main.get_y()
    
    def get_surf(self):
        return self.main.get_surf()
    
    def draw(self):
        self.main.draw()
        layout:GraphicLayout
        for layout in self.layouts:
            layout.draw()
            if layout.get_x() is not None and layout.get_y() is not None:
                self.main.get_surf().blit(layout.get_surf(),(layout.get_x(),layout.get_y()))

    def set_background(self,rgb:tuple):
        self.main.set_rect(rgb)

    def _collides(self,x,y):
        if self.at_y is None or self.at_x is None:
            return False
        x -= self.at_x
        y -= self.at_y
        return self.get_surf().get_rect().collidepoint(x,y)
    
    def _on_mouse_motion(self,coords: tuple):
        x,y = coords[0],coords[1]
        layout:GraphicLayout
        for layout in self.layouts:
            if layout._collides(x,y):
                if self._focused_layout != layout:
                    if self._focused_layout is not None:
                        self._focused_layout._on_mouse_leave()
                    self._focused_layout = layout
                    layout._on_mouse_enter(coords)
                return
        if self._focused_layout is not None:
            self._focused_layout._on_mouse_leave()
        self._focused_layout = None

    def _on_mouse_click(self,coords: tuple):
        x,y = coords[0],coords[1]
        layout:GraphicLayout
        for layout in self.layouts:
            if layout._collides(x,y):
                layout._on_mouse_click(coords)