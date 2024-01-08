from GameLogic.Hero import Hero
from GameLogic.Placeable import Placeable
from GUI.Frame import Frame,FRAMEPOINT
from GUI.GraphicComponents import Image,TileInterface,Rect
from GUI.PlaceableWidget import PlaceableWidget
from Game import GAME

PATH = '_Textures\\Tiles\\Retextured\\'

class Tile(TileInterface):
    _texture: str
    _pathing: tuple
    _active_layer: Image
    _press_layer: Image
    _placeable_widget: PlaceableWidget
    _c: int
    _r: int
    _heroes: list
    _placeable: Placeable
    _is_spawn: bool
    _placed: bool
    def __init__(self, parent: Rect,c: int,r :int) -> None:
        super().__init__(parent.get_tilesize(),parent.get_tilesize(), self._texture, parent)

        self._c = c
        self._r = r

        self._placeable_widget = PlaceableWidget(self.get_w()*0.6,self.get_h()*0.6,PATH + 'FocusedLayer.png',self)
        self._placeable_widget._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._active_layer = Image(self.get_w(),self.get_h(),PATH + 'FocusedLayer.png',self)
        self._active_layer._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer = Image(self.get_w(),self.get_h(),PATH + 'FocusedLayer.png',self)
        self._press_layer._set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer._set_visible(False)
        self._active_layer._set_visible(False)
        self._placeable_widget._set_visible(False)

        self._placeable = None
        self._placed = False

        self._heroes = []
        self.set_active(True)

    def add_placeable(self, placeable: Placeable):
        self._placeable = placeable
        self._placeable_widget.load_placeable(placeable)
        self._placeable_widget.set_visible(True)

    def get_placeable(self) -> Placeable:
        return self._placeable
    
    def remove_placeable(self):
        self._placeable = None
        self._placeable_widget.set_visible(False)

    def is_placed(self) -> bool:
        return self._placed
    
    def set_placed(self, placed: bool):
        self._placed = placed

    def add_hero(self, hero: Hero):
        self._heroes.append(hero)

    def is_spawn(self) -> bool:
        return self._is_spawn

    def remove_hero(self, hero: Hero):
        self._heroes.remove(hero)

    def get_c(self):
        return self._c
    
    def get_r(self):
        return self._r
    
    def set_active(self, active: bool):
        super().set_active(active)
        if active == False:
            self._active_layer.set_visible(False)
            self._press_layer.set_visible(False)
        else:
            self._active_layer.set_visible(True)

    def _on_mouse_enter(self):
        self._press_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._press_layer.set_visible(False)
        super()._on_mouse_leave()

    def _on_mouse_left_click(self, x, y):
        super()._on_mouse_left_click(x, y)

    def _on_mouse_left_press(self, x, y):
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
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Start(Tile):
    _texture = PATH + 'Start.png'
    _pathing = (1,1,1,1)
    _is_spawn = False
    def __init__(self, parent: Rect) -> None:
        super().__init__(parent, 0, 0)

class CorridorCorner(Tile):
    _texture = PATH + 'CorridorCorner.png'
    _pathing = (0,1,1,0)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Arena(Tile):
    _texture = PATH + 'Arena.png'
    _pathing = (1,0,1,0)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Chamber(Tile):
    _texture = PATH + 'Chamber.png'
    _pathing = (1,0,1,0)
    _is_spawn = True
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberCorner(Tile):
    _texture = PATH + 'ChamberCorner.png'
    _pathing = (0,1,1,0)
    _is_spawn = True
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberCross(Tile):
    _texture = PATH + 'ChamberCross.png'
    _pathing = (1,1,1,1)
    _is_spawn = True
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class ChamberT(Tile):
    _texture = PATH + 'ChamberT.png'
    _pathing = (0,1,1,1)
    _is_spawn = True
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Corridor(Tile):
    _texture = PATH + 'Corridor.png'
    _pathing = (1,0,1,0)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class CorridorCross(Tile):
    _texture = PATH + 'CorridorCross.png'
    _pathing = (1,1,1,1)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class CorridorT(Tile):
    _texture = PATH + 'CorridorT.png'
    _pathing = (1,0,1,1)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Curse(Tile):
    _texture = PATH + 'Curse.png'
    _pathing = (1,1,1,1)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Fountain(Tile):
    _texture = PATH + 'Fountain.png'
    _pathing = (0,1,1,0)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)

class Portal(Tile):
    _texture = PATH + 'Portal.png'
    _pathing = (1,0,1,0)
    _is_spawn = False
    def __init__(self, parent: Rect, c: int, r: int) -> None:
        super().__init__(parent, c, r)