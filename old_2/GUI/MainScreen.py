import GUI.Graphics as Graphics
import GUI.CastleScreen as Castle
import pygame

class MainScreen():
    conts = []
    def __init__(self) -> None:
        self.WIDTH = pygame.display.Info().current_w
        self.HEIGHT = pygame.display.Info().current_h
        self.surf = pygame.display.set_mode((self.WIDTH,self.HEIGHT),pygame.FULLSCREEN)
        self.rgb = (255,150,0)

    def add(self,cont:Graphics.GraphicLayoutContainer,x,y):
        cont.set_abs_point(x,y)
        self.conts.append(cont)

    def remove(self,cont:Graphics.GraphicLayoutContainer):
        self.conts.remove(cont)

    def draw(self):
        pygame.draw.rect(self.surf,self.rgb,(0,0,self.surf.get_width(),self.surf.get_height()))
        cont:Graphics.GraphicLayoutContainer
        for cont in self.conts:
            cont.draw()
            self.surf.blit(cont.get_surf(),(cont.get_x(),cont.get_y()))
            
    def _on_mouse_motion(self,coords:tuple):
        x,y = coords[0],coords[1]
        cont:Graphics.GraphicLayoutContainer
        for cont in self.conts:
            if cont._collides(x,y):
                cont._on_mouse_motion(coords)
                break

    def _on_mouse_click(self,coords:tuple):
        x,y = coords[0],coords[1]
        cont:Graphics.GraphicLayoutContainer
        for cont in self.conts:
            if cont._collides(x,y):
                cont._on_mouse_click(coords)
                break