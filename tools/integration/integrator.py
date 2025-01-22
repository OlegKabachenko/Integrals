__all__ = "Integrator"

from sympy import evalf
from tools.integration import Integral


class Integrator:

    @staticmethod
    def mid_rect_method(integral: Integral, n: int, **extra_var):
        a = integral.get_a(True)
        b = integral.get_b(True)
        integral_mlt = integral.get_integral_mlt(True)

        h = (a - b) / n
        x = a + h / 2

        s = 0

        for i in range(1, n + 1):
            f = integral.calculate_integrand(x=x, **extra_var)
            s += f
            x += h

        integral_value = integral_mlt * s * h

        return integral_value

    @staticmethod
    def trapezoid_method(integral: Integral, n: int, use_runge_corr: bool = True, **extra_var):
        a = integral.get_a(True)
        b = integral.get_b(True)
        integral_mlt = integral.get_integral_mlt(True)

        h = (b - a) / n

        integrand_at_a = integral.calculate_integrand(x=a, **extra_var)
        integrand_at_b = integral.calculate_integrand(x=b, **extra_var)

        s = (integrand_at_a + integrand_at_b) / 2

        for i in range(1, n):
            s += integral.calculate_integrand(x=a + i * h, **extra_var)

        integral_value = integral_mlt * s * h

        if use_runge_corr:
            integral_value = Integrator.apply_runge_correction(integral, integral_value, n, 2,
                                                               integration_method=Integrator.trapezoid_method,
                                                               **extra_var)

        return integral_value

    @staticmethod
    def simpson_method(integral: Integral, n: int, use_runge_corr: bool = True, **extra_var):
        a = integral.get_a(True)
        b = integral.get_b(True)
        integral_mlt = integral.get_integral_mlt(True)

        h = (b-a)/(2*n)
        x = a
        f = integral.calculate_integrand(x=x, **extra_var)
        s = f / 2
        for i in range(1, n + 1):
            x = x + h
            f = integral.calculate_integrand(x=x, **extra_var)
            s = s + 2 * f
            x = x + h
            f = integral.calculate_integrand(x=x, **extra_var)
            s = s + f
        integral_value = integral_mlt*((2 * s - f) * h / 3)

        if use_runge_corr:
            integral_value = Integrator.apply_runge_correction(integral, integral_value, n, 4,
                                                               integration_method=Integrator.simpson_method,
                                                               **extra_var)

        return integral_value

    @staticmethod
    def apply_runge_correction(integral: Integral, integral_value, n, p, integration_method, **extra_var):
        k = 2
        n_new = int(n / k)

        integral_value_new_step = integration_method(integral=integral, n=n_new, use_runge_corr=False, **extra_var)

        correction_factor = (integral_value-integral_value_new_step) / (pow(k, p) - 1)
        corrected_value = integral_value + correction_factor

        return corrected_value

    methods = {
        "Метод середніх прямокутників": mid_rect_method,
        "Метод трапецій": trapezoid_method,
        "Метод Сімпсона": simpson_method
    }
