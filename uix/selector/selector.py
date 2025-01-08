__all__ = "EMSelector"

import os
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFabButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.clock import Clock

import math

from config import Config

with open(
        os.path.join("uix", "selector", "selector.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class EMSelector(MDBoxLayout):
    items_list = ListProperty()
    default_element_id = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.register_event_type('on_select')
        Clock.schedule_once(lambda dt: self.init_label(self.default_element_id))  #draw default text

    def init_label(self, default_id):
        self.ids.button.menu_callback(default_id, default_id + 1, self.ids.field, self.items_list[default_id], True)

    def event_dispatch(self, s_id, prev_id):
        event = 'on_select'
        self.dispatch(event, s_id, prev_id)

    def on_select(self, s_id, prev_id):
        pass


class SelectButton(MDFabButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    @staticmethod
    def calculate_menu_item_font(menu_width):

        root_w = Window.width
        root_h = Window.height
        if root_w > root_h:
            font_size = str(menu_width / (Config.MENU_ITEM_WIDE_FNT_MULT * root_w / root_h)) + "sp"
        else:
            font_size = str(menu_width / (Config.MENU_ITEM_NARROW_FNT_MULT * root_w / root_h)) + "sp"
        return font_size

    def build_menu(self, item, text_field=None):
        menu_items = []
        root_w = Window.width
        prev_id = None

        menu_width = root_w / 1.5

        source_list = self.parent.items_list

        for i, entry in enumerate(source_list):
            text = entry
            font_size = self.calculate_menu_item_font(menu_width)
            background_color = MDApp.get_running_app().theme_cls.transparentColor
            text_color = MDApp.get_running_app().theme_cls.onSurfaceColor

            if text_field.text == text:
                prev_id = i

            menu_items.append(
                {
                    "viewclass": "MenuItem",
                    "text": text,
                    "font_size": font_size,

                    "background_color": background_color,
                    "color": text_color,
                    "text_size": [menu_width, None],

                    "on_release": lambda s_id=i, text_item=text: self.menu_callback(s_id, prev_id, text_field,
                                                                                    text_item),
                })

            menu_items.append(
                {
                    "viewclass": "MDDivider",
                    "height": 1,
                }
            )

        self.menu = MDDropdownMenu(caller=item, items=menu_items, width=menu_width)
        self.menu.open()

    def menu_callback(self, s_id, prev_id, text_field, text, is_initialization=False):
        if text_field is None:
            raise ValueError("text_field is None!")
        elif prev_id is None:
            raise ValueError("prev_id is None!")

        text_field.text = text

        if hasattr(self, 'menu'):
            if self.menu:
                self.menu.dismiss()

        if not is_initialization:
            self.parent.event_dispatch(s_id, prev_id)


class SFMArea(MDBoxLayout):
    pass


class SFMLabel(MDLabel):
    def calculate_font_size(self):
        font_corr_divider = Config.SFM_CORR_WIDE_DIVIDER

        screen_width = Window.width
        screen_height = Window.height

        if screen_width * Config.APP_WIDE_SCR_MULT > screen_height:  #for width/narrow screen, different formulas give good result
            base_font = self.parent.height * Config.SFM_WIDE_FNT_MULT
        else:
            base_font = self.parent.width * Config.SFM_NARROW_FNT_MULT
            font_corr_divider = Config.SFM_CORR_NARROW_DIVIDER

        font_corrector = len(
            self.text) / font_corr_divider  #this correction helps to display text of different sizes correctly.
        if font_corrector > base_font * Config.SFM_MAX_FONT_CORR:
            font_corrector = base_font * Config.SFM_MAX_FONT_CORR

        font = math.floor(base_font - font_corrector)

        if screen_width < Config.SFM_CRITICAL_WIDTH:
            font = font * Config.SFM_EXTRA_FNT_MULT

        self.font_size = font


class SFMScroll(MDScrollView):
    pass


class SFMAnchor(MDAnchorLayout):
    pass
