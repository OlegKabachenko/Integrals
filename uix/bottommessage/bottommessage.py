__all__ = "BottomMessage, BottomErrorMessage"

import os

from kivy.lang import Builder
from kivy.properties import StringProperty

from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandleButton, MDBottomSheetDragHandleTitle
from kivymd.uix.label import MDIcon

from config import Config

with open(
        os.path.join("uix", "bottommessage", "bottommessage.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class MessageIcon(MDIcon):
    def on_parent_size_change(self, size):
        root_width = size[0]
        root_height = size[1]

        if root_width >= root_height * Config.HEIGHT_ERR_MSG_MLT:
            self.font_size = root_height / Config.ERR_MSG_WIDE_DIV_ICON
        else:
            self.font_size = root_width / Config.ERR_MSG_NARROW_DIV_ICON


class BottomMessage(MDBottomSheet):
    bg_color = None
    icon = "information-outline"
    icon_color = None
    text_color = None
    close_icon_color = "gray"
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = " "
        self.bind(size=self.on_size_change)

    def on_size_change(self, *args):
        self.notify_children(self, self)

    def notify_children(self, parent, root):
        for child in parent.children:
            if hasattr(child, 'on_parent_size_change'):
                child.on_parent_size_change(root.size)

            self.notify_children(child, root)

    def set_msg_text(self, text):
        self.text = text

    def set_text_change_state(self, text=None):
        if text is None:
            text = self.text
        self.set_msg_text(text)
        self.set_state("toggle")


class ErrorText(MDBottomSheetDragHandleTitle):
    def calculate_font(self, parent_size):
        root_width = parent_size[0]
        root_height = parent_size[1]

        if root_width >= root_height*4:
            self.font_size = (root_width + root_height) / (len(self.text))
        else:
            self.font_size = (root_width + root_height + root_height) / (len(self.text) / 1.5)


class BottomErrorMessage(BottomMessage):
    bg_color = Config.ERROR_MSG_BG_COLOR
    icon = "alert-circle-outline"
    icon_color = "red"
    text_color = "red"
    close_icon_color = "red"
