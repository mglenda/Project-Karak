import pygame
import sys
from Game import GAME

def main():
    pygame.display.set_caption("Karak")
    pygame.font.init()
    GAME.start()

    while True:
        for event in pygame.event.get():
            coords = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                GAME.ui.on_mouse_motion(x=coords[0],y=coords[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                #LEFT CLICK
                if event.button == 1:
                    GAME.ui.on_mouse_left_click(x=coords[0],y=coords[1])
                #WHEEL CLICK
                if event.button == 2:
                    GAME.ui.on_mouse_wheel_click(x=coords[0],y=coords[1])
                #RIGHT CLICK
                if event.button == 3:
                    GAME.ui.on_mouse_right_click(x=coords[0],y=coords[1])
                #WHEEL UP = 4 
                if event.button == 4:
                    GAME.ui.on_mouse_wheel_up(x=coords[0],y=coords[1])
                #WHEEL DOWN = 5
                if event.button == 5:
                    GAME.ui.on_mouse_wheel_down(x=coords[0],y=coords[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #LEFT CLICK
                if event.button == 1:
                    GAME.ui.on_mouse_left_press(x=coords[0],y=coords[1])
                #WHEEL CLICK
                if event.button == 2:
                    GAME.ui.on_mouse_wheel_press(x=coords[0],y=coords[1])
                #RIGHT CLICK
                if event.button == 3:
                    GAME.ui.on_mouse_right_press(x=coords[0],y=coords[1])
                    
        GAME.update()
        GAME.draw()

if __name__ == "__main__":
    main()