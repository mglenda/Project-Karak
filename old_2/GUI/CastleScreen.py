import GUI.Graphics as Graphics
import pygame

class CastleScreen(Graphics.GraphicLayoutContainer):
    def __init__(self,w,h):
        self.WIDTH = w - 20
        self.HEIGHT = h * 0.92
        self.tilse_size = h / 7.68
        self.START_X = self.WIDTH / 2 - self.tilse_size / 2
        self.START_Y = self.HEIGHT * 0.4 - self.tilse_size / 2

        super().__init__(Graphics.Background(w=self.WIDTH,h=self.HEIGHT,rgb=(25,25,25)))

    def _on_mouse_motion(self, coords: tuple):
        super()._on_mouse_motion(coords)

    def get_tile_size(self):
        return self.tilse_size
    
    def set_tile_size(self,tile_size):
        self.tilse_size = tile_size

    def get_start_x(self):
        return self.START_X
    
    def get_start_y(self):
        return self.START_Y