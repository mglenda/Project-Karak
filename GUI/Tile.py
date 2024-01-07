from GameLogic.Hero import Hero
from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Image,TileInterface
from Game import GAME

PATH = '_Textures\\Tiles\\Retextured\\'

class Tile(TileInterface):
    _texture: str
    _pathing: tuple
    _focus_layer: Image
    _press_layer: Image
    _c: int
    _r: int
    _heroes: list
    def __init__(self, parent: Frame,c: int,r :int) -> None:
        super().__init__(parent.get_tilesize(),parent.get_tilesize(), self._texture, parent)

        self._c = c
        self._r = r

        self._focus_layer = Image(self.get_w(),self.get_h(),PATH + 'FocusedLayer.png',self)
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer = Image(self.get_w(),self.get_h(),PATH + 'FocusedLayer.png',self)
        self._press_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer.set_visible(False)
        self._focus_layer.set_visible(False)

        self._heroes = []
        self.set_active(True)

    def add_hero(self, hero: Hero):
        self._heroes.append(hero)

    def remove_hero(self, hero: Hero):
        self._heroes.remove(hero)

    def get_c(self):
        return self._c
    
    def get_r(self):
        return self._r
    
    def set_active(self, active: bool):
        super().set_active(active)
        if active == False:
            self._focus_layer.set_visible(False)
            self._press_layer.set_visible(False)

    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(False)
        super()._on_mouse_leave()

    def _on_mouse_left_click(self, x, y):
        self._focus_layer.set_visible(True)
        self._press_layer.set_visible(False)
        super()._on_mouse_left_click(x, y)

    def _on_mouse_left_press(self, x, y):
        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(True)
        super()._on_mouse_left_press(x, y)
    
    def is_passable_top(self):
        return self._pathing[0] == 1
    
    def is_passable_right(self):
        return self._pathing[1] == 1
    
    def is_passable_bottom(self):
        return self._pathing[2] == 1
    
    def is_passable_left(self):
        return self._pathing[3] == 1
    
    def rotate_up(self):
        self._pathing = (
            self._pathing[1]
            ,self._pathing[2]
            ,self._pathing[3]
            ,self._pathing[0]
        )
        self.rotate(90)
    
    def rotate_down(self):
        self._pathing = (
            self._pathing[3]
            ,self._pathing[0]
            ,self._pathing[1]
            ,self._pathing[2]
        )
        self.rotate(-90)

class Unknown(Tile):
    _texture = PATH + 'Background.png'
    _pathing = (1,1,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Start(Tile):
    _texture = PATH + 'Start.png'
    _pathing = (1,1,1,1)
    def __init__(self, parent: Frame) -> None:
        super().__init__(parent, 0, 0)

class CorridorCorner(Tile):
    _texture = PATH + 'CorridorCorner.png'
    _pathing = (0,1,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Arena(Tile):
    _texture = PATH + 'Arena.png'
    _pathing = (1,0,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Chamber(Tile):
    _texture = PATH + 'Chamber.png'
    _pathing = (1,0,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberCorner(Tile):
    _texture = PATH + 'ChamberCorner.png'
    _pathing = (0,1,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberCross(Tile):
    _texture = PATH + 'ChamberCross.png'
    _pathing = (1,1,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberT(Tile):
    _texture = PATH + 'ChamberT.png'
    _pathing = (0,1,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Corridor(Tile):
    _texture = PATH + 'Corridor.png'
    _pathing = (1,0,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class CorridorCross(Tile):
    _texture = PATH + 'CorridorCross.png'
    _pathing = (1,1,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class CorridorT(Tile):
    _texture = PATH + 'CorridorT.png'
    _pathing = (1,0,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Curse(Tile):
    _texture = PATH + 'Curse.png'
    _pathing = (1,1,1,1)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Fountain(Tile):
    _texture = PATH + 'Fountain.png'
    _pathing = (0,1,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Portal(Tile):
    _texture = PATH + 'Portal.png'
    _pathing = (1,0,1,0)
    def __init__(self, parent: Frame, c: int, r: int) -> None:
        super().__init__(parent, c, r)