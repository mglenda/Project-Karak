from GraphicsEngine.Screen import Screen
from GraphicsEngine.MouseController import MouseController
from GraphicsEngine.World import World
from GraphicComponents.DisableScreen import DisableScreen
from UserInterface.HeroPanel import HeroPanel
from UserInterface.CombatPanel import CombatPanel
from UserInterface.ActionPanel import ActionPanel
from UserInterface.DicePanel import DicePanel
from UserInterface.RewardPanel import RewardPanel
from UserInterface.CursePanel import CursePanel
from UserInterface.TurnOrderPanel import TurnOrderPanel
from UserInterface.HeroSelectionPanel import HeroSelectionPanel
from UserInterface.ArenaLootPanel import ArenaLootPanel
from UserInterface.LordOfKarakPanel import LordOfKarakPanel
from UserInterface.EndGamePanel import EndGamePanel
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
    curse_panel: CursePanel
    turn_order_panel: TurnOrderPanel
    hero_selection_panel: HeroSelectionPanel
    arena_loot_panel: ArenaLootPanel
    lord_of_karak_panel: LordOfKarakPanel
    end_game_panel: EndGamePanel

    def __init__(self, game: "Game") -> None:
        super().__init__(Screen())
        self.world = World(self.screen, game)
        self.hero_panel = HeroPanel(self.screen, game)
        self.hero_panel.portrait.resize(0.8)

        self.disable_screen = DisableScreen(self.screen)

        self.turn_order_panel = TurnOrderPanel(self.screen, game)

        self.combat_panel = CombatPanel(self.screen, game)

        self.curse_panel = CursePanel(self.screen)

        self.dice_panel = DicePanel(self.screen, game)

        self.reward_panel = RewardPanel(self.screen, game)

        self.action_panel = ActionPanel(self.screen, game)

        self.hero_selection_panel = HeroSelectionPanel(self.screen, game)
        self.arena_loot_panel = ArenaLootPanel(self.screen, game)
        self.lord_of_karak_panel = LordOfKarakPanel(self.screen, game)
        self.end_game_panel = EndGamePanel(self.screen, game)

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

    def get_curse_panel(self) -> CursePanel:
        return self.curse_panel

    def get_turn_order_panel(self) -> TurnOrderPanel:
        return self.turn_order_panel

    def get_hero_selection_panel(self) -> HeroSelectionPanel:
        return self.hero_selection_panel

    def get_arena_loot_panel(self) -> ArenaLootPanel:
        return self.arena_loot_panel

    def get_lord_of_karak_panel(self) -> LordOfKarakPanel:
        return self.lord_of_karak_panel

    def get_end_game_panel(self) -> EndGamePanel:
        return self.end_game_panel

    def draw(self):
        if self.combat_panel.is_visible() or self.reward_panel.is_visible() or self.curse_panel.is_visible() or self.hero_selection_panel.is_visible() or self.arena_loot_panel.is_visible() or self.lord_of_karak_panel.is_visible() or self.end_game_panel.is_visible():
            self.disable_screen.set_visible(True)
        else:
            self.disable_screen.set_visible(False)
        self.screen.draw()
