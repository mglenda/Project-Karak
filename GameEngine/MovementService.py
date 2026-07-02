from GameContext import GameContext
from GameEngine.Constants import DurationScopes
from GameEngine.MinionDefinition import MinionDefinition
from Interfaces.MinionInterface import MinionInterface
from Interfaces.TileObjectInterface import TileObjectInterface
import GameEngine.Buff as buff
import GameEngine.BuffModifier as bMod


class MovementService:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def choose_minion(self, tile: TileObjectInterface):
        arr = self.context.minion_pack.pick()
        if len(arr) == 0:
            self.move_to_tile(tile)
        else:
            if len(arr) == 1:
                self.spawn_minion(arr[0], tile)
                self.move_to_tile(tile)
            else:
                pass

    def spawn_minion(self, definition: MinionDefinition, tile: TileObjectInterface):
        from GameEngine.Minion import Minion
        Minion(definition).set_tile(tile)

    def confirm_tile_placement(self, tile: TileObjectInterface):
        self.context.get_current_hero().remove_buffs(buff.ChoosingTile)
        tile.on_click(self.move_to_tile, tile)
        if tile.is_spawn:
            self.choose_minion(tile)
        else:
            self.move_to_tile(tile)

    def move_to_tile(self, tile: TileObjectInterface):
        hero = self.context.get_current_hero()
        hero.move_to_tile(tile)
        hero.reset_cooldowns(DurationScopes.DURATION_SCOPE_TILEMOVE)
        hero.remove_buffs(DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.load_move_options()

    def load_move_options(self):
        hero = self.context.get_current_hero()
        tile = hero.get_tile()
        placeable = tile.get_placeable()

        if not(isinstance(placeable, MinionInterface) and placeable.agressive) or hero.has_modifier(bMod.IgnoreHostiles):
            if hero.get_move_points() > 0 and not hero.has_modifier(bMod.CannotMove):
                tile = hero.get_tile()
                self.context.get_tilemap().load_path(tile, 1)
            else:
                self.context.get_tilemap().disable_all_tiles()
        else:
            self.context.get_tilemap().disable_all_tiles()
