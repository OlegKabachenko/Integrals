__all__ = "Integral"

from sympy import sympify, evalf


class Integral:

    def __init__(self, a, b, expr, integral_mlt=1):
        self.a = None
        self.b = None
        self.integrand = None
        self.variables = None
        self.integral_mlt = None

        self.set_integrand(expr)
        self.set_limits(a, b)
        self.set_free_symbhols()
        self.set_integral_mlt(integral_mlt)

    def set_limits(self, a, b):
        a_validated = self.validate_limit(a)
        b_validated = self.validate_limit(b)

        self.a = a_validated
        self.b = b_validated

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
        self.integrand = i_validated

    def set_free_symbhols(self):
        self.variables = self.integrand.free_symbols

    def set_integral_mlt(self, integral_mlt):
        integral_mlt_validated = self.validate_sympy_expr(integral_mlt, "integral mlt")
        self.integral_mlt = integral_mlt_validated

    @staticmethod
    def validate_sympy_expr(e, name="expression"):
        try:
            return sympify(e)
        except Exception:
            raise Exception(f"Invalid {name} (check the parentheses and operators)")

    def calculate_integrand(self, **val):
        i_with_vars = self.integrand.subs(val)
        variable_names = {str(var) for var in self.variables}

        missing_vars = variable_names - set(val.keys())
        if missing_vars:
            raise Exception(f"Missing values for variables: {', '.join([str(var) for var in missing_vars])}")

        extra_vars = set(val.keys()) - variable_names
        if extra_vars:
            raise Exception(f"Unnecessary variables: {', '.join([str(var) for var in extra_vars])}")

        return i_with_vars.evalf()
