import pygame
import sys
from Game import GAME
from DataLoader import DataLoader
from threading import Thread

class AppLogic():
    thread: Thread
    running: bool
    def __init__(self):
        self.thread = Thread(target=self.update,daemon=True)
        
    def start(self):
        self.running = True
        self.thread.start()

    def update(self):
        while self.running:
            GAME.update()
            pygame.time.Clock().tick(60)

    def quit(self):
        self.running = False
        self.thread.join()

class Graphics():
    thread: Thread
    running: bool
    def __init__(self):
        self.thread = Thread(target=self.update,daemon=True)
    
    def start(self):
        self.running = True
        self.thread.start()

    def update(self):
        while self.running:
            GAME.update_gui()
            pygame.time.Clock().tick(60)

    def quit(self):
        self.running = False
        self.thread.join()

def main():
    pygame.display.set_caption("Karak")
    pygame.font.init()
    DataLoader.load()

    GAME.start()

    app_logic = AppLogic()
    graphics = Graphics()

    app_logic.start()
    graphics.start()

    while GAME.is_running():
        for event in pygame.event.get():
            coords = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                GAME.quit()
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
        GAME.draw()
        pygame.time.Clock().tick(120)

    app_logic.quit()
    graphics.quit()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()