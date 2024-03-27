from GUI.GraphicComponents import Image,Frame,FRAMEPOINT
import random

PATH = '_Textures\\Dice\\'

DICE_PATHS = [
    PATH + 'Zero.png'
    ,PATH + 'One.png'
    ,PATH + 'Two.png'
    ,PATH + 'Three.png'
    ,PATH + 'Four.png'
    ,PATH + 'Five.png'
    ,PATH + 'Six.png'
]

DICE_NORMAL = 0
DICE_WARLOCK = 1
DICE_SWORDMASTER = 2

DICE_TYPES = [
    (1,2,3,4,5,6) # NORMAL
    ,(0,1,2,3)    # WARLOCK
    ,(2,3,4,5,6)  # SWORDMASTER
]
        
class Dice(Image):
    _parent: Frame
    _active_layer: Image
    _focus_layer: Image

    value: int
    dice_type: int

    def __init__(self,w: int, h:int, parent: Frame, dice_type: int = DICE_NORMAL) -> None:
        super().__init__(w,h,DICE_PATHS[0],parent)  

        self._active_layer = Image(self.get_w(),self.get_h(),PATH + 'ActiveLayer.png',self)
        self._active_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._focus_layer = Image(self.get_w(),self.get_h(),PATH + 'FocusLayer.png',self)
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.set_active(False)

        self.value = 0
        self.dice_type = dice_type

    def set_active(self, active: bool):
        super().set_active(active)
        self._active_layer.set_visible(active)
        if not active:
            self._focus_layer.set_visible(False)

    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        super()._on_mouse_leave()

    def roll(self) -> int:
        n = random.choice(DICE_TYPES[self.dice_type])
        if n == self.value:
            n = self.roll()
        self.value = n
        self.set_texture(DICE_PATHS[n])
        return n