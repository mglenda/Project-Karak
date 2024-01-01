import pygame
import sys
import Screen
import GameLogic
import Controllers

# Initialize Pygame
pygame.init()
    
# Main function
def main():
    pygame.display.set_caption("Karak")

    #CREATE UI START
    main_screen = Screen.MainScreen()
    #CREATE UI END

    controller = Controllers.MainController(GameLogic.Game())

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                controller.mouse_motion(main_screen,pygame.mouse.get_pos())
            elif event.type == pygame.MOUSEWHEEL:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #LEFT CLICK
                if event.button == 1:
                    controller.mouse_left_click(main_screen)
                #WHEEL CLICK
                if event.button == 2:
                    pass
                #RIGHT CLICK
                if event.button == 3:
                    pass
                #WHEEL UP = 4 
                if event.button == 4:
                    controller.mouse_wheel_up(main_screen)
                #WHEEL DOWN = 5
                if event.button == 5:
                    controller.mouse_wheel_down(main_screen)

        controller.keyboard_hold_handler(pygame.key.get_pressed(),main_screen)

        main_screen.draw()
        pygame.display.update()
        main_screen.set_fps(60)
        
if __name__ == "__main__":
    main()