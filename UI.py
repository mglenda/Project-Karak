from GraphicsEngine.Screen import Screen
from GraphicsEngine.MouseController import MouseController
from GraphicsEngine.World import World
from GraphicComponents.DisableScreen import DisableScreen
from UserInterface.HeroPanel import HeroPanel
from UserInterface.CombatPanel import CombatPanel
from UserInterface.ActionPanel import ActionPanel

class UI(MouseController):
    screen: Screen
    world: World
    hero_panel: HeroPanel
    combat_panel: CombatPanel
    disable_screen: DisableScreen
    action_panel: ActionPanel

    def __init__(self) -> None:
        super().__init__(Screen())
        self.world = World(self.screen)
        self.hero_panel = HeroPanel(self.screen)
        self.hero_panel.portrait.resize(0.8)

        self.disable_screen = DisableScreen(self.screen)

        self.combat_panel = CombatPanel(self.screen)

        self.action_panel = ActionPanel(self.screen)

    def get_hero_panel(self) -> HeroPanel:
        return self.hero_panel
    
    def get_combat_panel(self) -> CombatPanel:
        return self.combat_panel

    def get_world(self) -> World:
        return self.world
    
    def get_action_panel(self) -> ActionPanel:
        return self.action_panel

    def draw(self):
        if (self.combat_panel.is_visible()):
            self.disable_screen.set_visible(True)
        else:
            self.disable_screen.set_visible(False)
        self.screen.draw()