from sympy import *

class Integrator():  
    def __init__(self):
        self.formulas = ["Приклад 1", "Приклад 2", "Приклад 3", "Введення власного інтегралу"]

        self.methods = ["Метод середніх прямокутників", "Метод трапецій", "Метод Сімпсона"]
        
    def mid_rect_method(self, a, b, n, function: Function, **extra_var):
        a = sympify(a)
        b = sympify(b)
        
        c = 1/b.evalf()
        h = ((b - a) / n).evalf()
        x = (a + h / 2).evalf()
        
        s = 0
        
        for i in range(1, n+1):
            f = function.calculate(x = x,  **extra_var)
            s += f
            x += h
        s = h*s
        print(round(c*s, 6))   
        return round(c*s, 6)     

class Function():
    def __init__(self, e):       
        self.set_expression(e)
        self.variables = self.expression.free_symbols

    def set_expression(self, e):        
            e_validated = self.validate_expression(e)
            self.expression = e_validated    
      
    def validate_expression (self, e):
        try:
            return sympify(e)            
        except Exception as e:           
            raise Exception("Invalid function expression(check the parentheses and operators)")
      
    def calculate(self,  **val):      
        e_with_vars = self.expression.subs(val)
        variable_names = {str(var) for var in self.variables}
        
        missing_vars = variable_names - set(val.keys())       
        if missing_vars:
            raise Exception(f"Missing values for variables: {', '.join([str(var) for var in missing_vars])}")
        
        extra_vars = set(val.keys()) - variable_names
        if extra_vars:
            raise Exception(f"Unnecessary variables: {', '.join([str(var) for var in extra_vars])}")
               
        rezult =  round(e_with_vars.evalf(), 6)
        return rezult

class Integral():
    def __init__(self, a, b, func: Function):
        self.function = func
        self.a = a
        self.b = b

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
        

        
