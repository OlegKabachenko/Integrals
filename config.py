from tools.integration import Integral
import threading

class Config():
             
    @staticmethod               
    def normalize_rgb (r, g, b): 
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        return [r/255, g/255, b/255]

    card_l_color = normalize_rgb(221, 249, 255) 
    
    i1 = Integral(0, "pi", "cos(z*sin(x) - p*x)")
    i2 = Integral(0, "pi/2", "(x^2+5*x+6)*sin(3*x)")
    i3 = Integral(4, 9, "1/(sqrt(x)-1)")
        
    integral_examples = {
            "Приклад 1": i1,
            "Приклад 2": i2,
            "Приклад 3": i3,
            "Введення власного інтегралу": None
    }
    
    app_wide_scr_mult = 1.2 #the app window is considered wide when wide*app_wide_scr_mult > height

    #------for text in select formula/method area
    sfm_narrow_fnt_mult = 0.08#font multiplier when app window is narrow
    sfm_wide_fnt_mult = 0.65 #font multiplier when app window is wide

    sfm_critical_width = 360 #size that is considered very narrow
    sfm_extra_fnt_mult = 1.4 #multiplayer to increase font size when application window is too narrow
    
    sfm_max_font_corr = 0.5 # the maximum % of the base font that the font_corrector can be equal to
        
    sfm_corr_wide_divider = 2.5#font correction divider when app window is wide
    sfm_corr_narrow_divider = 6#font correction divider when app window is narrow

    #------for drop menu
    menu_item_narrow_fnt_mult = 25#font multiplier when app window is narrow(for items in dropmenu)
    menu_item_wide_fnt_mult = 20 #font multiplier when app window is wide(for items in dropmenu)

    #------for integral parameters layout
    p_widg_wide_item_mult = 2 #widget of integral parameter is considered  wide when width*p_widg_wide_item_mult > height
    p_font_wide_wid_mult = 0.3 #used when calculating font size for integral parameter widget when parent widget is wide       
    p_font_narrow_wid_mult = 7  #used when calculating font size for integral parameter widget when parent widget is narrow
    p_section_height = 80
    p_section_wide_scr_mult = 1 #used to select the appropriate orientation for parameter section 


    
