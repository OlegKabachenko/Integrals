__all__ = "BigTouchSwitch"

import os

from kivy.properties import BooleanProperty, NumericProperty, StringProperty, ObjectProperty
from kivy.lang import Builder

from kivymd.uix.boxlayout import MDBoxLayout

with open(
        os.path.join("uix", "bigtouchswitch", "bigtouchswitch.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class BigTouchSwitch(MDBoxLayout):
    active = BooleanProperty(False)
    switch_width = NumericProperty(80)
    icon_active = StringProperty("check")
    icon_inactive = StringProperty("close")
    on_active = ObjectProperty(lambda instance, value: None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.active = not self.active
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super().on_touch_up(touch)
