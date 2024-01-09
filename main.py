import pygame
import sys
from Game import GAME

def main():
    pygame.display.set_caption("Karak")
    pygame.font.init()
    GAME.start()
    _unicode_pressed: str = ''
    now = None
    while True:
        key_pressed = False
        for event in pygame.event.get():
            coords = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                GAME.get_screen()._on_mouse_motion(x=coords[0],y=coords[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                #LEFT CLICK
                if event.button == 1:
                    GAME.get_screen()._on_mouse_left_click(x=coords[0],y=coords[1])
                #WHEEL CLICK
                if event.button == 2:
                    GAME.get_screen()._on_mouse_wheel_click(x=coords[0],y=coords[1])
                #RIGHT CLICK
                if event.button == 3:
                    GAME.get_screen()._on_mouse_right_click(x=coords[0],y=coords[1])
                #WHEEL UP = 4 
                if event.button == 4:
                    GAME.get_screen()._on_mouse_wheel_up(x=coords[0],y=coords[1])
                #WHEEL DOWN = 5
                if event.button == 5:
                    GAME.get_screen()._on_mouse_wheel_down(x=coords[0],y=coords[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #LEFT CLICK
                if event.button == 1:
                    GAME.get_screen()._on_mouse_left_press(x=coords[0],y=coords[1])
                #WHEEL CLICK
                if event.button == 2:
                    GAME.get_screen()._on_mouse_wheel_press(x=coords[0],y=coords[1])
                #RIGHT CLICK
                if event.button == 3:
                    GAME.get_screen()._on_mouse_right_press(x=coords[0],y=coords[1])
            elif event.type == pygame.KEYDOWN:
                GAME.get_screen()._on_key_pressed(event.key,event.unicode)
                _unicode_pressed = event.unicode
                key_pressed = True
            elif event.type == pygame.KEYUP:
                if _unicode_pressed == event.unicode:
                    _unicode_pressed = ''
                GAME.get_screen()._on_key_released(event.key,event.unicode)
            elif event.type == pygame.WINDOWENTER:
                now = pygame.time.get_ticks() + 50

        if now is not None and pygame.time.get_ticks() - now >= 0:
            now = None
            GAME.get_screen().draw()
                
        if not key_pressed:
            keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if True in keys:
                GAME.get_screen()._on_key_hold(keys,_unicode_pressed)

        GAME.run_timers()

        pygame.display.update()
        pygame.time.Clock().tick(120)

if __name__ == "__main__":
    main()