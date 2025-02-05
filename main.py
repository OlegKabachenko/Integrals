from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button

from kivymd.uix.boxlayout import MDBoxLayout

from config import Config
from tools.integration import Integrator
from tools.integration import Integral
from tools.animation import Animator
from tools.exceptions import ComplexInfError

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
    example_keys = list(Config.INTEGRAL_EXAMPLES.keys())
    example_values = list(Config.INTEGRAL_EXAMPLES.values())
    method_keys = list(Integrator.methods.keys())
    method_values = list(Integrator.methods.values())
    start_example_id = Config.DEFAULT_EXAMPLE_ID
    start_method_id = Config.DEFAULT_METHOD_ID
    animator = Animator()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

        self.current_method_id = None

        self.bs_params = BesselParams()

        self.example_cnahge_actions = {i: self.default_expl_cnhg_actions(i) for i in
                                       range(len(Config.INTEGRAL_EXAMPLES))}
        self.set_unique_expl_cnhg_actions()

        Clock.schedule_once(self.init_params)  #set default values for parameters fields

    def init_params(self, _):
        self.current_method_id = self.start_method_id
        self.handle_example_select(self.start_example_id, self.start_example_id + 1)
        self.handle_method_select(self.start_method_id, self.start_method_id + 1)

    def default_expl_cnhg_actions(self, i):
        return {
            "add_action": lambda: None,
            "set_values_action": lambda: self.set_input_values(i),
        }

    def set_unique_expl_cnhg_actions(self):
        self.example_cnahge_actions[0]["add_action"] = lambda: (
            self.animator.animate_widget_add(
                self.ids.extra_integral_params_box,
                self.bs_params,
                Config.ANIMATION_DURATION
            ))

    def set_input_values(self, i):
        a = b = int_mlt = integrand = ""
        allowed_symbols = {"x"}

        integral = self.example_values[i]
        if integral is not None:
            a = str(integral.get_a())
            b = str(integral.get_b())

            int_mlt = str(integral.get_integral_mlt())
            integrand = str(integral.get_integrand())

            allowed_symbols = integral.get_variables()

        self.ids.limits_params.set_params(a, b)
        self.ids.integral_expr_params.set_params(int_mlt, integrand, allowed_symbols)

    def handle_example_select(self, s_id, prev_id):
        if s_id != prev_id:
            self.animator.animate_container_clear(self.ids.extra_integral_params_box, Config.ANIMATION_DURATION)

            actions = self.example_cnahge_actions.get(s_id)

            for key in actions:
                action = actions.get(key)
                if action is not None:
                    action()
            self.clear_result_output()

    def handle_method_select(self, s_id, prev_id):
        if s_id != prev_id:
            self.current_method_id = s_id
            self.clear_result_output()

    def get_integral_params(self):
        extra_params_box = self.ids.extra_integral_params_box
        extra_integral_params = {}

        try:
            limits = self.ids.limits_params.get_params()
            integral_params = self.ids.integral_expr_params.get_params()
            n = self.ids.interval_param.get_params()

            if extra_params_box.children:
                extra_integral_params = extra_params_box.children[0].get_params()

            return limits, integral_params, n, extra_integral_params

        except ValueError:
            return None

    def get_integral_value(self):
        params = self.get_integral_params()

        if params is None:
            self.show_error("Будь ласка, правильно заповніть поля!")
            return

        limits, integral_params, n, extra_integral_params = params

        a, b = limits["a"], limits["b"]
        integrand = integral_params["integrand"]
        integral_mlt = integral_params["integral_mlt"]

        try:
            integral = Integral(a, b, integrand, integral_mlt)
        except ComplexInfError:
            self.show_error("Комплексна нескінченність, перевірьте данні!")
            return

        result = self.method_values[self.current_method_id](integral, n, **extra_integral_params)

        self.set_result_output(round(result, Config.ROUND_PRECISION))

    def show_error(self, text):
        self.ids.error_msg.set_text_change_state(text)

    def set_result_output(self, content, is_error: bool = False):
        if is_error:
            text = str(content)
        else:
            text = "Відповідь: " + str(content)
        self.ids.calculate_box.set_label_text(text)

    def clear_result_output(self):
        self.ids.calculate_box.set_label_text("")

    @staticmethod
    def unlock_widget(widget):
        widget.disabled = False


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
