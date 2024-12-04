from Interfaces.TileObjectInterface import TileObjectInterface
from Interfaces.HeroInterface import HeroInterface
from GameEngine.MinionDefinition import MinionDefinition
from Interfaces.MinionInterface import MinionInterface
import pygame

pygame.init()

class Game():
    def __init__(self) -> None:
        pass

    def get_tilemap(self):
        return self.ui.get_world().get_tilemap()

    def start(self):
        from UI import UI
        self.ui = UI()

        from GameEngine.MinionPack import MinionPack
        self.minion_pack = MinionPack()

        self.spawn_heroes()

    def spawn_heroes(self):
        from GameEngine.HeroDefinition import LordOfKarak,Thief,Barbarian,BeastHunter,Wizard
        from GameEngine.Hero import Hero
        self.heroes: list[Hero] = []
        self.heroes.append(Hero(Wizard,'Marek'))
        self.heroes.append(Hero(BeastHunter,'Katka'))

        from GameEngine.Item import Item
        from GameEngine.ItemDefinition import Axe,Sword,Key,FrostFist,HealingPortal,MagicBolt

        for h in self.heroes:
            h.move_to_tile(self.get_tilemap().tiles[0])
            h.refresh_move_points()

        #self.heroes[0].inventory.add_item(Item(Axe))
        #self.heroes[0].inventory.add_item(Item(FrostFist))
        #self.heroes[0].inventory.add_item(Item(Key))
        #self.heroes[0].inventory.add_item(Item(HealingPortal))
        #self.heroes[0].inventory.add_item(Item(MagicBolt))
        #self.heroes[0].inventory.add_item(Item(Sword))

        self.load_actions()

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
        tile.add_placeable(Minion(definition))

    def get_current_hero(self):
        return self.heroes[0]
    
    def confirm_tile_placement(self, tile: TileObjectInterface):
        tile.on_click(self.move_to_tile,tile)
        if tile.is_spawn:
            self.choose_minion(tile)
        else:
            self.move_to_tile(tile)
    
    def move_to_tile(self, tile: TileObjectInterface):
        self.get_current_hero().move_to_tile(tile)
        self.load_actions()

    def load_actions(self):
        hero = self.get_current_hero()
        tile = hero.get_tile()
        placeable = tile.get_placeable()

        if isinstance(placeable,MinionInterface) and placeable.agressive:
            #self.ui.get_combat_panel().show()
            print(placeable.get_path())

        if hero.get_move_points() <= 0:
            self.end_turn()
        else:
            tile = hero.get_tile()
            self.get_tilemap().load_path(tile,1)

    def end_turn(self):
        hero = self.get_current_hero()
        for i,h in enumerate(self.heroes):
            if i != 0:
                self.heroes[i-1] = h
        self.heroes[i] = hero
        
        self.refresh_hero(self.heroes[0])
        self.load_actions()

    def refresh_hero(self, hero: HeroInterface):
        hero.refresh_move_points()

    def update(self):
        self.ui.get_hero_panel().update()
        self.ui.get_combat_panel().update()

    def draw(self):
        self.ui.draw()

GAME = Game()