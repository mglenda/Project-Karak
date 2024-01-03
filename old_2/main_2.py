import pygame
import sys
from Game import Game

pygame.init()

def main():
    pygame.display.set_caption("Karak")
    game = Game()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                game.on_mouse_motion(pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEBUTTONUP:
                #LEFT CLICK
                if event.button == 1:
                    game.on_mouse_click(pygame.mouse.get_pos())
                #WHEEL CLICK
                if event.button == 2:
                    pass
                #RIGHT CLICK
                if event.button == 3:
                    pass
                #WHEEL UP = 4 
                if event.button == 4:
                    pass
                #WHEEL DOWN = 5
                if event.button == 5:
                    pass

        game.draw()
        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()