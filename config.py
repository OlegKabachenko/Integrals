from tools.integration import Integral


class Config:
    @staticmethod
    def normalize_rgb(r, g, b):
        r, g, b = max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))
        return [r / 255, g / 255, b / 255]

    CARD_L_COLOR = normalize_rgb(221, 249, 255)

    ERROR_MSG_BG_COLOR = normalize_rgb(255, 218, 214)

    ROUND_PRECISION = 7
    EXEC_TIME_PRECISION = 5

    I1 = Integral("0", "pi", "cos(z*sin(x)-p*x)", "1/pi")
    I2 = Integral("0", "pi/2", "(x^2+5*x+6)*sin(3*x)")
    I3 = Integral("4", "9", "1/(sqrt(x)-1)")

    INTEGRAL_EXAMPLES: dict[str, Integral | None] = {
        "Ф-ія Бесселя": I1,
        "Приклад 2": I2,
        "Приклад 3": I3,
        "Введення власного інтегралу": None
    }

    APP_WIDE_SCR_MULT = 1.2  #the app window is considered wide when wide*app_wide_scr_mult > height

    DEFAULT_EXAMPLE_ID = 0
    DEFAULT_METHOD_ID = 0

    ANIMATION_DURATION = 0.3

    # ------default values for font size config
    TEXT_LENGTH_CORR_DIV = 1.5
    BASE_FONT_MLT_WIDE = 0.5
    BASE_FONT_MLT_NARROW = 0.07

    # ------for error message widget
    ERR_TEXT_LENGTH_CORR_DIV = 1.2
    ERR_BASE_FONT_MLT_NARROW = 0.067
    HEIGHT_ERR_MSG_MLT = 3.5  # root widget of error message is considered wide when root_width >= root_height*HEIGHT_ERR_MSG_MLT:
    ERR_MSG_WIDE_DIV_ICON = 2  #divider when root widget of error messag is wide(for size of Icons)
    ERR_MSG_NARROW_DIV_ICON = 8  #divider when root widget of error messag is narrow(for size of Icons)
    ERR_ICON_BASE_FONT_MLT_WIDE = 0.9
    ERR_ICON_BASE_FONT_MLT_NARROW = 1

    #------for text in controlbox
    CTRL_BTN_ROOT_WIDTH_MLT = 0.8
    CTRL_BTN_BASE_FONT_MLT = 0.7

    CTRL_LBL_BASE_FONT_MLT_WIDE = 0.8
    CTRL_LBL_BASE_FONT_MLT_NARROW = 0.08

    #------for drop menu
    DROP_MENU_WIDTH_DIV = 1.5
    DROP_MENU_MAX_WIDTH = 700
    DROP_MENU_TEXT_LENGTH_CORR_DIV = 1.4
    DROP_MENU_BASE_FONT_MLT_WIDE = 0.038
    DROP_MENU_BASE_FONT_MLT_NARROW = 0.08

    #------for integral parameters widget
    P_WIDG_BASE_FONT_MLT =0.25
    P_SECTION_HEIGHT = 85
