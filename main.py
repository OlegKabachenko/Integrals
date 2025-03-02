import time

import yaml
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.uix.boxlayout import MDBoxLayout

from tools.integration import Integrator
from tools.integration import Integral
from tools.animation import Animator
from tools.exceptions import ComplexInfError, NotANumberError

from uix.i_params import *

from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
import inspect

Builder.load_file("main.kv")  #import main interface file

with open('config.yaml', 'r', encoding="utf-8") as file:
    config = yaml.safe_load(file)


class StandartBoxLayout(MDBoxLayout):
    pass


class ParameterBox(MDBoxLayout):
    pass


class MainLayout(MDScreen):
    INTEGRAL_EXAMPLES = {
        key: Integral(*value) if value else None
        for key, value in config["INTEGRAL_EXAMPLES"].items()
    }

    EXAMPLE_KEYS = list(INTEGRAL_EXAMPLES.keys())
    EXAMPLE_VALUES = list(INTEGRAL_EXAMPLES.values())
    METHOD_KEYS = list(Integrator.methods.keys())
    METHOD_VALUES = list(Integrator.methods.values())
    DEFAULT_METHOD_ID = config['DEFAULT_METHOD_ID']
    DEFAULT_EXAMPLE_ID = config['DEFAULT_EXAMPLE_ID']
    animator = Animator()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None

        self.current_method_id = None

        self.bs_params = BesselParams()
        self.interval_param = IntervalParam()

        self.example_change_actions = {i: self.default_expl_chng_actions(i) for i in
                                       range(len(self.INTEGRAL_EXAMPLES))}
        self.set_unique_expl_chng_actions()
        self.method_change_actions = {i: self.default_method_chng_actions() for i in
                                      range(len(Integrator.methods))}
        self.set_unique_method_chng_actions()

        Clock.schedule_once(self.init_params)  #set default values for parameters fields

    def init_params(self, _):
        self.current_method_id = self.DEFAULT_METHOD_ID
        self.handle_example_select(self.DEFAULT_EXAMPLE_ID,  self.DEFAULT_EXAMPLE_ID + 1)
        self.handle_method_select(self.DEFAULT_METHOD_ID, self.DEFAULT_METHOD_ID + 1)

    def add_interval_param(self):
        parent_box = self.ids.interval_param_box
        if self.interval_param not in parent_box.children:
            self.animator.animate_widget_add(
                parent_box,
                self.interval_param,
                config['ANIMATION_DURATION']
            )

    def default_expl_chng_actions(self, i):
        return {
            "add_action": lambda: None,
            "set_values_action": lambda: self.set_input_values(i),
        }

    def set_unique_expl_chng_actions(self):
        self.example_change_actions[0]["add_action"] = lambda: (
            self.animator.animate_widget_add(
                self.ids.extra_integral_params_box,
                self.bs_params,
                config['ANIMATION_DURATION']
            ))

    def default_method_chng_actions(self):
        return {
            "clear_action": lambda: None,
            "add_action": lambda: self.add_interval_param(),
        }

    def set_unique_method_chng_actions(self):
        self.method_change_actions[3]["clear_action"] = lambda: (
            self.animator.animate_container_clear(
                self.ids.interval_param_box,
                config['ANIMATION_DURATION']
            ))
        self.method_change_actions[3]["add_action"] = lambda: None

    def set_input_values(self, i):
        a = b = int_mlt = integrand = ""
        allowed_symbols = {"x"}

        integral = self.EXAMPLE_VALUES[i]
        if integral is not None:
            a = str(integral.get_a())
            b = str(integral.get_b())

            int_mlt = str(integral.get_integral_mlt())
            integrand = str(integral.get_integrand())

            allowed_symbols = integral.get_variables()

        self.ids.limits_params.set_params(a, b)
        self.ids.integral_expr_params.set_params(int_mlt, integrand, allowed_symbols)

    def execute_actions(self, s_id, is_example_actions: bool):
        if is_example_actions:
            actions = self.example_change_actions.get(s_id)
        else:
            actions = self.method_change_actions.get(s_id)
        for key, action in actions.items():
            if action is not None:
                action()

    def handle_example_select(self, s_id, prev_id):
        if s_id != prev_id:
            self.animator.animate_container_clear(self.ids.extra_integral_params_box, config['ANIMATION_DURATION'])

            self.execute_actions(s_id, True)

            self.clear_result_output()
            self.update_formula_display(self.EXAMPLE_VALUES[s_id])

    def handle_method_select(self, s_id, prev_id):
        if s_id != prev_id:
            self.current_method_id = s_id

            self.execute_actions(s_id, False)

            self.clear_result_output()

    def get_integral_params(self):
        extra_params_box = self.ids.extra_integral_params_box
        interval_param_box = self.ids.interval_param_box
        extra_integral_params = {}
        n = None

        try:
            limits = self.ids.limits_params.get_params()
            integral_params = self.ids.integral_expr_params.get_params()

            if interval_param_box.children:
                n = interval_param_box.children[0].get_params()

            if extra_params_box.children:
                extra_integral_params = extra_params_box.children[0].get_params()

            return limits, integral_params, n, extra_integral_params

        except ValueError:
            return None

    def update_formula_display(self, integral: Integral):
        if integral is None:
            math_text = f"$\\int_{{{"a"}}}^{{{"b"}}} {""} \\,dx$"
        else:
            math_text = integral.get_latex_integral()
        self.ids.formula_display.set_formula(math_text)

    def show_error(self, text):
        self.ids.error_msg.set_text_change_state(text)

    def clear_result_output(self):
        self.ids.calculate_box.set_label_text(["", ""])

    def set_result_output(self, answer, exec_time):

        answer = "Відповідь: " + str(answer)
        exec_time = "Час виконання: " + str(exec_time) + " сек."

        self.ids.calculate_box.set_label_text([answer, exec_time])

    @staticmethod
    def unlock_widget(widget):
        widget.disabled = False


class SMethodsApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = MainLayout()

    def call_integrator(self, integral, n, **kwargs):
        method = self.main_layout.METHOD_VALUES[self.main_layout.current_method_id]
        method_signature = inspect.signature(method)

        if 'n' in method_signature.parameters:
            args = (integral, n)
        else:
            args = (integral,)

        try:
            start_time = time.time()
            result = method(*args, **kwargs)
            end_time = time.time()
        except NotANumberError:
            self.main_layout.show_error("Відповідь не число, перевірьте данні!")
            return None

        exec_time = end_time - start_time

        return result, exec_time

    def get_integral_value(self):
        self.main_layout.clear_result_output()
        params = self.main_layout.get_integral_params()

        if params is None:
            self.main_layout.show_error("Будь ласка, правильно заповніть поля!")
            return

        limits, integral_params, n, extra_integral_params = params

        a, b = limits["a"], limits["b"]
        integrand = integral_params["integrand"]
        integral_mlt = integral_params["integral_mlt"]

        try:
            integral = Integral(a, b, integrand, integral_mlt)
        except ComplexInfError:
            self.main_layout.show_error("Комплексна нескінченність, перевірьте данні!")
            return

        result, exec_time = self.call_integrator(integral, n, **extra_integral_params)

        self.main_layout.update_formula_display(integral)
        if result is not None:
            result = round(result, config['ROUND_PRECISION'])
            exec_time = round(exec_time, config['EXEC_TIME_PRECISION'])
            self.main_layout.set_result_output(result, exec_time)

    def switch_theme_style(self):
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

        self.theme_cls.surfaceContainerHighestColor = (
            config['CARD_L_COLOR']
            if self.theme_cls.theme_style == "Light"
            else self.theme_cls.surfaceContainerHighestColor
        )

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Azure"

        if self.theme_cls.theme_style == "Light":
            self.theme_cls.surfaceContainerHighestColor = config['CARD_L_COLOR']

        return self.main_layout


if __name__ == '__main__':
    SMethodsApp().run()
