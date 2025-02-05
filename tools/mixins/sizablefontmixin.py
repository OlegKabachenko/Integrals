__all__ = "SizableFontMixin"

from kivy.core.window import Window
import math

from kivymd.uix.widget import MDWidget
from config import Config

class SizableFontMixin:
    @staticmethod
    def calculate_font(text: str, ref_widget: MDWidget, root: MDWidget = Window, length_div: float = Config.TEXT_LENGTH_CORR_DIV,
                       root_width_mlt: float = Config.APP_WIDE_SCR_MULT, base_font_mlt_wide: float = Config.BASE_FONT_MLT_WIDE,
                       base_font_mlt_narrow: float = Config.BASE_FONT_MLT_NARROW, use_txt_corr: bool = True):

        root_width = root.width
        root_height = root.height

        if root_width * root_width_mlt > root_height:
            base_font = ref_widget.height * base_font_mlt_wide
            font_corrector = len(text) / length_div
        else:
            base_font = ref_widget.width * base_font_mlt_narrow
            font_corrector = 0

        if use_txt_corr:
            font = math.floor(base_font - font_corrector)
        else:
            font = math.floor(base_font)

        return f"{font}sp"
