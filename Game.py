from GameEngine.DiceService import DiceService
from GameEngine.CombatService import CombatService
from GameEngine.MovementService import MovementService
from GameEngine.RewardService import RewardService
from GameEngine.GameSetupService import GameSetupService
from GameEngine.TurnService import TurnService
from GameEngine.TexturePreloadService import TexturePreloadService
from GraphicsEngine.LoadingScreen import LoadingScreen
from GameContext import GameContext
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from UI import UI

pygame.init()

class Game():
    def __init__(self) -> None:
        self.context = GameContext()
        self.dice_service = DiceService(self.context)
        self.combat_service = CombatService(self.context, self.dice_service)
        self.movement_service = MovementService(self.context)
        self.reward_service = RewardService(self.context)
        self.setup_service = GameSetupService(self.context, self.movement_service, self)
        self.turn_service = TurnService(self.context, self.movement_service)
        self.texture_preload_service = TexturePreloadService(self.context)

    def start(self):
        self.context.running = True

        from UI import UI
        self.context.ui = UI(self)
        # loading_screen = LoadingScreen(self.context.ui.screen)
        # loading_screen.draw(0, 1, "Setting up game")

        from GameEngine.MinionPack import MinionPack
        self.context.minion_pack = MinionPack()

        self.setup_service.spawn_heroes()
        # self.texture_preload_service.preload(loading_screen.draw)
        # loading_screen.draw(1, 1, "Starting game")

    def quit(self):
        self.context.running = False

    def is_running(self) -> bool:
        return self.context.running

    def update(self):
        for h in self.context.heroes:
            h.refresh_actions()

    def update_gui(self):
        self.context.ui.get_hero_panel().update()
        self.context.ui.get_combat_panel().update()
        self.context.ui.get_dice_panel().update()
        self.context.ui.get_action_panel().update()
        self.context.ui.get_reward_panel().update()
        self.context.ui.get_ranking_panel().update()

    def draw(self):
        self.context.ui.draw()

    def force_mouse_motion(self):
        self.context.ui.on_mouse_motion(self.context.ui.get_mouse_x(),self.context.ui.get_mouse_y())

GAME = Game()
