__all__ = ("Integrator")

from sympy import evalf
from tools.integration import Integral

class Integrator():  
    def __init__(self):      
        self.formulas = ["Приклад 1", "Приклад 2", "Приклад 3", "Введення власного інтегралу"]

        #self.methods = ["Метод середніх прямокутників", "Метод трапецій", "Метод Сімпсона"]
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
  


class Integral_Examples():
    def __init__(self, e):  
        f1 = Function("cos(z*sin(x) - p*x)")
        f2 = Function("(x^2+5*x+6)*sin(3*x)")
        f3 = Function("1/(sqrt(x)-1)")

        i1 = (0,"pi",f1)
        i2 = (0,"pi/2",f2)
        i3 = (4,9,f2)
        
        self.ex = [
                (i1, "Приклад 1"),
                (i2, "Приклад 2"),
                (i3, "Приклад 3"),
                (None, "Введення власного інтегралу")
            ]
        

        
