__all__ = ("CommonParams", "BesselParams", "MidRectParams")

import os
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.properties import BooleanProperty
from kivy.lang import Builder
import math
from config import Config
from kivy.core.window import Window
from sympy import Symbol, sympify, SympifyError
from re import findall

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
    def check_balance(text) -> bool:
        brackets = {')': '(', ']': '['}
        balance_stack = []

        for symbol in text:
            if symbol in brackets or symbol in brackets.values():
                if symbol not in brackets:
                    balance_stack.append(symbol)
                else:
                    if not balance_stack:
                        return False
                    if balance_stack[-1] == brackets[symbol]:
                        balance_stack.pop()
                    else:
                        return False

        return not balance_stack  #return True if text is balansed(balance_stack is empty)

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

        if not self.check_balance(user_input):  #check if the input text has balanced brackets.
            return self.set_error(item)

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


class BaseLayout(MDBoxLayout):  #Base layout for function parameters
    first_call = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = Config.P_SECTION_HEIGHT

    def on_kv_post(self, base_widget):
        print("kivipost")
        self.first_call = True

    def orientation_check(self):
        screen_width = Window.width
        screen_height = Window.height

        critical_wdth = screen_width * Config.APP_WIDE_SCR_MULT

        # When the widget is being initialized (first call to orientation_check),
        # the current value of self.orientation does not affect the setup.
        if critical_wdth > screen_height and (self.orientation == "vertical" or self.first_call):
            self.orientation = "horizontal"
            self.height = Config.P_SECTION_HEIGHT
            self.spacing = "60dp"

        elif critical_wdth <= screen_height and (self.orientation == "horizontal" or self.first_call):
            self.orientation = "vertical"
            self.height = len(self.children) * Config.P_SECTION_HEIGHT
            self.spacing = "0dp"

        if self.first_call:
            self.first_call = False


class CommonParams(BaseLayout):  #Common parameters (limits of integration)
    pass


class BesselParams(BaseLayout):  #Bessel's parameters  (order of the Bessel function + argument before sin)
    pass


class MidRectParams(BaseLayout):  #Params for mid. rectangles method(integration interval partition number)
    pass
