from GameContext import GameContext
from GameEngine.Reward import Reward
from Interfaces.HeroInterface import HeroInterface
from Interfaces.ItemInterface import ItemInterface


class RewardService:
    def __init__(self, context: GameContext) -> None:
        self.context = context

    def get_reward(self) -> Reward:
        return self.context.reward

    def create_reward(self, item: ItemInterface, hero: HeroInterface):
        self.context.reward = Reward(item, hero)

    def clear_reward(self):
        self.context.reward = None
