__all__ = ("LimitParams", "IntegralExprParams", "BesselParams", "IntervalParam")

import os

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.widget import MDWidget

import matplotlib.pyplot as plt

from config import Config

from sympy import Symbol, sympify, SympifyError
from re import findall, match

from tools.mixins import SizableFontMixin

from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

with open(
        os.path.join("uix", "i_params", "i_params.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())


class FormulaDisplay(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = Config.P_SECTION_HEIGHT

    def set_formula(self, math_text):
        fig = plt.figure()
        ax = fig.add_axes((0, 0, 1, 1))
        ax.set_axis_off()

        t = ax.text(0.5, 0.5, math_text,
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=17, color='black')

        bbox = t.get_window_extent()

        fig.set_size_inches(bbox.width / fig.dpi, bbox.height / fig.dpi)
        fig.patch.set_alpha(0)
        canvas = FigureCanvasKivyAgg(plt.gcf())

        canvas.size_hint_x = None
        canvas.width = float(fig.get_size_inches()[0] * fig.dpi)

        self.ids.content_box.clear_widgets()

        self.ids.content_box.add_widget(canvas)


class ParameterText(MDTextField, SizableFontMixin):
    is_required = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font = 16

        mock_widget = MDWidget()  # Create a mock widget since the mixin requires an MDWidget instance
        mock_widget.width = mock_widget.height = self.height

        self.bind(size=lambda instance, value: setattr(self, 'font_size', self.calculate_font(
            self.text, mock_widget, base_font_mlt_wide=Config.P_WIDG_BASE_FONT_MLT,
            base_font_mlt_narrow=Config.P_WIDG_BASE_FONT_MLT, use_txt_corr=False)))

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
    def set_error(item, is_error=True):
        item.error = is_error
        return

    @staticmethod
    def correct_symbols(text):
        text = text.replace('{', '(').replace('}', ')').replace('[', '(').replace(']', ')')
        text = text.replace(',', '.')
        return text

    def property_validate(self, item, allowed_symbols=None):
        if allowed_symbols is None:
            allowed_symbols = set()

        item.text = self.correct_symbols(item.text)

        user_input = item.text

        if not self.check_function_brackets(user_input):
            return self.set_error(item)

        try:
            if (not user_input or not user_input.strip()) and not item.required:
                return self.set_error(item, False)

            expr = sympify(user_input, convert_xor=True)
            if not self.check_forbidden_symbols(expr, allowed_symbols):
                return self.set_error(item)

        except (SympifyError, ZeroDivisionError):
            return self.set_error(item)

        except TypeError:
            return self.set_error(item)


class StrictParameterText(ParameterText):
    pass


class IntegralMltPrText(StrictParameterText):
    is_required = False


class IntegrandText(ParameterText):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__allowed_symbols = {"x"}

    def set_allowed_symbols(self, symbols: set[str]):
        self.__allowed_symbols = symbols

    def get_allowed_symbols(self):
        return self.__allowed_symbols


class BaseLayout(MDBoxLayout):  #Base layout for function parameters
    h_height = NumericProperty(Config.P_SECTION_HEIGHT)

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
            self.spacing = "5sp"
            if not self.is_animated:
                self.height = v_height

        if self.first_call:
            self.first_call = False

    def get_params(self, widget=None, result=None):
        if widget is None:
            widget = self
        if result is None:
            result = {}

        ids_dict = widget.ids.items()

        for key, value in ids_dict:
            if isinstance(value, MDTextField):
                result[key] = self.get_param_text(value)
            self.get_params(value, result)

        return result

    @staticmethod
    def get_param_text(widget):
        if widget.error:
            raise ValueError(f"Widget is in error state!")
        else:
            return widget.text


class LimitParams(BaseLayout):  #Common parameters (limits of integration)
    def set_params(self, a, b):
        self.ids.a.text = a
        self.ids.b.text = b

    def get_params(self, **kwargs):
        result = {
            "a": self.get_param_text(self.ids.a),
            "b": self.get_param_text(self.ids.b)
        }
        return result


class IntegralExprParams(BaseLayout):  #Common parameters (limits of integration)
    def set_params(self, mlt, expr, allowed_symbols):
        self.ids.integral_mlt.text = mlt

        integrand = self.ids.integrand
        integrand.set_allowed_symbols(allowed_symbols)
        integrand.text = expr

    def get_params(self, **kwargs):
        result = {
            "integral_mlt": self.get_param_text(self.ids.integral_mlt) or "1",
            "integrand": self.get_param_text(self.ids.integrand)
        }
        return result


class BesselParams(BaseLayout):  #Bessel's parameters  (order of the Bessel function + argument before sin)
    def get_params(self, **kwargs):
        result = {
            "z": self.get_param_text(self.ids.z),
            "p": self.get_param_text(self.ids.p)
        }
        return result


class IntervalParam(BaseLayout):  #Interval parameters  (min/max)
    def get_params(self, **kwargs):
        return self.get_param_text(self.ids.n)
