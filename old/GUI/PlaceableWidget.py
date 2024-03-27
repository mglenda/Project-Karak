from GUI.Frame import Frame
from GUI.GraphicComponents import Image,TextField,FRAMEPOINT,FONT_PATH_NUMBERS
from GameLogic.Placeable import Placeable
from GameLogic.Minion import Minion
from GameLogic.Items import Item

class PlaceableWidget(Image):
    _power_wheel: Image
    _power_text: TextField
    def __init__(self, w: int, h: int, path: str, parent: Frame) -> None:
        super().__init__(w, h, path, parent)

        self._power_wheel = Image(w=w*0.4,h=h*0.4,path='_Textures\\PowerWheel.png',parent=self)
        self._power_wheel.set_point(FRAMEPOINT.BOTTOMRIGHT,FRAMEPOINT.BOTTOMRIGHT,x_offset=-w*0.053,y_offset=-h*0.053)

        self._power_text = TextField(parent=self._power_wheel,font_size=30,text='10',font_path=FONT_PATH_NUMBERS)
        self._power_text.set_point(FRAMEPOINT.CENTER,FRAMEPOINT.CENTER)

        self._power_text.resize(w*0.3,h*0.3)

    def load_placeable(self, placeable: Placeable):
        if isinstance(placeable,Minion):
            self._load_minion(placeable)
        elif isinstance(placeable,Item):
            self._load_item(placeable)

    def _load_minion(self, minion: Minion):
        self.set_texture(minion.get_path())
        if minion.is_aggresive():
            self._power_text.set_text(str(minion.get_power()))
            self._power_wheel.set_visible(True)
        else:
            self._power_wheel.set_visible(False)

    def _load_item(self, item: Item):
        self.set_texture(item.get_icon())

        pv = item.get_power_wheel_value()
        if pv is not None:
            self._power_wheel.set_visible(True)
            self._power_text.set_text(pv)
        else:
            self._power_wheel.set_visible(False)