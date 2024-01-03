import pygame
import sys
import Controller

pygame.init()

game = Controller.Main()

def main():
    pygame.display.set_caption("Karak")
    pygame.font.init()

    while True:
        for event in pygame.event.get():
            coords = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                game._on_mouse_motion(x=coords[0],y=coords[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                #LEFT CLICK
                if event.button == 1:
                    game._on_mouse_left_click(x=coords[0],y=coords[1])
                #WHEEL CLICK
                if event.button == 2:
                    game._on_mouse_wheel_click(x=coords[0],y=coords[1])
                #RIGHT CLICK
                if event.button == 3:
                    game._on_mouse_right_click(x=coords[0],y=coords[1])
                #WHEEL UP = 4 
                if event.button == 4:
                    game._on_mouse_wheel_up(x=coords[0],y=coords[1])
                #WHEEL DOWN = 5
                if event.button == 5:
                    game._on_mouse_wheel_down(x=coords[0],y=coords[1])
            elif event.type == pygame.KEYDOWN:
                game._on_key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                game._on_key_released(event.key)
        for key,is_pressed in enumerate(pygame.key.get_pressed()):
            if is_pressed == True:
                game._on_key_hold(key)
        game.draw()
        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == "__main__":
    main()