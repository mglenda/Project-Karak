import GUI.Graphics as Graphics
from GUI.TileMap import TileMap
import pygame

class CastleScreen(Graphics.GraphicLayoutContainer):
    def __init__(self,w,h):
        self.WIDTH = w - 20
        self.HEIGHT = h * 0.92
        self.tilse_size = h / 7.68
        self.START_X = self.WIDTH / 2 - self.tilse_size / 2
        self.START_Y = self.HEIGHT * 0.4 - self.tilse_size / 2
        self.tilemap = TileMap()

        super().__init__(Graphics.GraphicElement(w=self.WIDTH,h=self.HEIGHT,rect=(25,25,25)))

        start_zone = self.tilemap.create_starting_zone(w=self.tilse_size,h=self.tilse_size)
        self.add(start_zone)
        start_zone.set_abs_point(x=self.START_X,y=self.START_Y)

    def _on_mouse_motion(self, coords: tuple):
        super()._on_mouse_motion(coords)

    def get_tile_size(self):
        return self.tilse_size