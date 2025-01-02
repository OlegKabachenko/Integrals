__all__ = ("IParams")

import os
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.lang import Builder
import math
from config import Config
from kivy.core.window import Window
from sympy import Symbol, sympify
from re import findall



with open(
    os.path.join("uix", "i_params", "i_params.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())

class ParameterText(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.font = 16
        
    def calculate_font_size(self):
        p_width = self.parent.width
        p_height = Config.p_section_height       
      
        screen_width = Window.width
        screen_height = Window.height

       
     
        if screen_width * Config.p_widg_wide_item_mult  > screen_height:
            multiplier = Config.p_font_wide_wid_mult
            self.font = (p_height*multiplier)
        else:
            multiplier = Config.p_font_narrow_wid_mult                    
            chldr_cnt = max(len(self.parent.children), 1)
            self.font = math.floor(p_height * abs(p_width/chldr_cnt/(p_height*multiplier)))
                             
        self.font_size = f"{self.font}sp"      
       
    
    def check_balance(self, text)->bool:
        brackets = {')': '(', ']': '['}
        balance_stack = []

        for symbol in text:
            if symbol in brackets or symbol in brackets.values():
                if symbol not in brackets:
                    balance_stack.append(symbol)
                else:
                    if not balance_stack:
                        return False
                    if balance_stack[-1] == brackets[symbol]:
                        balance_stack.pop()
                    else:
                        return False

        return not balance_stack #return True if text is balansed(balance_stack is empty)

    def check_forbidden_symbols(self, expr, allowed_symbols:set={})-> bool:       
            variables_in_expr = expr.free_symbols         
            allowed_symbols = {Symbol(s) if isinstance(s, str) else s for s in allowed_symbols}#convert str into Symbol
           
            if not variables_in_expr.issubset(allowed_symbols):
                return False
            else:
                return True
            
    def check_function_brackets(self, text):#prevent such structures like "cos" [must be "cos(_content_)"] or "cos(cos)" [must be "cos(cos(_content_))"]
        functions = "(cos|sin|tan|cot|sec|csc|arcsin|arccos|arctan|log)"       
        f_pattern = functions + r"((?!\S)|(?=\s*(\)|\}|\])))"        
       
        if  findall(f_pattern, text):                
            return False
        else:
            return True

    def set_error(self, item):
        item.error = True
        return
    
    def property_validate(self, item, allowed_symbols:set = {}):
        user_input = item.text

        if not self.check_balance(user_input): #check if the input text has balanced brackets.          
            return self.set_error(item)
        
        if not self.check_function_brackets(user_input):                    
            return self.set_error(item)
              
        try:           
            expr = sympify(user_input, convert_xor=True)
            
            if not self.check_forbidden_symbols(expr, allowed_symbols):                    
                return self.set_error(item)
                
        except Exception as e:               
            return self.set_error(item)


class BaseLayout(MDBoxLayout):#Base layout for function parameters    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)        
        self.height = Config.p_section_height       
             
    def orientation_check(self):
        screen_width = Window.width
        screen_height = Window.height  
        
        if screen_width*Config.app_wide_scr_mult  > screen_height:
            self.orientation = "horizontal"
            self.height = Config.p_section_height

            self.spacing = "60dp"         
        
        else:
            self.orientation = "vertical"
            self.height = len(self.children)*Config.p_section_height            
            self.spacing = "20dp"
        
  
class CommonParams(BaseLayout):#Common parameters (limits of integration)
    pass

class BesselParams(BaseLayout):#Bessel parameters  (order of the Bessel function + argument before sin)
    pass

class MidRectParams(BaseLayout):#Params for mid. rectangles method(integration interval partition number)
   pass

class IParams(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self.height = Config.p_section_height
        self.child_font = 16

  
            


   
                
           
        
    
