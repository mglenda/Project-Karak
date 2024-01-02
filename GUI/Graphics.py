import pygame

class GraphicElement():
    x,y = None,None
    def __init__(self,surf:pygame.Surface=None,w=50,h=50,rect:tuple=None,img:str=None):
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
        self.surf = pygame.Surface((w,h)) if surf is None else surf
        self.w = self.surf.get_width()
        self.h = self.surf.get_height()
        self.rect = rect
        self.angle = 0
        if img is not None:
            self.img = pygame.image.load(img).convert_alpha()
        else:
            self.img = None

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
    
    def set_rect(self,rect):
        self.rect = rect

    def draw(self):
        if self.get_x() is not None and self.get_y() is not None:
            if self.rect is not None:
                pygame.draw.rect(self.surf,self.rect,(0,0,self.surf.get_width(),self.surf.get_height()))
            if self.img is not None:
                self.img_tmp = self.img
                self.img_tmp = pygame.transform.scale(self.img_tmp,(self.w,self.h))
                self.img_tmp = pygame.transform.rotate(self.img_tmp,self.angle)
                self.surf.blit(self.img_tmp,(0,0))
    
class GraphicLayout():
    elements = []
    at_x,at_y = None,None
    def __init__(self,main:GraphicElement) -> None:
        self.main = main

    def add(self,child:GraphicElement):
        self.elements.append(child)

    def remove(self,child:GraphicElement):
        self.elements.remove(child)

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
    
    def draw(self):
        self.main.draw()
        element:GraphicElement
        for element in self.elements:
            element.draw()
            self.main.get_surf().blit(element.get_surf(),(element.get_x(),element.get_y()))

    def set_background(self,rgb:tuple):
        self.main.set_rect(rgb)

    def _collides(self,x,y):
        if self.at_y is None or self.at_x is None:
            return False
        x -= self.at_x
        y -= self.at_y
        return self.get_surf().get_rect().collidepoint(x,y)
    
    def _on_mouse_motion(self,coords: tuple):
        pass

class GraphicLayoutContainer():
    layouts = []
    at_x,at_y = None,None
    def __init__(self,main:GraphicElement):
        self.main = main

    def add(self,child:GraphicLayout):
        self.layouts.append(child)

    def remove(self,child:GraphicLayout):
        self.layouts.remove(child)

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
        pass