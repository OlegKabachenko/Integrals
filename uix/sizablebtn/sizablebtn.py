__all__ = ("SizableBtn")

import os

import yaml
from kivy.lang import Builder
from kivymd.uix.button import MDFabButton

from uix.mixins import SizableFontMixin

with open('uix/uix_config.yaml', 'r') as file, \
     open(os.path.join("uix", "sizablebtn", "sizablebtn.kv"), encoding="utf-8") as kv_file:
    config = yaml.safe_load(file)
    Builder.load_string(kv_file.read())


class SizableBtn(MDFabButton, SizableFontMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(
            self.text, self, root=self, root_width_mlt=config['BTN_ROOT_WIDTH_MLT'],
            base_font_mlt_wide=config['BTN_BASE_FONT_MLT'], base_font_mlt_narrow=config['BTN_BASE_FONT_MLT'])))
