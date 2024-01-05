import GUI.Graphics as G

PATH = 'Textures\\Buttons\\'

BUTTON_CLASSIC_GREEN = {
    'img_name': 'ButtonGreen.png'
    ,'font_color': (18,115,0)
    ,'focus_layer': 'ButtonFocusLayer.png'
    ,'press_layer': 'ButtonPressLayer.png'
}
BUTTON_CLASSIC_RED = {
    'img_name': 'ButtonRed.png'
    ,'font_color': (160,0,0)
    ,'focus_layer': 'ButtonFocusLayer.png'
    ,'press_layer': 'ButtonPressLayer.png'
} 
BUTTON_CLASSIC_BLUE = {
    'img_name': 'ButtonBlue.png'
    ,'font_color': (0,111,164)
    ,'focus_layer': 'ButtonFocusLayer.png'
    ,'press_layer': 'ButtonPressLayer.png'
} 
BUTTON_CLASSIC_YELLOW = {
    'img_name': 'ButtonYellow.png'
    ,'font_color': (255,240,0)
    ,'focus_layer': 'ButtonFocusLayer.png'
    ,'press_layer': 'ButtonPressLayer.png'
} 
BUTTON_ARROWRIGHT_GREEN = {
    'img_name': 'ButtonArrowRight.png'
    ,'font_color': (0,140,0)
    ,'focus_layer': 'ButtonArrowRightFocusLayer.png'
    ,'press_layer': 'ButtonArrowRightPressLayer.png'
}
BUTTON_ARROWLEFT_GREEN = {
    'img_name': 'ButtonArrowLeft.png'
    ,'font_color': (0,140,0)
    ,'focus_layer': 'ButtonArrowLeftFocusLayer.png'
    ,'press_layer': 'ButtonArrowLeftPressLayer.png'
}


class Button(G.Panel):
    def __init__(self, w=0, h=0, button_style: dict = BUTTON_CLASSIC_GREEN,text: str = '',font_size: int = 15) -> None:
        img_path = PATH + button_style['img_name']
        super().__init__(w=w, h=h, img_path=img_path)
        self.focus_layer = G.Image(w,h,PATH + button_style['focus_layer'])
        self.add(self.focus_layer,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)
        self.focus_layer.set_visible(False)

        self.press_layer = G.Image(w,h,PATH + button_style['press_layer'])
        self.add(self.press_layer,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)
        self.press_layer.set_visible(False)

        self.text = G.TextField(button_style['font_color'],text=text,font_size=font_size)
        self.add(self.text,G.ATTPOINT_CENTER,G.ATTPOINT_CENTER)

    def _on_mouse_enter(self):
        super()._on_mouse_enter()
        self.focus_layer.set_visible(True)
    
    def _on_mouse_leave(self):
        super()._on_mouse_leave()
        self.focus_layer.set_visible(False)
        self.press_layer.set_visible(False)

    def _on_mouse_left_click(self, x, y):
        super()._on_mouse_left_click(x, y)
        self.focus_layer.set_visible(True)
        self.press_layer.set_visible(False)

    def _on_mouse_left_press(self, x, y):
        super()._on_mouse_left_press(x, y)
        self.focus_layer.set_visible(False)
        self.press_layer.set_visible(True)