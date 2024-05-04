from GraphicComponents.HeroPortrait import HeroPortrait,Frame,FRAMEPOINT
from UserInterface.InventoryPanel import InventoryPanel

from Game import GAME

class HeroPanel():
    portrait: HeroPortrait
    inventory_panel: InventoryPanel

    def __init__(self, screen: Frame) -> None:
        height = screen.get_h() * 0.35
        self.portrait = HeroPortrait(height * 0.72, height,screen)
        self.portrait.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT)

        self.inventory_panel = InventoryPanel(self.portrait,FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT)
        
    def update(self):
        hero = GAME.get_current_hero()
        self.portrait.set_texture(hero.get_definition().portrait_path)
        self.portrait.set_move_values(hero.get_move_points(),hero.get_max_move_points())
        self.portrait.set_hp_values(hero.get_hit_points(),hero.get_max_hit_points())

        self.inventory_panel.update(hero)