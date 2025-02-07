__all__ = "BottomMessage, BottomErrorMessage"

import os

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandleButton, MDBottomSheetDragHandleTitle
from kivymd.uix.label import MDIcon
from config import Config
from tools.mixins import SizableFontMixin

with open(
        os.path.join("uix", "bottommessage", "bottommessage.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class MessageIcon(MDIcon, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(self.text, self,
             base_font_mlt_wide=Config.ERR_ICON_BASE_FONT_MLT_WIDE, base_font_mlt_narrow=Config.ERR_ICON_BASE_FONT_MLT_NARROW)))


class BottomMessage(MDBottomSheet):
    bg_color = StringProperty("white")
    icon = StringProperty("information-outline")
    icon_color = StringProperty("blue")
    text_color = StringProperty("black")
    close_icon_color = StringProperty("gray")
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = " "

    def set_msg_text(self, text):
        self.text = text

    def set_text_change_state(self, text=None):
        if text is None:
            text = self.text
        self.set_msg_text(text)
        self.set_state("toggle")


class CloseBtn(MDBottomSheetDragHandleButton, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(self.text, self,
             base_font_mlt_wide=Config.ERR_ICON_BASE_FONT_MLT_WIDE, base_font_mlt_narrow=Config.ERR_ICON_BASE_FONT_MLT_NARROW)))


class ErrorText(MDBottomSheetDragHandleTitle, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(text=lambda instance, value: setattr(self, 'font_size', self.calculate_font(self.text,
            self.parent, length_div=Config.ERR_TEXT_LENGTH_CORR_DIV, base_font_mlt_narrow=Config.ERR_BASE_FONT_MLT_NARROW)))

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(self.text,
            self.parent, length_div=Config.ERR_TEXT_LENGTH_CORR_DIV, base_font_mlt_narrow=Config.ERR_BASE_FONT_MLT_NARROW)))


class BottomErrorMessage(BottomMessage):
    bg_color = Config.ERROR_MSG_BG_COLOR
    icon = "alert-circle-outline"
    icon_color = "red"
    text_color = "red"
    close_icon_color = "red"
