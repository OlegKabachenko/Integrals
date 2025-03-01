__all__ = "Integral"

from sympy import sympify, zoo, SympifyError, latex
from tools.exceptions import ComplexInfError


class Integral:

    def __init__(self, a, b, integrand, integral_mlt=1):
        self.__a = None
        self.__b = None
        self.__integrand = None
        self.__variables = None
        self.__integral_mlt = None

        self.set_integral_mlt(integral_mlt)
        self.set_integrand(integrand)
        self.set_limits(a, b)
        self.set_variables()

    def set_limits(self, a, b):
        a_validated = self.validate_no_free_var_expr(a, "min limit")
        b_validated = self.validate_no_free_var_expr(b, "max limit")

        if a_validated.evalf() > b_validated.evalf():
            a_validated, b_validated = b_validated, a_validated
            self.__integral_mlt *= -1

        self.__a = a_validated
        self.__b = b_validated

    def set_integrand(self, expr):
        i_validated = Integral.validate_sympy_expr(expr, "integrand")
        self.__integrand = i_validated

    def set_variables(self):
        self.__variables = self.__integrand.free_symbols

    def set_integral_mlt(self, integral_mlt):
        integral_mlt_validated = self.validate_no_free_var_expr(integral_mlt, "integral mlt")
        self.__integral_mlt = integral_mlt_validated

    def get_a(self, is_numeric: bool = False):
        return self.__a.evalf() if is_numeric else self.__a

    def get_b(self, is_numeric: bool = False):
        return self.__b.evalf() if is_numeric else self.__b

    def get_integral_mlt(self, is_numeric: bool = False):
        return self.__integral_mlt.evalf() if is_numeric else self.__integral_mlt

    def get_integrand(self):
        return self.__integrand

    def get_variables(self):
        return self.__variables

    @staticmethod
    def validate_sympy_expr(e, name="expression"):
        try:
            result = sympify(e)
            if result.has(zoo):
                raise ComplexInfError(f"Complex infinity detected!")
            return result
        except SympifyError:
            raise ValueError(f"Invalid {name} (check the parentheses and operators)")

    @staticmethod
    def validate_no_free_var_expr(e, name="expression"):
        s_e = Integral.validate_sympy_expr(e, name)

        if s_e.free_symbols:
            raise ValueError(f"Invalid {name} (can't have free variables)")

        return s_e

    def calculate_integrand(self, **kwargs):
        i_with_vars = self.__integrand.subs(kwargs)
        variable_names = {str(var) for var in self.__variables}

        missing_vars = variable_names - set(kwargs.keys())
        if missing_vars:
            raise Exception(f"Missing values for variables: {', '.join([str(var) for var in missing_vars])}")

        return self.get_integral_mlt(True) * i_with_vars.evalf()

    def get_latex_integral(self):
        latex_a = latex(self.__a)
        latex_b = latex(self.__b)
        latex_intergand = latex(self.__integrand)
        latex_mlt = latex(self.__integral_mlt)

        if self.__integral_mlt != 1:
            return f"${latex_mlt}\\int_{{{latex_a}}}^{{{latex_b}}} {latex_intergand} \\,dx$"
        else:
            return f"$\\int_{{{latex_a}}}^{{{latex_b}}} {latex_intergand} \\,dx$"
