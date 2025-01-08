__all__ = "Integrator"

from sympy import evalf
from tools.integration import Integral


class Integrator:

    def __init__(self):
        self.methods = {
            "Метод середніх прямокутників": self.mid_rect_method,
            "Метод трапецій": self.trapezoid_method,
            "Метод Сімпсона": self.simpson_method
        }

    @staticmethod
    def mid_rect_method(integral: Integral, n, **extra_var):
        c = 1 / integral.b.evalf()
        h = ((integral.b - integral.a) / n).evalf()
        x = (integral.a + h / 2).evalf()

        s = 0

        for i in range(1, n + 1):
            f = integral.calculate_integrand(x=x, **extra_var)
            s += f
            x += h
        s = h * s
        return round(c * s, 6)

    @staticmethod
    def trapezoid_method(self):
        pass

    @staticmethod
    def simpson_method(self):
        pass
