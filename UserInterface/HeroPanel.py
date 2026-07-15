from GraphicComponents.HeroPortrait import HeroPortrait,Frame,FRAMEPOINT
from UserInterface.InventoryPanel import InventoryPanel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class HeroPanel():
    portrait: HeroPortrait
    inventory_panel: InventoryPanel

    def __init__(self, screen: Frame, game: "Game") -> None:
        self.context = game.context
        height = screen.get_h() * 0.35
        self.portrait = HeroPortrait(height * 0.72, height,screen)
        self.portrait.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT)

        self.inventory_panel = InventoryPanel(self.portrait,FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMLEFT)
        
    def update(self):
        hero = self.context.get_current_hero()
        self.portrait.set_texture(hero.get_definition().portrait_path)
        self.portrait.set_move_values(hero.get_move_points(),hero.get_max_move_points())
        self.portrait.set_hp_values(hero.get_hit_points(),hero.get_max_hit_points())
        self.portrait.set_cursed(hero.is_cursed())

        self.inventory_panel.update(hero)
