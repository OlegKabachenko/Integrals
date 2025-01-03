__all__ = ("Integrator")

from sympy import sympify, evalf

class Integral():
    def __init__(self, a, b, e):
        self.set_integrand(e)
        self.set_limits(a, b)
        self.variables = self.integrand.free_symbols    

    def set_limits(self, a, b):        
            a_validated = self.validate_limit(a)
            b_validated = self.validate_limit(b)
            
            self.a = a_validated
            self.b = b_validated

    def validate_limit (self, limit):
        try:
            s_limit = sympify(limit)
            if s_limit.free_symbols:               
                raise ValueError("Limits can't have free variables!")
            return s_limit       
        except Exception  as e:  
            raise Exception(f"Invalid limits! {e}")
            
    def set_integrand(self, e):        
            i_validated = self.validate_integrand(e)
            self.integrand = i_validated 
      
    def validate_integrand (self, e):
        try:
            return sympify(e)            
        except Exception:           
            raise Exception("Invalid integrand(check the parentheses and operators)")
      
    def calculate_integrand(self,  **val):      
        i_with_vars = self.integrand.subs(val)
        variable_names = {str(var) for var in self.variables}
        
        missing_vars = variable_names - set(val.keys())       
        if missing_vars:
            raise Exception(f"Missing values for variables: {', '.join([str(var) for var in missing_vars])}")
        
        extra_vars = set(val.keys()) - variable_names
        if extra_vars:
            raise Exception(f"Unnecessary variables: {', '.join([str(var) for var in extra_vars])}")
               
        rezult =  round(i_with_vars.evalf(), 6)
        return rezult

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
        

        
