__all__ = " ControlBox, SelectorBox, CalculateBox"

import os

import yaml
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFabButton
from kivymd.uix.label import MDLabel
from kivy.uix.button import Button
from kivy.lang import Builder
from kivymd.uix.widget import MDWidget

from uix.mixins import SizableFontMixin

from kivy.core.window import Window
from kivy.properties import ListProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock


with open('uix/uix_config.yaml', 'r') as file, \
     open(os.path.join("uix", "controlbox", "controlbox.kv"), encoding="utf-8") as kv_file:
    config = yaml.safe_load(file)
    Builder.load_string(kv_file.read())


class MenuItem(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding_x = "10sp"
        self.halign = "left"


class ControlButton(MDFabButton, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(
            self.text, self, root=self, root_width_mlt=config['CTRL_BTN_ROOT_WIDTH_MLT'],
            base_font_mlt_wide=config['CTRL_BTN_BASE_FONT_MLT'], base_font_mlt_narrow=config['CTRL_BTN_BASE_FONT_MLT'])))


class LabelArea(MDBoxLayout):
    pass


class ControlLabel(MDLabel, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(
            self.text, self.parent, base_font_mlt_wide=config['CTRL_LBL_BASE_FONT_MLT_WIDE'],
            base_font_mlt_narrow=config['CTRL_LBL_BASE_FONT_MLT_NARROW'])))
        self.bind(text=lambda instance, value: setattr(self, 'font_size', self.calculate_font(
            self.text, self.parent, base_font_mlt_wide=config['CTRL_LBL_BASE_FONT_MLT_WIDE'],
            base_font_mlt_narrow=config['CTRL_LBL_BASE_FONT_MLT_NARROW'])))


class ControlBox(MDBoxLayout):
    button_type = ObjectProperty(ControlButton)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_btn_click')

        self.button = self.button_type()
        self.ids["button"] = self.button
        self.add_widget(self.button)
        self.create_label_area()

    def create_label_area(self):
        lbl_area = LabelArea()
        self.ids["area"] = lbl_area

        lbl = ControlLabel()

        self.ids["label"] = lbl
        lbl_area.add_widget(lbl)
        self.add_widget(lbl_area)

    def dispatch_btn_click(self):
        event = 'on_btn_click'
        self.dispatch(event)

    def on_btn_click(self):
        pass

    def set_label_text(self, new_text):
        self.ids.label.text = new_text

    def get_label_text(self):
        return self.ids.label.text


class SelectButton(ControlButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu = None

    def build_menu(self, item):
        menu_items = []
        root_w = Window.width

        menu_width = min(root_w / config['DROP_MENU_WIDTH_DIV'], config['DROP_MENU_MAX_WIDTH'])

        source_list = self.parent.items_list

        for i, entry in enumerate(source_list):
            text = entry

            mock_widget = MDWidget()  # Create a mock widget since the mixin requires an MDWidget instance
            mock_widget.width = mock_widget.height = menu_width

            font_size = self.calculate_font(
                self.text, mock_widget, length_div=config['DROP_MENU_TEXT_LENGTH_CORR_DIV'],
                base_font_mlt_wide=config['DROP_MENU_BASE_FONT_MLT_WIDE'],
                base_font_mlt_narrow=config['DROP_MENU_BASE_FONT_MLT_NARROW'])

            background_color = MDApp.get_running_app().theme_cls.transparentColor
            text_color = MDApp.get_running_app().theme_cls.onSurfaceColor

            if self.parent.get_label_text() == text:
                prev_id = i

            menu_items.append(
                {
                    "viewclass": "MenuItem",
                    "text": text,
                    "font_size": font_size,

                    "background_color": background_color,
                    "color": text_color,
                    "text_size": [menu_width, None],

                    "on_release": lambda s_id=i, text_item=text: self.menu_callback(s_id, prev_id, text_item),
                })

            menu_items.append(
                {
                    "viewclass": "MDDivider",
                    "height": 1,
                }
            )

        self.menu = MDDropdownMenu(caller=item, items=menu_items, width=menu_width)
        self.menu.open()

    def menu_callback(self, s_id, prev_id, text, is_initialization=False):
        if prev_id is None:
            raise ValueError("prev_id is None!")

        self.parent.set_label_text(text)

        if hasattr(self, 'menu'):
            if self.menu:
                self.menu.dismiss()

        if not is_initialization:
            self.parent.event_dispatch(s_id, prev_id)


class SelectorBox(ControlBox):
    items_list = ListProperty()
    default_element_id = NumericProperty(0)

    button_type = SelectButton

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_select')
        Clock.schedule_once(lambda dt: self.init_label(self.default_element_id))  #draw default text

    def init_label(self, default_id):
        self.ids.button.menu_callback(default_id, default_id + 1, self.items_list[default_id], True)

    def event_dispatch(self, s_id, prev_id):
        event = 'on_select'
        self.dispatch(event, s_id, prev_id)

    def on_select(self, s_id, prev_id):
        pass


class CalculateButton(ControlButton):
    pass


class CalculateBox(ControlBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clear_widgets()

    def set_label_text(self, new_text):
        new_answer, new_time = new_text
        self.ids.label_answer.text = new_answer
        self.ids.label_time.text = new_time

    def set_answer_text(self, new_text):
        self.ids.label_answer.text = new_text

    def set_time_text(self, new_text):
        self.ids.label_time.text = new_text

    def get_label_text(self):
        label_dict = {
            "label_answer": self.ids.label_answer.text,
            "label_time": self.ids.label_time.text
        }

        return label_dict
