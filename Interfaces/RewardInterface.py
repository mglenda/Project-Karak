from Interfaces.Interface import Interface
from Interfaces.HeroInterface import HeroInterface
from Interfaces.ItemInterface import ItemInterface

class RewardInterface(Interface):
    hero: HeroInterface
    item: ItemInterface
    
    def get_hero(self):
        pass

    def get_item(self):
        pass