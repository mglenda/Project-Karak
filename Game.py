from Services.DiceService import DiceService
from Services.CombatService import CombatService
from Services.MovementService import MovementService
from Services.RewardService import RewardService
from Services.GameSetupService import GameSetupService
from Services.TurnService import TurnService
from Services.TexturePreloadService import TexturePreloadService
from Services.HeroSelectionService import HeroSelectionService
from Services.LordOfKarakService import LordOfKarakService
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
        self.movement_service = MovementService(self.context, self.dice_service)
        self.hero_selection_service = HeroSelectionService(self.context, self.movement_service)
        self.reward_service = RewardService(self.context)
        self.combat_service = CombatService(self.context, self.dice_service, self.movement_service, self.hero_selection_service, self.reward_service)
        self.movement_service.set_arena_service(self.combat_service)
        self.lord_of_karak_service = LordOfKarakService(self.context)
        self.movement_service.set_lord_of_karak_service(self.lord_of_karak_service)
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
        self.movement_service.update()
        for h in self.context.heroes:
            h.refresh_actions()

    def update_gui(self):
        self.context.ui.get_hero_panel().update()
        self.context.ui.get_combat_panel().update()
        self.context.ui.get_dice_panel().update()
        self.context.ui.get_action_panel().update()
        self.context.ui.get_reward_panel().update()
        self.context.ui.get_turn_order_panel().update()
        self.context.ui.get_hero_selection_panel().update()
        self.context.ui.get_arena_loot_panel().update()
        self.context.ui.get_lord_of_karak_panel().update()

    def draw(self):
        self.context.ui.draw()

    def force_mouse_motion(self):
        self.context.ui.on_mouse_motion(self.context.ui.get_mouse_x(),self.context.ui.get_mouse_y())

GAME = Game()
