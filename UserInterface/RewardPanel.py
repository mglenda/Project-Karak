from GraphicComponents.RewardScreen import RewardScreen,Frame,FRAMEPOINT
from GraphicsEngine.ItemImage import ItemImage
from Interfaces.ItemInterface import ItemInterface
from GameEngine.Constants import ItemTypes
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game import Game

class RewardPanel():
    main: RewardScreen
    item_image: ItemImage

    def __init__(self,screen: Frame, game: "Game") -> None:
        self.reward_service = game.reward_service
        height: int = screen.get_h()
        self.main = RewardScreen(height,height,screen)
        self.main.set_point(FRAMEPOINT.BOTTOM,FRAMEPOINT.BOTTOM)
        self.main.set_visible(False)

        self.item_image = ItemImage(height*0.15,height*0.15,'_Textures\\Heroes\\Combat\\BeastHunter.png',self.main,'Red',0)
        self.item_image.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER,0,-height*0.2,self.main.background)

    def show(self):
        self.main.set_visible(True)

    def hide(self):
        self.main.set_visible(False)

    def is_visible(self)-> bool:
        return self.main.is_visible()

    def update(self):
        reward = self.reward_service.get_reward()
        if reward is not None:
            if not self.is_visible():
                self.show()

            item: ItemInterface = reward.get_item()
            if item is not None:
                color:str = 'Red' if item.type == ItemTypes.WEAPON else 'Gold'
                self.item_image.change(item.get_path(),color,item.get_power())

        else:
            if self.is_visible():
                self.hide()
