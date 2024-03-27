from GraphicsEngine.Frame import Frame
import pygame

class Screen(Frame):
    def __init__(self):
        super().__init__(None)
        self.set_w(pygame.display.Info().current_w)
        self.set_h(pygame.display.Info().current_h)
        self.surface = pygame.display.set_mode((self.w,self.h),pygame.FULLSCREEN)
        self.visible = True
        self.active = True

    def draw(self):
        self.surface.fill((0,0,0))
        self.surface.blits(self.get_blits_children())
        pygame.display.update()