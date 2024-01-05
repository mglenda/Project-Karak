PATH = 'Textures\\Buttons\\'

class Image():
    def __init__(self) -> None:
        pass

class Button(Image):
    texture = 'Background.png'
    texture_focused = 'FocusedLayer.png'
    w = 50
    h = 50
    def __init__(self) -> None:
        super().__init__()


class ConfirmButton(Button):
    texture = 'Confirm.png'
    texture_focused = 'ConfirmFocused.png'
    def __init__(self) -> None:
        super().__init__()