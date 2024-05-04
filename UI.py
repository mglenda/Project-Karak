from GraphicsEngine.Screen import Screen
from GraphicsEngine.MouseController import MouseController
from GraphicsEngine.World import World
from UserInterface.HeroPanel import HeroPanel

class UI(MouseController):
    screen: Screen
    world: World
    hero_panel: HeroPanel

    def __init__(self) -> None:
        super().__init__(Screen())
        self.world = World(self.screen)
        self.hero_panel = HeroPanel(self.screen)
        self.hero_panel.portrait.resize(0.8)

    def get_hero_panel(self) -> HeroPanel:
        return self.hero_panel

    def get_world(self) -> World:
        return self.world

    def draw(self):
        self.screen.draw()