from tools.integration import Integral


class Config:
    CARD_L_COLOR = [0.867, 0.98, 1]

    ROUND_PRECISION = 7
    EXEC_TIME_PRECISION = 5

    I1 = Integral("0", "pi", "cos(z*sin(x)-p*x)", "1/pi")
    I2 = Integral("0", "pi/2", "(x^2+5*x+6)*sin(3*x)")
    I3 = Integral("0", "2", "exp(-x^2)")

    INTEGRAL_EXAMPLES: dict[str, Integral | None] = {
        "Ф-ія Бесселя": I1,
        "Приклад 2": I2,
        "Приклад 3": I3,
        "Введення власного інтегралу": None
    }

    DEFAULT_EXAMPLE_ID = 0
    DEFAULT_METHOD_ID = 0

    ANIMATION_DURATION = 0.3
