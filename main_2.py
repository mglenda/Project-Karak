import pygame
import sys
import GUI.MainScreen as MainScreen

pygame.init()

def main():
    pygame.display.set_caption("Karak")
    screen = MainScreen.MainScreen()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                screen._on_mouse_motion(pygame.mouse.get_pos())
        screen.draw()
        pygame.display.update()

if __name__ == "__main__":
    main()