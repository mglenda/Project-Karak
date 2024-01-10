from GUI.GraphicComponents import Image,Frame,TextField
import GUI._const_framepoints as FRAMEPOINT

PATH = '_Textures\\Buttons\\'

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

class Button(Image):
    _focus_layer: Image
    _press_layer: Image
    _text: TextField
    _button_style: dict
    def __init__(self, w: int, h: int, button_style: dict, parent: Frame , text: str = '', font_size: int = 15):
        self._button_style = button_style
        path = PATH + self._button_style['img_name']
        super().__init__(w, h, path, parent)

        self._focus_layer = Image(w,h,PATH + self._button_style['focus_layer'],self)
        self._focus_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._press_layer = Image(w,h,PATH + button_style['press_layer'],self)
        self._press_layer.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._text = TextField(self,self._button_style['font_color'],font_size,text)
        self._text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(False)
        self.set_active(True)

    def set_text(self, text: str):
        self._text.set_text(text)

    def set_style(self, button_style: dict) -> bool:
        if self._button_style != button_style:
            self._button_style = button_style
            self.set_texture(PATH + self._button_style['img_name'])
            self._focus_layer.set_texture(PATH + self._button_style['focus_layer'])
            self._press_layer.set_texture(PATH + self._button_style['press_layer'])
            self._text.set_color(button_style['font_color'])
            return True
        return False
    
    def set_active(self, active: bool):
        super().set_active(active)
        if active == False:
            self._focus_layer.set_visible(False)
            self._press_layer.set_visible(False)
    
    def _on_mouse_enter(self):
        self._focus_layer.set_visible(True)
        super()._on_mouse_enter()
    
    def _on_mouse_leave(self):
        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(False)
        super()._on_mouse_leave()

    def _on_mouse_left_click(self, x, y):
        self._focus_layer.set_visible(True)
        self._press_layer.set_visible(False)
        super()._on_mouse_left_click(x, y)

    def _on_mouse_left_press(self, x, y):
        self._focus_layer.set_visible(False)
        self._press_layer.set_visible(True)
        super()._on_mouse_left_press(x, y)