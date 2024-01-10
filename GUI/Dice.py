import pygame
from GUI.GraphicComponents import Image,Frame
from Game import GAME

DICE_ZERO = 0
DICE_ONE = 1
DICE_TWO = 2
DICE_THREE = 3
DICE_FOUR = 4
DICE_FIVE = 5
DICE_SIX = 6

PATH = '_Textures\\Dice\\'

class DiceImages():
    _images: list = []
    def _load():
        size = GAME.get_screen().get_h()*0.1
        DiceImages._images = []
        DiceImages._images.append(Image(size,size,PATH + 'Zero.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'One.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'Two.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'Three.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'Four.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'Five.png',GAME.get_screen()))
        DiceImages._images.append(Image(size,size,PATH + 'Six.png',GAME.get_screen()))

    def get(id: int) -> Image:
        if id >= 0 and id < len(DiceImages._images):
            return DiceImages._images[id]
        return None
        
class Dice(Frame):
    _type: int
    _stored: Image
    _parent: Frame
    def __init__(self,type: int) -> None:
        dice: Image = DiceImages.get(type)
        super().__init__(dice.get_parent())
        self._type = type
        self._stored = dice.get_surface()
        self.set_w(dice.get_w())
        self.set_h(dice.get_h())
        self.refresh()

    def refresh(self):
        self._surface = pygame.transform.smoothscale(self._stored,(self._w,self._h))
        if self._angle != 0:
            self._surface = pygame.transform.rotate(self._surface,self._angle)

    def rotate(self,angle: int):
        super().rotate(angle)
        self.refresh()

    def set_type(self,type: int) -> bool:
        if type != self._type:
            self._type = type
            self._stored = DiceImages.get(type).get_surface()
            self.refresh()
            return True
        return False
    
    def get_parent(self) -> Frame:
        return self._parent