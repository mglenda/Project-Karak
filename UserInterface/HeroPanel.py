from GraphicComponents.HeroPortrait import HeroPortrait,Frame,FRAMEPOINT
from Interfaces.HeroInterface import HeroInterface

class HeroPanel():
    portrait: HeroPortrait
    hero: HeroInterface

    def __init__(self, screen: Frame) -> None:
        height = screen.get_h() * 0.35
        self.portrait = HeroPortrait(height * 0.72, height,(0,0,0),screen)
        self.portrait.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT)

    def set_hero(self, hero: HeroInterface):
        self.hero = hero
        self.portrait.set_texture(hero.get_definition().portrait_path)

    def update(self):
        self.portrait.set_move_values(self.hero.get_move_points(),self.hero.get_max_move_points())
        self.portrait.set_hp_values(self.hero.get_hit_points(),self.hero.get_max_hit_points())