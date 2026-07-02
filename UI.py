from GraphicsEngine.Screen import Screen
from GraphicsEngine.MouseController import MouseController
from GraphicsEngine.World import World
from GraphicComponents.DisableScreen import DisableScreen
from UserInterface.HeroPanel import HeroPanel
from UserInterface.CombatPanel import CombatPanel
from UserInterface.ActionPanel import ActionPanel
from UserInterface.DicePanel import DicePanel
from UserInterface.RewardPanel import RewardPanel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class UI(MouseController):
    screen: Screen
    world: World
    hero_panel: HeroPanel
    combat_panel: CombatPanel
    disable_screen: DisableScreen
    action_panel: ActionPanel
    dice_panel: DicePanel
    reward_panel: RewardPanel

    def __init__(self, game: "Game") -> None:
        super().__init__(Screen())
        self.world = World(self.screen, game)
        self.hero_panel = HeroPanel(self.screen, game)
        self.hero_panel.portrait.resize(0.8)

        self.disable_screen = DisableScreen(self.screen)

        self.combat_panel = CombatPanel(self.screen, game)

        self.dice_panel = DicePanel(self.screen, game)

        self.reward_panel = RewardPanel(self.screen, game)

        self.action_panel = ActionPanel(self.screen, game)

    def get_hero_panel(self) -> HeroPanel:
        return self.hero_panel
    
    def get_combat_panel(self) -> CombatPanel:
        return self.combat_panel

    def get_world(self) -> World:
        return self.world
    
    def get_action_panel(self) -> ActionPanel:
        return self.action_panel
    
    def get_dice_panel(self) -> DicePanel:
        return self.dice_panel
    
    def get_reward_panel(self) -> RewardPanel:
        return self.reward_panel

    def draw(self):
        if self.combat_panel.is_visible() or self.reward_panel.is_visible():
            self.disable_screen.set_visible(True)
        else:
            self.disable_screen.set_visible(False)
        self.screen.draw()
