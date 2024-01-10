import pygame
import sys
pygame.init()

w = pygame.display.Info().current_w
h = pygame.display.Info().current_h

pygame.display.set_mode((w,h),pygame.FULLSCREEN)
pygame.display.get_surface().fill((40,40,40))

pygame.event.set_blocked(None)
pygame.event.set_allowed([pygame.MOUSEMOTION,pygame.MOUSEBUTTONUP,pygame.MOUSEBUTTONDOWN,pygame.KEYDOWN,pygame.KEYUP,pygame.QUIT])

s = pygame.image.load("_Textures\\Heroes\\MyIcons\\Barbarian.png")
s.convert_alpha()

def add_surface():
    pygame.display.get_surface().fill((40,40,40))
    pygame.display.get_surface().blit(s,(300,300))
    pygame.display.update()

def alpha_surface():
    s.set_alpha(100)
    pygame.display.update()

while True:
    event: pygame.event.Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            #LEFT CLICK
            if event.button == 1:
                add_surface()
            #WHEEL CLICK
            if event.button == 2:
                pass
            #RIGHT CLICK
            if event.button == 3:
                alpha_surface()
        if event.type == pygame.MOUSEBUTTONUP:
            pass