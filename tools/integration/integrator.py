__all__ = "Integrator"

from tools.integration import Integral
from sympy import integrate, symbols
from tools.exceptions import NotANumberError
from math import isnan


class Integrator:
    @staticmethod
    def check_integral_value(value):
        if isnan(value):
            raise NotANumberError()


    @staticmethod
    def check_interval_splitting(n):
        try:
            return int(n)
        except TypeError:
            raise TypeError(f"n must be int!")

    @staticmethod
    def mid_rect_method(integral: Integral, n, use_runge_corr: bool = True, **kwargs):
        n = Integrator.check_interval_splitting(n)

        a = integral.get_a(True)
        b = integral.get_b(True)

        h = (b - a) / n
        x = a + h / 2

        s = 0

        for i in range(1, n + 1):
            f = integral.calculate_integrand(x=x, **kwargs)
            s += f
            x += h

        integral_value = s * h

        if use_runge_corr:
            integral_value = Integrator.apply_runge_correction(integral, integral_value, n, 2,
                                                               integration_method=Integrator.mid_rect_method,
                                                               **kwargs)
        Integrator.check_integral_value(integral_value)
        return integral_value

    @staticmethod
    def trapezoid_method(integral: Integral, n, use_runge_corr: bool = True, **kwargs):
        n = Integrator.check_interval_splitting(n)

        a = integral.get_a(True)
        b = integral.get_b(True)

        h = (b - a) / n

        integrand_at_a = integral.calculate_integrand(x=a, **kwargs)
        integrand_at_b = integral.calculate_integrand(x=b, **kwargs)

        s = (integrand_at_a + integrand_at_b) / 2

        for i in range(1, n):
            s += integral.calculate_integrand(x=a + i * h, **kwargs)

        integral_value = s * h

        if use_runge_corr:
            integral_value = Integrator.apply_runge_correction(integral, integral_value, n, 2,
                                                               integration_method=Integrator.trapezoid_method,
                                                               **kwargs)

        Integrator.check_integral_value(integral_value)
        return integral_value

    @staticmethod
    def simpson_method(integral: Integral, n, use_runge_corr: bool = True, **kwargs):
        n = Integrator.check_interval_splitting(n)

        a = integral.get_a(True)
        b = integral.get_b(True)

        h = (b - a) / (2 * n)
        x = a
        f = integral.calculate_integrand(x=x, **kwargs)
        s = f / 2
        for i in range(1, n + 1):
            x = x + h
            f = integral.calculate_integrand(x=x, **kwargs)
            s = s + 2 * f
            x = x + h
            f = integral.calculate_integrand(x=x, **kwargs)
            s = s + f
        integral_value = ((2 * s - f) * h / 3)

        if use_runge_corr:
            integral_value = Integrator.apply_runge_correction(integral, integral_value, n, 4,
                                                               integration_method=Integrator.simpson_method,
                                                               **kwargs)

        Integrator.check_integral_value(integral_value)
        return integral_value

    @staticmethod
    def sympy_method(integral: Integral, **kwargs):

        x = symbols('x')
        integral_mlt = integral.get_integral_mlt(True)
        integrand = integral.get_integrand()

        for var_name, value in kwargs.items():
            integrand = integrand.subs(var_name, value)

        integral_value = integrate(integrand, (x, integral.get_a(), integral.get_b()))

        integral_value = integral_mlt * integral_value.evalf()

        Integrator.check_integral_value(integral_value)

        return integral_value

    @staticmethod
    def apply_runge_correction(integral: Integral, integral_value, n, order, integration_method, **kwargs):
        k = 2
        n_new = int(n / k)

        integral_value_new_step = integration_method(integral=integral, n=n_new, use_runge_corr=False, **kwargs)

        correction_factor = (integral_value - integral_value_new_step) / (pow(k, order) - 1)
        corrected_value = integral_value + correction_factor

        return corrected_value

    methods = {
        "Метод середніх прямокутників": mid_rect_method,
        "Метод трапецій": trapezoid_method,
        "Метод Сімпсона": simpson_method,
        "Бібліотечний метод": sympy_method
    }
