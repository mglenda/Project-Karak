import GameLogic
import Screen
import Tiles
import pygame

class MainController():
    def __init__(self,game:GameLogic.Game):
        self.game = game

    def mouse_motion(self,screen:Screen.MainScreen,coords:tuple):
        x,y = coords[0],coords[1]
        # Mouse is in Castle Area
        if not self.game.is_mouse_motion_locked():
            if screen.get_castle().collides(x,y):
                screen.get_castle().mouse_motion(x,y)
                self.game.set_focused_layer(GameLogic.FOCUS_CASTLE_SCREEN)
            else:
                self.game.set_focused_layer(GameLogic.FOCUS_NONE)

    def mouse_left_click(self,screen:Screen.MainScreen):
        if self.game.get_focused_layer() == GameLogic.FOCUS_CASTLE_SCREEN:
            if self.game.get_state() == GameLogic.STATE_DEFAULT:
                t:Tiles.Tile = screen.get_castle().get_focused_tile()
                if t is not None and not t.is_revealed():
                    screen.get_castle().get_tilemap().tile_spawn(parent=t)
                    self.game.set_state(GameLogic.STATE_TILE_SPAWN)
                    # self.game.lock_mouse_motion()
            elif self.game.get_state() == GameLogic.STATE_TILE_SPAWN:
                screen.get_castle().get_tilemap().tile_spawn_confirm()
                self.game.set_state(GameLogic.STATE_DEFAULT)
                # self.game.unlock_mouse_motion()

    def mouse_wheel_up(self,screen:Screen.MainScreen):
        if self.game.get_focused_layer() == GameLogic.FOCUS_CASTLE_SCREEN:
            if self.game.get_state() == GameLogic.STATE_TILE_SPAWN:
                screen.get_castle().get_tilemap().get_spawned_tile().rotate_up()
            elif self.game.get_state() == GameLogic.STATE_DEFAULT:
                screen.get_castle().get_tilemap().resize(10,10)
                # pass

    def mouse_wheel_down(self,screen:Screen.MainScreen):
        if self.game.get_focused_layer() == GameLogic.FOCUS_CASTLE_SCREEN:
            if self.game.get_state() == GameLogic.STATE_TILE_SPAWN:
                screen.get_castle().get_tilemap().get_spawned_tile().rotate_down()
            elif self.game.get_state() == GameLogic.STATE_DEFAULT:
                screen.get_castle().get_tilemap().resize(-10,-10)
                # pass

    def keyboard_hold_handler(self,keys,screen:Screen.MainScreen):
        if keys[pygame.K_w]:
            screen.get_castle().get_tilemap().move(0,30 if keys[pygame.K_LSHIFT] else 15)
        if keys[pygame.K_a]:
            screen.get_castle().get_tilemap().move(30 if keys[pygame.K_LSHIFT] else 15,0)
        if keys[pygame.K_d]:
            screen.get_castle().get_tilemap().move(-30 if keys[pygame.K_LSHIFT] else -15,0)
        if keys[pygame.K_s]:
            screen.get_castle().get_tilemap().move(0,-30 if keys[pygame.K_LSHIFT] else -15)
