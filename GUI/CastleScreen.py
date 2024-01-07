from GUI.GraphicComponents import Rect
from GUI.Frame import FRAMEPOINT
from GUI._ComponentListeners import KeyBoardListener
from GUI.Tile import Unknown,Start,Tile
import GUI._const_mouseevents as MouseEvent
from GUI.TilePack import TilePack
from GameLogic.Player import Player
from GameLogic.Hero import Hero
from Game import GAME
import pygame

class CastleScreen(Rect,KeyBoardListener):
    _start_tile: Start
    _motion_x: int
    _motion_y: int
    _is_pressed: bool
    _zoom: float
    _player_i: int
    _tilemap: dict
    _tilepack: TilePack
    _tilesize: int
    def __init__(self) -> None:
        super().__init__(GAME.screen.get_w(), GAME.screen.get_h(), (40,40,40), GAME.screen)
        self._tilesize = self.get_h() * 0.15
        self._tilepack = TilePack()
        self._is_pressed = False
        self._zoom = 0.0
        self._player_i = 0
        self.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)

        self._start_tile = Start(self)
        self._start_tile.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._tilemap = {"00": self._start_tile}

        self.set_active(True)

        p: Player
        for p in GAME.players.get_all():
            p.get_hero().set_tile(self._start_tile)
            self._start_tile.add_hero(p.get_hero())

        self.place_tile(self._start_tile)

    def load_action_options(self):
        hero: Hero = self.get_current_hero()

        tile: Tile
        for _,tile in self._tilemap.items():
            if self.are_tiles_accesible(hero.get_tile(),tile):
                tile.set_active(True)
            else:
                tile.set_active(False)

    def are_tiles_accesible(self, tile_one: Tile, tile_two: Tile) -> bool:
        c_one,r_one = tile_one.get_c(),tile_one.get_r()
        c_two,r_two = tile_two.get_c(),tile_two.get_r()
        accesible: bool = False
        if c_one == c_two:
            if r_one - r_two == 1:
                #potential access on TOP
                accesible = tile_one._pathing[0] == 1 and tile_two._pathing[2] == 1
                pass
            elif r_one - r_two == -1:
                #potential access on BOTTOM
                accesible = tile_one._pathing[2] == 1 and tile_two._pathing[0] == 1
                pass

        if r_one == r_two:
            if c_one - c_two == 1:
                #potential access on LEFT
                accesible = tile_one._pathing[3] == 1 and tile_two._pathing[1] == 1
                pass
            elif c_one - c_two == -1:
                #potential access on RIGHT
                accesible = tile_one._pathing[1] == 1 and tile_two._pathing[3] == 1
                pass

        return accesible

    def move_to_tile(self, tile: Tile):
        hero: Hero = self.get_current_hero()
        former_tile: Tile = hero.get_tile()
        former_tile.remove_hero(hero)
        hero.set_tile(tile)
        tile.add_hero(hero)
        self.load_action_options()

    def explore_tile(self, tile: Tile):
        hero: Hero = self.get_current_hero()
        if isinstance(tile,Unknown):
            tile_type = self._tilepack.pick()
            if tile_type is not None:
                self.spawn_tile(tile_type,tile,hero.get_tile())
            else:
                tile: Tile
                for k in list(self._tilemap.keys()):
                    if isinstance(self._tilemap[k],Unknown):
                        self.destroy_tile(self._tilemap[k])
        else:
            pass
        
    def spawn_tile(self, tile_type: Tile, parent: Tile, start: Tile):
        c,r = parent.get_c(),parent.get_r()
        att_point,att_point_parent = parent.get_attached_point(),parent.get_attached_point_parent()
        new_parent = parent.get_attached_parent()
        self.destroy_tile(parent)

        tile: Tile = self.create_tile(tile_type,new_parent,att_point,att_point_parent,c,r)

        tile.register_mouse_event(MouseEvent.WHEELUP,self.rotate_tile_up,tile,start)
        tile.register_mouse_event(MouseEvent.WHEELDOWN,self.rotate_tile_down,tile,start)

        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_up(tile,start)

    def get_current_hero(self) -> Hero:
        return GAME.players.get(self._player_i).get_hero()
    
    def rotate_tile_up(self, tile: Tile, start: Tile):
        tile.rotate_up()
        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_up(tile,start)

    def rotate_tile_down(self, tile: Tile, start: Tile):
        tile.rotate_down()
        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_down(tile,start)
        
    def place_tile(self, tile: Tile):
        c,r = tile.get_c(),tile.get_r()

        if (str(c) + str(r-1)) not in self._tilemap and not isinstance(tile,Unknown) and tile.is_passable_top():
            self.create_tile(Unknown,tile,FRAMEPOINT.BOTTOM,FRAMEPOINT.TOP,c,r-1)
        if (str(c+1) + str(r)) not in self._tilemap and not isinstance(tile,Unknown) and tile.is_passable_right():
            self.create_tile(Unknown,tile,FRAMEPOINT.LEFT,FRAMEPOINT.RIGHT,c+1,r)
        if (str(c) + str(r+1)) not in self._tilemap and not isinstance(tile,Unknown) and tile.is_passable_bottom():
            self.create_tile(Unknown,tile,FRAMEPOINT.TOP,FRAMEPOINT.BOTTOM,c,r+1)
        if (str(c-1) + str(r)) not in self._tilemap and not isinstance(tile,Unknown) and tile.is_passable_left():
            self.create_tile(Unknown,tile,FRAMEPOINT.RIGHT,FRAMEPOINT.LEFT,c-1,r)

        tile.clear_mouse_event(MouseEvent.WHEELUP)
        tile.clear_mouse_event(MouseEvent.WHEELDOWN)
        tile.register_mouse_event(MouseEvent.LEFTCLICK,self.move_to_tile,tile)
        tile.set_active(False)
        self.move_to_tile(tile)
        
    def create_tile(self, tile_type: Tile, parent: Tile, att_point: int, att_point_parent: int,c: int, r: int) -> Tile:
        tile:Tile = tile_type(self,c,r)
        tile.set_point(att_point=att_point,att_point_parent=att_point_parent,parent=parent)
        self._tilemap[str(c)+str(r)] = tile
        if issubclass(tile_type,Unknown):
            tile.register_mouse_event(MouseEvent.LEFTCLICK,self.explore_tile,tile)
        else:
            tile.register_mouse_event(MouseEvent.LEFTCLICK,self.place_tile,tile)
        return tile

    def player_turn_end(self):
        self._player_i += 1
        if self._player_i >= len(GAME.players.get_count()):
            self._player_i = 0

    def destroy_tile(self, tile: Tile):
        cr = str(tile.get_c()) + str(tile.get_r())
        del self._tilemap[cr]
        tile.destroy()

    def get_tilesize(self) -> int:
        return self._tilesize

    def _on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        x,y = 0,0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y += 10 + (10 * self._zoom)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y -= 10 + (10 * self._zoom)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x -= 10 + (10 * self._zoom)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x += 10 + (10 * self._zoom)
        if x != 0 or y != 0:
            self._start_tile.move(x,y)

    def _on_mouse_motion(self, x, y):
        if self._is_pressed:
            self._start_tile.move(x - self._motion_x,y - self._motion_y)
            self._motion_x = x
            self._motion_y = y

    def _on_mouse_left_press(self, x, y):
        self._motion_x = x
        self._motion_y = y
        self._is_pressed = True
    
    def _on_mouse_left_click(self, x, y):
        self._is_pressed = False

    def _on_mouse_wheel_down(self, x, y):
        w = self._start_tile.get_w() - 10
        h = self._start_tile.get_h() - 10
        if w >= self.get_h()*0.05:
            self._zoom -= 0.05
            tile: Tile
            for _,tile in self._tilemap.items():
                tile._resize(w,h)
            self._tilesize = h
            self.draw()
    
    def _on_mouse_wheel_up(self, x, y):
        w = self._start_tile.get_w() + 10
        h = self._start_tile.get_h() + 10
        if w <= self.get_h()*0.3:
            self._zoom += 0.05
            tile: Tile
            for _,tile in self._tilemap.items():
                tile._resize(w,h)
            self._tilesize = h
            self.draw()