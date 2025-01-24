__all__ = ("LimitParams", "IntegralExprParams", "BesselParams", "IntervalParam")

import os
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import BooleanProperty
from kivy.lang import Builder
import math
from config import Config
from kivy.core.window import Window
from sympy import Symbol, sympify, SympifyError
from re import findall, match

with open(
        os.path.join("uix", "i_params", "i_params.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class ParameterText(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font = 16

    def calculate_font_size(self):
        p_width = self.parent.width
        p_height = Config.P_SECTION_HEIGHT

        screen_width = Window.width
        screen_height = Window.height

        if screen_width * Config.P_WIDG_WIDE_ITEM_MULT > screen_height:
            multiplier = Config.P_FONT_WIDE_WID_MULT
            self.font = (p_height * multiplier)
        else:
            multiplier = Config.P_FONT_NARROW_WID_MULT
            chldr_cnt = max(len(self.parent.children), 1)
            self.font = math.floor(p_height * abs(p_width / chldr_cnt / (p_height * multiplier)))

        self.font_size = f"{self.font}sp"

    @staticmethod
    def check_forbidden_symbols(expr, allowed_symbols=None) -> bool:
        if allowed_symbols is None:
            allowed_symbols = set()

        variables_in_expr = expr.free_symbols
        allowed_symbols = {Symbol(s) if isinstance(s, str) else s for s in allowed_symbols}  #convert str into Symbol

        if not variables_in_expr.issubset(allowed_symbols):
            return False
        else:
            return True

    @staticmethod
    def check_function_brackets(
            text):  #prevent such structures like "cos" [must be "cos(_content_)"] or "cos(cos)" [must be "cos(cos(_content_))"]
        functions = "(cos|sin|tan|cot|sec|csc|arcsin|arccos|arctan|log)"
        f_pattern = functions + r"((?!\S)|(?=\s*(\)|\}|\])))"

        if match(r'^[()]+$', text):
            return False

        if findall(f_pattern, text):
            return False
        else:
            return True

    @staticmethod
    def set_error(item):
        item.error = True
        return

    def property_validate(self, item, allowed_symbols=None):
        if allowed_symbols is None:
            allowed_symbols = set()
        user_input = item.text
        user_input = user_input.replace('{', '(').replace('}', ')').replace('[', '(').replace(']', ')')

        if not self.check_function_brackets(user_input):
            return self.set_error(item)

        try:
            expr = sympify(user_input, convert_xor=True)
            if not self.check_forbidden_symbols(expr, allowed_symbols):
                return self.set_error(item)

        except SympifyError:
            return self.set_error(item)

        except TypeError:
            return self.set_error(item)


class StrictParameterText(ParameterText):
    pass


class IntegrandText(ParameterText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__allowed_symbols = {"x"}

    def set_allowed_symbols(self, symbols: set[str]):
        self.__allowed_symbols = symbols

    def get_allowed_symbols(self):
        return self.__allowed_symbols


class BaseLayout(MDBoxLayout):  #Base layout for function parameters
    h_height = Config.P_SECTION_HEIGHT

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = Config.P_SECTION_HEIGHT
        self.is_animated = False
        self.first_call = True

    def on_kv_post(self, base_widget):
        self.is_animated = False
        self.first_call = True

    def set_params(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.ids:
                self.ids[key].text = value

    def orientation_check(self):
        v_height = len(self.children) * self.h_height

        screen_width = Window.width
        screen_height = Window.height
        critical_wdth = screen_width * Config.APP_WIDE_SCR_MULT

        if (critical_wdth > screen_height and self.height != self.h_height) or self.first_call:
            self.orientation = "horizontal"
            self.spacing = "60dp"
            if not self.is_animated:
                self.height = self.h_height

        elif (critical_wdth <= screen_height and self.height != v_height) or self.first_call:
            self.orientation = "vertical"
            self.spacing = "0dp"
            if not self.is_animated:
                self.height = v_height

        if self.first_call:
            self.first_call = False


class LimitParams(BaseLayout):  #Common parameters (limits of integration)
    def set_params(self, a, b):
        self.ids.a_text.text = a
        self.ids.b_text.text = b


class IntegralExprParams(BaseLayout):  #Common parameters (limits of integration)
    def set_params(self, mlt, expr, allowed_symbols):
        self.ids.integral_mlt.text = mlt

        integrand = self.ids.integrand
        integrand.set_allowed_symbols(allowed_symbols)
        integrand.text = expr


class BesselParams(BaseLayout):  #Bessel's parameters  (order of the Bessel function + argument before sin)
    pass


class IntervalParam(BaseLayout):  # Common param for all method(integration interval partition number)
    pass
