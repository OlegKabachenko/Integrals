__all__ = ("Integrator")

from sympy import evalf
from tools.integration import Integral

class Integrator():  
    def __init__(self):      
        self.methods = {
            "Метод середніх прямокутників": self.mid_rect_method,
            "Метод трапецій": self.trapezoid_method,
            "Метод Сімпсона": self.simpson_method
        }
    def mid_rect_method(self, integral: Integral, n, **extra_var):        
        c = 1/b.evalf()
        h = ((b - a) / n).evalf()
        x = (a + h / 2).evalf()
        
        s = 0
        
        for i in range(1, n+1):
            f = integral.calculate_integrand(x = x,  **extra_var)
            s += f
            x += h
        s = h*s      
        return round(c*s, 6)     

    def trapezoid_method():
        pass

    def simpson_method():
        pass
  
