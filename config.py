from tools.integration import Integral


class Config:
    @staticmethod
    def normalize_rgb(r, g, b):
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        return [r / 255, g / 255, b / 255]

    CARD_L_COLOR = normalize_rgb(221, 249, 255)

    I1 = Integral(0, "pi", "cos(z*sin(x) - p*x)")
    I2 = Integral(0, "pi/2", "(x^2+5*x+6)*sin(3*x)")
    I3 = Integral(4, 9, "1/(sqrt(x)-1)")

    INTEGRAL_EXAMPLES = {
        "Приклад 1": I1,
        "Приклад 2": I2,
        "Приклад 3": I3,
        "Введення власного інтегралу": None
    }

    APP_WIDE_SCR_MULT = 1.2  #the app window is considered wide when wide*app_wide_scr_mult > height

    DEFAULT_EXAMPLE_ID = 0
    DEFAULT_METHOD_ID = 0

    #------for text in select formula/method area
    SFM_NARROW_FNT_MULT = 0.08  #font multiplier when app window is narrow
    SFM_WIDE_FNT_MULT = 0.65  #font multiplier when app window is wide

    SFM_CRITICAL_WIDTH = 360  #size that is considered very narrow
    SFM_EXTRA_FNT_MULT = 1.4  #multiplayer to increase font size when application window is too narrow

    SFM_MAX_FONT_CORR = 0.5  # the maximum % of the base font that the font_corrector can be equal to

    SFM_CORR_WIDE_DIVIDER = 2.5  #font correction divider when app window is wide
    SFM_CORR_NARROW_DIVIDER = 6  #font correction divider when app window is narrow

    #------for drop menu
    MENU_ITEM_NARROW_FNT_MULT = 25  #font multiplier when app window is narrow(for items in drop menu)
    MENU_ITEM_WIDE_FNT_MULT = 20  #font multiplier when app window is wide(for items in drop menu)

    #------for integral parameters layout
    P_WIDG_WIDE_ITEM_MULT = 2  #widget of integral parameter is considered  wide when width*p_widg_wide_item_mult > height
    P_FONT_WIDE_WID_MULT = 0.3  #used when calculating font size for integral parameter widget when parent widget is wide
    P_FONT_NARROW_WID_MULT = 7  #used when calculating font size for integral parameter widget when parent widget is narrow
    P_SECTION_HEIGHT = 85
    P_SECTION_WIDE_SCR_MULT = 1  #used to select the appropriate orientation for parameter section
