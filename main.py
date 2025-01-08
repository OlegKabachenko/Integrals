from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button

from kivymd.uix.boxlayout import MDBoxLayout
from config import Config
from tools.integration import Integrator
from tools.animation import Animator

from uix.i_params import *

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen

Builder.load_file("main.kv")  #import main interface file


class StandartBoxLayout(MDBoxLayout):
    pass


class ParameterBox(MDBoxLayout):
    pass


class MenuItem(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding_x = "10sp"
        self.halign = "left"


class MainLayout(MDScreen):
    integrator = Integrator()
    example_keys = list(Config.INTEGRAL_EXAMPLES.keys())
    start_example_id = Config.DEFAULT_EXAMPLE_ID
    start_method_id = Config.DEFAULT_METHOD_ID
    animator = Animator()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bs_params = BesselParams()
        self.md_rect_params = MidRectParams()

        Clock.schedule_once(self.init_params)  #set default parameters fields

    def init_params(self, _):
        self.handle_example_select(self.start_example_id, self.start_example_id + 1)
        self.handle_method_select(self.start_method_id, self.start_method_id + 1)

    def handle_example_select(self, s_id, prev_id):
        if s_id != prev_id:
            self.animator.animate_container_clear(self.ids.extra_integral_params)
            if s_id == 0:
                self.animator.animate_widget_add(self.ids.extra_integral_params, self.bs_params)

    def handle_method_select(self, s_id, prev_id):
        if s_id != prev_id:
            print()
            self.animator.animate_container_clear(self.ids.method_params)
            self.animator.animate_widget_add(self.ids.method_params, self.md_rect_params)


class SMethodsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = MainLayout()

    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

        self.theme_cls.surfaceContainerHighestColor = (
            Config.CARD_L_COLOR
            if self.theme_cls.theme_style == "Light"
            else self.theme_cls.surfaceContainerHighestColor
        )

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Azure"

        if self.theme_cls.theme_style == "Light":
            self.theme_cls.surfaceContainerHighestColor = Config.CARD_L_COLOR

        return self.main_layout


if __name__ == '__main__':
    SMethodsApp().run()
