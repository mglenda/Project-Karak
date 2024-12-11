from GraphicsEngine.Rect import Rect,Frame
from GraphicsEngine.Image import Image
from GraphicsEngine.Constants import Framepoint as FRAMEPOINT
from GraphicComponents.DuelistScreen import DuelistScreen

class CombatButton(Image):
    normal_path: str = '_Textures\\Combat\\CombatNormal.png'
    focused_path: str = '_Textures\\Combat\\CombatFocused.png'
    pressed_path: str = '_Textures\\Combat\\CombatPushed.png'

    def __init__(self, w, h, parent):
        super().__init__(w, h, self.normal_path, parent)

    def on_mouse_enter(self):
        self.set_texture(self.focused_path)
        return super().on_mouse_enter()
    
    def on_mouse_leave(self):
        self.set_texture(self.normal_path)
        return super().on_mouse_leave()
    
    def on_mouse_left_press(self, x, y):
        self.set_texture(self.pressed_path)
        return super().on_mouse_left_press(x, y)
    
    def on_mouse_left_click(self, x, y):
        self.set_texture(self.focused_path)
        return super().on_mouse_left_click(x, y)

class CombatScreen(Rect):
    background:Rect
    duelist_screen:list[DuelistScreen]
    combat_button: CombatButton

    def __init__(self, w: int, h: int, parent: Frame) -> None:
        super().__init__(w, h, (255,255,255), parent)

        self.background = Rect(w-w*0.01,h-h*0.01,(0,0,0),self)
        self.background.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self.duelist_screen = [DuelistScreen(w*0.34,w*0.24,(30,30,30),self,0)
                               ,DuelistScreen(w*0.34,w*0.24,(120,120,120),self,1)]
        
        self.duelist_screen[0].set_point(FRAMEPOINT.TOPLEFT,FRAMEPOINT.TOPLEFT,w*0.08,h*0.1)
        self.duelist_screen[1].set_point(FRAMEPOINT.TOPRIGHT,FRAMEPOINT.TOPRIGHT,-w*0.08,h*0.1)

        self.combat_button = CombatButton(w*0.1,w*0.1,self)
        self.combat_button.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT,-w*0.02,-w*0.02)
        self.combat_button.set_active(True)


    def update(self,id: int, base_value: int = 0,dice_value: int = 0,ability_value: int = 0,scroll_value: int = 0,total_value: int = 0,portrait: str = None):
        self.duelist_screen[id].update(base_value,dice_value,ability_value,scroll_value,total_value,portrait)