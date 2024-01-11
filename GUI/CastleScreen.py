from GUI.GraphicComponents import Rect
from GUI.Frame import FRAMEPOINT
from GUI._ComponentListeners import KeyBoardListener
from GUI.Tile import Unknown,Start,Tile
import GUI._const_mouseevents as MouseEvent
from GUI.TilePack import TilePack
from GUI.MinionPack import MinionPack
from GUI.PlayerPanel import PlayerPanel
from GameLogic.DiceRoller import DiceRoller,DICE_NORMAL,DICE_WARLOCK
from GameLogic.Player import Player
from GameLogic.Hero import Hero
from GameLogic.Placeable import Placeable
import GameLogic.Items as Items
import GameLogic.Minion as Minions
from Game import GAME
import pygame

class CastleScreen(Rect,KeyBoardListener):
    _start_tile: Start
    _motion_x: int
    _motion_y: int
    _is_pressed: bool
    _zoom: float
    _player_order: list
    _cur_player: Player
    _tilemap: dict
    _tilepack: TilePack
    _minionpack: MinionPack
    _tilesize: int
    _dr: DiceRoller
    def __init__(self) -> None:
        super().__init__(GAME.screen.get_w(), GAME.screen.get_h(), (40,40,40), GAME.screen)
        self._tilesize = self.get_h() * 0.12
        self._tilepack = TilePack()
        self._minionpack = MinionPack()
        self._is_pressed = False
        self._zoom = 0.0
        self._player_order = []
        self.set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT)

        self._start_tile = Start(self)
        self._start_tile.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)
        self._tilemap = {"00": self._start_tile}

        self.set_active(True)

        p: Player
        for p in GAME.get_players().get_all():
            p.get_hero().set_tile(self._start_tile)
            self._player_order.append(p)
            p.get_hero().refresh_move_points()

        self._cur_player = self._player_order[0]

        self.place_tile(self._start_tile,False)
        self.load_action_options()

    def move_to_tile(self, tile: Tile):
        hero: Hero = self.get_current_hero()
        hero.move(tile)

        if hero.get_move_points() <= 0:
            self.player_turn_end()
        else:
            self.center_camera(self._cur_player)
            self.load_action_options()

    def load_action_options(self):
        hero: Hero = self.get_current_hero()

        if isinstance(hero.get_tile().get_placeable(),Minions.Minion) and hero.get_tile().get_placeable().is_aggresive():
            GAME.get_combat_screen().set_visible(True)

        else:
            tile: Tile
            for _,tile in self._tilemap.items():
                if self.are_tiles_accesible(hero.get_tile(),tile):
                    tile.set_active(True)
                else:
                    tile.set_active(False)

    def player_turn_end(self):
        p = self._player_order[0]
        self._player_order.remove(p)
        self._player_order.append(p)
        self._cur_player = self._player_order[0]
        self.get_current_hero().refresh_move_points()
        self.refresh_player_panels()
        self.load_action_options()
        self.center_camera(self._cur_player)

    def refresh_player_panels(self):
        p:PlayerPanel
        for i,p in enumerate(GAME.get_player_panels()):
            p.load_player(self._player_order[i])

    def dice_roll(self,*dices):
        self._dr = DiceRoller(*dices)
        GAME.register_timer(50,[
            (self._dr.roll,())
        ],15,10
        ,[
            (self.roll_end,())
        ])

    def roll_end(self):
        print(self._dr.roll())

    def disable_all_tiles(self):
        tile: Tile
        for _,tile in self._tilemap.items():
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
    
    def center_camera(self, player: Player):
        tile: Tile = player.get_hero().get_tile()
        x,y = tile.get_x(),tile.get_y()

        midx = GAME.get_screen().get_w() / 2
        midy = GAME.get_screen().get_h() / 2
        midx -= tile.get_w()/2
        midy -= tile.get_h()/2

        self._start_tile.move(midx - x,midy - y)

    def explore_tile(self, tile: Tile):
        hero: Hero = self.get_current_hero()
        if isinstance(tile,Unknown):
            tile_type = self._tilepack.pick()
            self.spawn_tile(tile_type,tile,hero.get_tile())
            if len(self._tilepack.pack) == 0:
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

        self.disable_all_tiles()

        tile: Tile = self.create_tile(tile_type,new_parent,att_point,att_point_parent,c,r)

        tile.register_mouse_event(MouseEvent.WHEELUP,self.rotate_tile_up,tile,start)
        tile.register_mouse_event(MouseEvent.WHEELDOWN,self.rotate_tile_down,tile,start)
        tile.set_active(True)

        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_up(tile,start)

    def get_current_hero(self) -> Hero:
        return self._cur_player.get_hero()
    
    def rotate_tile_up(self, tile: Tile, start: Tile):
        tile.rotate_up()
        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_up(tile,start)

    def rotate_tile_down(self, tile: Tile, start: Tile):
        tile.rotate_down()
        if not self.are_tiles_accesible(tile,start):
            self.rotate_tile_down(tile,start)
        
    def place_tile(self, tile: Tile, moving:bool = True):
        c,r = tile.get_c(),tile.get_r()

        if len(self._tilepack.pack) > 0:
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

        if tile.is_spawn() and not tile.is_placed():
            minion: Placeable = self._minionpack.pick()
            if minion is not None:
                tile.add_placeable(minion())

        tile.set_placed(True)
        if moving:
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

    def destroy_tile(self, tile: Tile):
        cr = str(tile.get_c()) + str(tile.get_r())
        del self._tilemap[cr]
        tile.destroy()

    def get_tilesize(self) -> int:
        return self._tilesize

    def _on_key_hold(self, keys: pygame.key.ScancodeWrapper, unicode: str):
        x,y = 0,0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            y += 25 + (10 * self._zoom)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            y -= 25 + (10 * self._zoom)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            x -= 25 + (10 * self._zoom)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            x += 25 + (10 * self._zoom)
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
        self.dice_roll(DICE_NORMAL,DICE_NORMAL,DICE_NORMAL,DICE_WARLOCK,DICE_WARLOCK)

    def _on_mouse_leave(self):
        self._is_pressed = False

    def _on_mouse_wheel_down(self, x, y):
        w = self._start_tile.get_w() - 10
        h = self._start_tile.get_h() - 10
        if w >= self.get_h()*0.08:
            self._zoom -= 0.1
            tile: Tile
            for _,tile in self._tilemap.items():
                tile.resize(w,h)
            self._tilesize = h
    
    def _on_mouse_wheel_up(self, x, y):
        w = self._start_tile.get_w() + 10
        h = self._start_tile.get_h() + 10
        if w <= self.get_h()*0.2:
            self._zoom += 0.1
            tile: Tile
            for _,tile in self._tilemap.items():
                tile.resize(w,h)
            self._tilesize = h