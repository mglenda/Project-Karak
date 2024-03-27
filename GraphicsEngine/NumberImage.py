from GraphicsEngine.Image import Image,Frame

PATH = '_Textures\\Numbers\\'

class NumberImage(Image):
    color: str
    value: int

    def __init__(self, w: int, h: int, value: int, color: str, parent: Frame) -> None:
        self.value = value
        self.color = color
        super().__init__(w, h, self.get_path(), parent)

    def get_path(self):
        return PATH + self.color + '\\' + str(self.value) + '.png'
    
    def set_value(self, value: int):
        if value != self.value:
            self.value = value
            self.set_texture(self.get_path())

    def set_color(self, color: str):
        if color != self.color:
            self.color = color
            self.set_texture(self.get_path())

    def change(self, color: str, value: int):
        if color != self.color or value != self.value:
            self.color = color
            self.value = value
            self.set_texture(self.get_path())