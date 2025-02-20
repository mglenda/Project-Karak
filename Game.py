from Interfaces.TileObjectInterface import TileObjectInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.MinionDefinition import MinionDefinition
from Interfaces.MinionInterface import MinionInterface
from Interfaces.PlaceableInterface import PlaceableInterface
from GameEngine.Combat import Combat
from GameEngine.Duelist import Duelist
from GameEngine.Constants import DurationScopes
import GameEngine.BuffModifier as bMod
import GameEngine.Buff as buff
from GameEngine.DiceManager import DiceManager
from GameEngine.DiceDefinition import DiceDefinition
import pygame

pygame.init()

class Game():
    def __init__(self) -> None:
        self.combat = None
        self.dice_manager = None

    def get_tilemap(self):
        return self.ui.get_world().get_tilemap()

    def start(self):
        from UI import UI
        self.ui = UI()

        from GameEngine.MinionPack import MinionPack
        self.minion_pack = MinionPack()

        self.spawn_heroes()

    def spawn_heroes(self):
        from GameEngine.HeroDefinition import LordOfKarak,Thief,Barbarian,BeastHunter,Wizard,Warrior
        from GameEngine.Hero import Hero
        self.heroes: list[Hero] = []
        self.heroes.append(Hero(Wizard,'Marek'))
        self.heroes.append(Hero(Thief,'Katka'))
        self.heroes.append(Hero(Warrior,'Cico'))

        from GameEngine.Item import Item
        from GameEngine.ItemDefinition import Axe,Sword,Key,FrostFist,HealingPortal,MagicBolt

        for h in self.heroes:
            h.move_to_tile(self.get_tilemap().tiles[0])
            h.refresh_move_points()

        self.heroes[0].inventory.add_item(Item(Axe))
        self.heroes[0].inventory.add_item(Item(FrostFist))
        self.heroes[0].inventory.add_item(Item(Key))
        self.heroes[0].inventory.add_item(Item(HealingPortal))
        self.heroes[0].inventory.add_item(Item(MagicBolt))
        self.heroes[0].inventory.add_item(Item(Sword))

        self.heroes[1].hit_points = 1

        # self.heroes[1].inventory.add_item(Item(Axe))
        # self.heroes[1].inventory.add_item(Item(Axe))

        # self.heroes[2].inventory.add_item(Item(Axe))
        # self.heroes[2].inventory.add_item(Item(Axe))

        self.load_move_options()

    def choose_minion(self, tile: TileObjectInterface):
        arr = self.minion_pack.pick()
        if len(arr) == 0:
            self.move_to_tile(tile)
        else:
            if len(arr) == 1:
                self.spawn_minion(arr[0],tile)
                self.move_to_tile(tile)
            else:
                pass

    def spawn_minion(self, definition: MinionDefinition, tile: TileObjectInterface):
        from GameEngine.Minion import Minion
        Minion(definition).set_tile(tile)

    def get_current_hero(self):
        return self.heroes[0]
    
    def get_current_hero_active(self) -> HeroInterface:
        if self.combat is not None and self.combat.is_arena_duel():
            return self.combat.get_active_duelist()
        else:
            return self.get_current_hero()

    def confirm_tile_placement(self, tile: TileObjectInterface):
        tile.on_click(self.move_to_tile,tile)
        if tile.is_spawn:
            self.choose_minion(tile)
        else:
            self.move_to_tile(tile)

        self.get_current_hero().remove_buffs(buff.CannotEndTurn)
    
    def move_to_tile(self, tile: TileObjectInterface):
        self.get_current_hero().move_to_tile(tile)
        self.get_current_hero().reset_cooldowns(DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.get_current_hero().remove_buffs(DurationScopes.DURATION_SCOPE_TILEMOVE)
        self.load_move_options()

    def load_move_options(self):
        hero = self.get_current_hero()
        tile = hero.get_tile()
        placeable = tile.get_placeable()

        if not(isinstance(placeable,MinionInterface) and placeable.agressive) or hero.has_modifier(bMod.IgnoreHostiles):
            if hero.get_move_points() > 0 and not hero.has_modifier(bMod.CannotMove):
                tile = hero.get_tile()
                self.get_tilemap().load_path(tile,1)
            else:
                self.get_tilemap().disable_all_tiles()
        else:
            self.get_tilemap().disable_all_tiles()

    def start_combat(self):
        attacker: Duelist = self.get_current_hero()
        defender: Duelist = attacker.get_tile().get_placeable()
        self.combat = Combat(attacker,defender)
        self.create_dice_manager(self.get_current_hero().get_dices())

    def end_combat(self):
        h = self.combat.get_active_duelist()
        if isinstance(h,HeroInterface):
            h.reset_cooldowns(DurationScopes.DURATION_SCOPE_COMBAT)
            h.remove_buffs(DurationScopes.DURATION_SCOPE_COMBAT)

        if self.combat is not None:
            if self.combat.is_finished():
                if self.combat.is_draw():
                    if not self.combat.is_arena_duel():
                        self.get_current_hero().move_to_former_tile()
                else:
                    loser = self.combat.get_loser()
                    winner = self.combat.get_winner()
                    if not self.combat.is_arena_duel():
                        if loser == self.get_current_hero():
                            self.get_current_hero().hurt()
                            self.get_current_hero().move_to_former_tile()
                        elif isinstance(loser,PlaceableInterface):
                            loser.remove()
                self.clear_dice_manager()
                self.combat.end()
                self.combat = None
            else:
                self.combat.active_next()
                self.create_dice_manager(self.get_current_hero_active().get_dices())

    def get_combat(self):
        return self.combat

    def end_turn(self):
        hero = self.get_current_hero()

        for h in self.heroes:
            if h.has_buff(buff.Unconsciousness):
                h.remove_buffs(buff.Unconsciousness)
                h.add_buff(buff.Injured)

        for i,h in enumerate(self.heroes):
            if i != 0:
                self.heroes[i-1] = h
        self.heroes[i] = hero
        
        self.refresh_hero(self.heroes[0])
        self.load_move_options()

    def refresh_hero(self, hero: HeroInterface):
        hero.refresh_move_points()
        hero.reset_cooldowns(DurationScopes.DURATION_SCOPE_TURN)
        hero.remove_buffs(DurationScopes.DURATION_SCOPE_TURN)

    def update(self):
        self.ui.get_hero_panel().update()
        self.ui.get_combat_panel().update()
        self.ui.get_dice_panel().update()
        self.ui.get_action_panel().update()

    def draw(self):
        self.ui.draw()

    def force_mouse_motion(self):
        self.ui.on_mouse_motion(self.ui.get_mouse_x(),self.ui.get_mouse_y())

    def create_dice_manager(self, dice_types: list[DiceDefinition]):
        self.dice_manager = DiceManager(dice_types)

    def get_dice_manager(self) -> DiceManager:
        return self.dice_manager
    
    def clear_dice_manager(self):
        self.dice_manager = None

GAME = Game()