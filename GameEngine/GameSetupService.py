from GameContext import GameContext
from GameEngine.MovementService import MovementService
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game


class GameSetupService:
    def __init__(self, context: GameContext, movement_service: MovementService, game: "Game") -> None:
        self.context = context
        self.movement_service = movement_service
        self.game = game

    def spawn_heroes(self):
        from GameEngine.HeroDefinition import Thief, Wizard, Warrior
        from GameEngine.Hero import Hero
        self.context.heroes = []
        self.context.heroes.append(Hero(Wizard, 'Marek', self.game))
        self.context.heroes.append(Hero(Thief, 'Katka', self.game))
        self.context.heroes.append(Hero(Warrior, 'Cico', self.game))

        from GameEngine.Item import Item
        from GameEngine.ItemDefinition import Axe, Sword, Key, FrostFist, HealingPortal, MagicBolt

        for h in self.context.heroes:
            h.move_to_tile(self.context.get_tilemap().tiles[0])
            h.refresh_move_points()

        self.context.heroes[0].inventory.add_item(Item(Axe))
        self.context.heroes[0].inventory.add_item(Item(FrostFist))
        self.context.heroes[0].inventory.add_item(Item(Key))
        self.context.heroes[0].inventory.add_item(Item(HealingPortal))
        self.context.heroes[0].inventory.add_item(Item(MagicBolt))
        self.context.heroes[0].inventory.add_item(Item(Sword))

        self.context.heroes[1].hit_points = 1

        # self.context.heroes[1].inventory.add_item(Item(Axe))
        # self.context.heroes[1].inventory.add_item(Item(Axe))

        # self.context.heroes[2].inventory.add_item(Item(Axe))
        # self.context.heroes[2].inventory.add_item(Item(Axe))

        self.movement_service.load_move_options()
