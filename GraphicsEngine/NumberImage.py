import math
from numbers import Real

from GraphicsEngine.Frame import Frame
from GraphicsEngine.TextColors import TextColors
from core.MemoryEngine import MEMORY_ENGINE

FONT_PATH_REGULAR = '_Fonts\\BreatheFireIii-PKLOB.ttf'


class NumberImage(Frame):
    color: tuple
    value: int | float | str

    def __init__(self, w: int, h: int, value: int | float | str, color: tuple | str, parent: Frame) -> None:
        super().__init__(parent)
        self.set_w(w)
        self.set_h(h)
        self.value = value
        self.template = value if isinstance(value, str) and "{" in value else None
        self.template_values = {}
        self.color = TextColors.normalize(color)
        self.font_path = FONT_PATH_REGULAR
        self.refresh_surface()

    def set_value(self, value: int | float | str):
        if value != self.value:
            self.value = value
            self.template = value if isinstance(value, str) and "{" in value else None
            self.template_values.clear()
            self.refresh_surface()

    def set_values(self, **values):
        if values != self.template_values:
            self.template_values = values
            self.refresh_surface()

    def set_color(self, color: tuple | str):
        color = TextColors.normalize(color)
        if color != self.color:
            self.color = color
            self.refresh_surface()

    def change(self, color: tuple | str, value: int | float | str):
        color = TextColors.normalize(color)
        if color != self.color or value != self.value:
            self.color = color
            self.value = value
            self.template = value if isinstance(value, str) and "{" in value else None
            self.template_values.clear()
            self.refresh_surface()

    def resize(self, factor: float):
        super().resize(factor)
        self.refresh_surface()

    def set_size(self, w: int, h: int):
        super().set_size(w, h)
        self.refresh_surface()

    def refresh_surface(self):
        text = self._get_text()
        self.surface = MEMORY_ENGINE.get_fitted_txt_buffer().get(
            font_color=self.color,
            text=text,
            font_path=self.font_path,
            angle=self.angle,
            w=self.w,
            h=self.h,
            alpha=self.alpha,
        )

    def rotate(self, angle: int):
        super().rotate(angle)
        self.refresh_surface()

    def _get_text(self) -> str:
        if self.template is None:
            return self._format_value(self.value)

        try:
            values = {key: self._format_value(value) for key, value in self.template_values.items()}
            return self.template.format(**values)
        except KeyError:
            return self.template

    def _format_value(self, value) -> str:
        if isinstance(value, Real) and not isinstance(value, bool):
            rounded = self._round_half_up(value, 1)
            if float(rounded).is_integer():
                return str(int(rounded))
            return f"{rounded:.1f}"
        return str(value)

    def _round_half_up(self, value: Real, decimals: int) -> float:
        multiplier = 10 ** decimals
        if value >= 0:
            return math.floor(value * multiplier + 0.5) / multiplier
        return math.ceil(value * multiplier - 0.5) / multiplier
