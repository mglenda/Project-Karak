from Interfaces.LootInterface import LootInterface
from Interfaces.ItemInterface import ItemInterface
from Interfaces.HeroInterface import HeroInterface

class Loot(LootInterface):
    looting_hero: HeroInterface
    reward: ItemInterface
    robbed_hero: HeroInterface

    def __init__(self, looting_hero: HeroInterface, reward: ItemInterface = None, robbed_hero: HeroInterface = None):
        self.looting_hero = looting_hero
        self.reward = reward
        self.robbed_hero = robbed_hero

    def get_loosting_hero(self) -> HeroInterface:
        return self.looting_hero
    
    def get_robbed_hero(self) -> HeroInterface:
        return self.robbed_hero
    
    def get_reward(self) -> list[ItemInterface]:
        return self.reward