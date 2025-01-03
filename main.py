from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.imagelist.imagelist import MDSmartTile
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDButton
from kivymd.uix.divider import MDDivider

from kivy.core.window import Window

import math
from config import Config
from tools.integration import Integrator

from uix.i_params import *
from uix.selector import EMSelector
from kivy.properties import ObjectProperty

Builder.load_file("main.kv")#import main interface file  

class StandartBoxLayout(MDBoxLayout):
    pass

class MenuItem(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  
        self.padding_x = "10sp"       
        self.halign = "left"

class MainLayout(MDBoxLayout):   
    integrator = Integrator()
    config = Config()   
    
    def remove_child_widgets_except(self, container, widgets_to_keep):
        for widget in container.children[:]:  
            if not isinstance(widget, tuple(widgets_to_keep)): 
                container.remove_widget(widget)
                
    def handle_example_select(self, instance, s_id):     
        print("handle_example_select")
        
    def handle_method_select(self, instance, s_id):
        print("handle_method_select")    
       
class SMethodsApp(MDApp):   
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_config = Config()
        self.bs_params = BesselParams()
 
    def switch_theme_style(self):            
        self.theme_cls.theme_style = (
            "Dark" if self.theme_cls.theme_style == "Light" else "Light"
        )

        self.theme_cls.surfaceContainerHighestColor = (
            self.app_config.card_l_color if self.theme_cls.theme_style == "Light" else self.theme_cls.surfaceContainerHighestColor
        )
                                  
    def build(self):        
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Azure"
        
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.surfaceContainerHighestColor = self.app_config.card_l_color
        return MainLayout()

    def on_start(self):   
        self.root.ids.enter_box.add_widget(self.bs_params)        
       
      
     
if __name__ == '__main__':
   SMethodsApp().run()


