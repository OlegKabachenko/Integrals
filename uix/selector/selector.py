__all__ = ("Selectora")

import os
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFabButton
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivy.lang import Builder

from kivy.core.window import Window
from kivy.properties import ListProperty
from kivy.clock import Clock

import math

from config import Config
from integration import Integrator


with open(
    os.path.join("uix", "selector", "selector.kv"), encoding="utf-8"
) as kv_file:
    Builder.load_string(kv_file.read())

class EMSelector(MDBoxLayout): 
    items_list = ListProperty()
    
    def __init__(self, **kwargs):       
        super().__init__(**kwargs) 
        self.register_event_type('on_select')      
        Clock.schedule_once(self.init_label)#draw default text

    def init_label(self, *args):        
        self.ids.button.menu_callback(0, self.ids.field,  self.items_list[0])
                  
    def event_dispatch(self, s_id):        
        event = 'on_select'
        self.dispatch(event, s_id)
   
    def on_select(self, s_id):
        pass             

class SelectButton(MDFabButton):      
    def __init__(self, **kwargs):
        super().__init__(**kwargs)   
        self.integrator = Integrator()
             
    def calculate_menu_item_font(self, menu_width, text):
        font_size = 16  
       
        root_w = Window.width
        root_h = Window.height    
        if root_w  >  root_h:
            font_size =  str(menu_width/(Config.menu_item_wide_fnt_mult*root_w/root_h)) + "sp"
                   
        else:           
           font_size =  str(menu_width/(Config.menu_item_narrow_fnt_mult*root_w/root_h)) + "sp"
        return font_size

    def build_menu(self, item, text_field=None):
        menu_items = []
        root_w = Window.width  
        
        menu_width =   root_w/1.5       

        source_list =  self.parent.items_list
                
        for i, entry in enumerate(source_list):   
            text = entry 
            font_size = self.calculate_menu_item_font(menu_width, text)
            background_color = MDApp.get_running_app().theme_cls.transparentColor
            text_color = MDApp.get_running_app().theme_cls.onSurfaceColor
        
            menu_items.append(
                {
                "viewclass": "MenuItem", 
                "text": text,
                "font_size": font_size,               
             
                "background_color": background_color,
                "color": text_color,
                "text_size": [menu_width, None],                
                       
                "on_release": lambda s_id=i, text_item=text: self.menu_callback(s_id,  text_field, text_item),               
                })
               
            menu_items.append(
                {
                    "viewclass": "MDDivider",
                    "height": 1,
                }
            )
    
        self.menu = MDDropdownMenu(caller=item, items=menu_items, width=menu_width)
        self.menu.open()

    def menu_callback(self, s_id, text_field, text):      
        if text_field is not None:        
            text_field.text = text

        if hasattr(self, 'menu'):
            if self.menu:
                self.menu.dismiss()
                
        self.parent.event_dispatch(s_id)
       
        #if is_f_list:
            #enter_box = self.ids.enter_box           
            #self.remove_child_widgets_except(enter_box, [CFLayout])
            #if f_id == 0:               
                #enter_box.add_widget(CFLayout())
            #else:
                #enter_box.add_widget(BesselLayout())
   
    

class SFMArea(MDBoxLayout):
    pass

class SFMLabel(MDLabel):           
    def calculate_font_size(self): 
        font_corr_divider = Config.sfm_corr_wide_divider        

        screen_width = Window.width
        screen_height = Window.height   
     
        if screen_width * Config.app_wide_scr_mult  > screen_height:#for width/narrow screen, different formulas give good result
            base_font =  self.parent.height *  Config.sfm_wide_fnt_mult 
        else:
            base_font = self.parent.width * Config.sfm_narrow_fnt_mult
            font_corr_divider = Config.sfm_corr_narrow_divider       
   
        font_corrector = len(self.text)/font_corr_divider#this correction helps to display text of different sizes correctly.
        if font_corrector  >  base_font*Config.sfm_max_font_corr:
            font_corrector = base_font *Config.sfm_max_font_corr
            
        font = math.floor(base_font - font_corrector)

        if screen_width < Config.sfm_critical_width:
            font = font*Config.sfm_extra_fnt_mult
         
        self.font_size =  font               
   

class SFMScroll(MDScrollView):
   pass

class SFMAnchor(MDAnchorLayout):
    pass


        
    
   
                
           
        
    
