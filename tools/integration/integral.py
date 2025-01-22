__all__ = "Integral"

from sympy import sympify, evalf


class Integral:

    def __init__(self, a, b, expr, integral_mlt=1):
        self.__a = None
        self.__b = None
        self.__integrand = None
        self.__variables = None
        self.__integral_mlt = None

        self.set_integrand(expr)
        self.set_limits(a, b)
        self.set_variables()
        self.set_integral_mlt(integral_mlt)

    def set_limits(self, a, b):
        a_validated = self.validate_limit(a)
        b_validated = self.validate_limit(b)

        self.__a = a_validated
        self.__b = b_validated

    @staticmethod
    def validate_limit(limit):
        try:
            s_limit = sympify(limit)
            if s_limit.free_symbols:
                raise ValueError("Limits can't have free variables!")
            return s_limit
        except Exception as e:
            raise Exception(f"Invalid limits! {e}")

    def set_integrand(self, expr):
        i_validated = self.validate_sympy_expr(expr, "integrand")
        self.__integrand = i_validated

    def set_variables(self):
        self.__variables = self.__integrand.free_symbols

    def set_integral_mlt(self, integral_mlt):
        integral_mlt_validated = self.validate_sympy_expr(integral_mlt, "integral mlt")
        self.__integral_mlt = integral_mlt_validated

    @staticmethod
    def validate_sympy_expr(e, name="expression"):
        try:
            return sympify(e)
        except Exception:
            raise Exception(f"Invalid {name} (check the parentheses and operators)")

    def calculate_integrand(self, **val):
        i_with_vars = self.__integrand.subs(val)
        variable_names = {str(var) for var in self.__variables}

        missing_vars = variable_names - set(val.keys())
        if missing_vars:
            raise Exception(f"Missing values for variables: {', '.join([str(var) for var in missing_vars])}")

        extra_vars = set(val.keys()) - variable_names
        if extra_vars:
            raise Exception(f"Unnecessary variables: {', '.join([str(var) for var in extra_vars])}")

        return i_with_vars.evalf()

    def get_a(self, is_numeric: bool = False):
        return self.__a.evalf() if is_numeric else self.__a

    def get_b(self,  is_numeric: bool = False):
        return self.__b.evalf() if is_numeric else self.__b

    def get_integral_mlt(self, is_numeric: bool = False):
        return self.__integral_mlt.evalf() if is_numeric else self.__integral_mlt

    def get_integrand(self):
        return self.__integrand

    def get_variables(self):
        return self.__variables
