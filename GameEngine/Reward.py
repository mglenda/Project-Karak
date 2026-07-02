from Interfaces.RewardInterface import RewardInterface
from Interfaces.ItemInterface import ItemInterface
from Interfaces.HeroInterface import HeroInterface
from Interfaces.InventoryInterface import InventoryInterface

class Reward(RewardInterface):
    hero: HeroInterface
    item: ItemInterface

    def __init__(self, hero: HeroInterface, item: ItemInterface):
        self.hero = hero
        self.item = item
    
    def get_hero(self) -> HeroInterface:
        return self.hero
    
    def get_item(self) -> ItemInterface:
        return self.item