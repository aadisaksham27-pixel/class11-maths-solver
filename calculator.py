import math
import re


# ============================================================
# SAFE FUNCTIONS
# ============================================================

SAFE_FUNCTIONS = {
    # Roots
    "sqrt": math.sqrt,
    "cbrt": lambda x: math.copysign(abs(x) ** (1 / 3), x),

    # Trigonometry - radians
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,

    # Inverse trigonometry
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,

    # Trigonometry - degrees
    "sind": lambda x: math.sin(math.radians(x)),
    "cosd": lambda x: math.cos(math.radians(x)),
    "tand": lambda x: math.tan(math.radians(x)),

    # Logs
    "log": math.log10,
    "ln": math.log,

    # Exponential
    "exp": math.exp,

    # General
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,

    # Factorial
    "factorial": math.factorial,
}


# ============================================================
# SAFE CONSTANTS
# ============================================================

SAFE_VALUES = {
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


# ============================================================
# MAIN CALCULATOR
# ============================================================

def calculate(expression):

    if not isinstance(expression, str):
        raise ValueError("Expression must be text.")

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression is empty.")

    # --------------------------------------------------------
    # Normalize mathematical symbols
    # --------------------------------------------------------

    expression = expression.replace("π", "pi")
    expression = expression.replace("τ", "tau")

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    expression = expression.replace("−", "-")
    expression = expression.replace("–", "-")

    expression = expression.replace("^", "**")

    # Square-root symbol
    expression = replace_square_roots(expression)

    # Percentage
    expression = convert_percentages(expression)

    # Factorial notation
    expression = convert_factorials(expression)

    # Combinations / permutations
    expression = convert_combinations(expression)

    # --------------------------------------------------------
    # Insert implicit multiplication
    # --------------------------------------------------------

    expression = insert_implicit_multiplication(expression)

    # --------------------------------------------------------
    # Safety check
    # --------------------------------------------------------

    if not re.fullmatch(
        r"[0-9a-zA-Z_+\-*/().,\s*]+",
        expression
    ):
        raise ValueError(
            "Expression contains unsupported characters."
        )

    # --------------------------------------------------------
    # Restricted evaluation environment
    # --------------------------------------------------------

    environment = {
        "__builtins__": {}
    }

    environment.update(SAFE_FUNCTIONS)
    environment.update(SAFE_VALUES)

    # Advanced combinatorics
    environment["ncr"] = ncr
    environment["npr"] = npr

    # --------------------------------------------------------
    # Calculate
    # --------------------------------------------------------

    try:

        result = eval(
            expression,
            environment,
            {}
        )

    except ZeroDivisionError:

        raise ValueError(
            "Cannot divide by zero."
        )

    except ValueError:

        raise ValueError(
            "Invalid mathematical value."
        )

    except OverflowError:

        raise ValueError(
            "The number is too large."
        )

    except Exception:

        raise ValueError(
            "Could not calculate this expression."
        )

    # --------------------------------------------------------
    # Validate result
    # --------------------------------------------------------

    if isinstance(result, complex):

        return format_complex(result)

    try:

        numeric_result = float(result)

    except Exception:

        raise ValueError(
            "Calculation did not produce a valid number."
        )

    if not math.isfinite(numeric_result):

        raise ValueError(
            "Result is not finite."
        )

    return format_number(result)


# ============================================================
# SQUARE ROOT SUPPORT
# ============================================================

def replace_square_roots(expression):

    # √(x) -> sqrt(x)
    expression = re.sub(
        r"√\s*\(",
        "sqrt(",
        expression
    )

    # √144 -> sqrt(144)
    expression = re.sub(
        r"√\s*([0-9]+(?:\.[0-9]+)?)",
        r"sqrt(\1)",
        expression
    )

    return expression


# ============================================================
# PERCENTAGE SUPPORT
# ============================================================

def convert_percentages(expression):

    # 50% -> (50/100)
    expression = re.sub(
        r"(\d+(?:\.\d+)?)\s*%",
        r"(\1/100)",
        expression
    )

    return expression


# ============================================================
# FACTORIAL SUPPORT
# ============================================================

def convert_factorials(expression):

    # 5! -> factorial(5)
    expression = re.sub(
        r"(\d+(?:\.\d+)?)!",
        r"factorial(\1)",
        expression
    )

    # (5)! -> factorial((5))
    expression = re.sub(
        r"(\([^()]+\))!",
        r"factorial\1",
        expression
    )

    return expression


# ============================================================
# COMBINATIONS / PERMUTATIONS
# ============================================================

def convert_combinations(expression):

    # 10C3 -> ncr(10,3)
    expression = re.sub(
        r"(\d+)\s*[cC]\s*(\d+)",
        r"ncr(\1,\2)",
        expression
    )

    # 10P3 -> npr(10,3)
    expression = re.sub(
        r"(\d+)\s*[pP]\s*(\d+)",
        r"npr(\1,\2)",
        expression
    )

    return expression


# ============================================================
# IMPLICIT MULTIPLICATION
# ============================================================

def insert_implicit_multiplication(expression):

    # Number followed by a constant/function
    #
    # 2pi       -> 2*pi
    # 3sqrt(9)  -> 3*sqrt(9)
    # 2sin(30)  -> 2*sin(30)
    expression = re.sub(
        r"(\d)(?=(pi|tau|e|sqrt|cbrt|sin|cos|tan|asin|acos|atan|sind|cosd|tand|log|ln|exp|abs|floor|ceil|factorial|ncr|npr))",
        r"\1*",
        expression
    )

    # Closing parenthesis followed by a number/letter
    #
    # (2+3)4 -> (2+3)*4
    expression = re.sub(
        r"(\))(?=[0-9a-zA-Z])",
        r"\1*",
        expression
    )

    # Number followed by opening parenthesis
    #
    # 2(3+4) -> 2*(3+4)
    expression = re.sub(
        r"(\d)\s*(?=\()",
        r"\1*",
        expression
    )

    # Constant followed by opening parenthesis
    #
    # pi(2) -> pi*(2)
    expression = re.sub(
        r"(pi|tau|e)\s*(?=\()",
        r"\1*",
        expression
    )

    # Closing parenthesis followed by opening parenthesis
    #
    # (2)(3) -> (2)*(3)
    expression = re.sub(
        r"\)\s*(?=\()",
        ")*",
        expression
    )

    return expression


# ============================================================
# NUMBER FORMATTING
# ============================================================

def format_number(value):

    value = float(value)

    # Prevent displaying -0
    if abs(value) < 1e-12:
        value = 0.0

    # Integer
    if value.is_integer():

        return str(int(value))

    # Normal decimal
    return f"{value:.10g}"


# ============================================================
# COMPLEX NUMBER FORMATTING
# ============================================================

def format_complex(value):

    real = value.real
    imag = value.imag

    if abs(real) < 1e-12:
        real = 0

    if abs(imag) < 1e-12:
        imag = 0

    # Pure real
    if imag == 0:

        return format_number(real)

    # Pure imaginary
    if real == 0:

        return f"{format_number(imag)}i"

    # Complex
    sign = "+" if imag >= 0 else "-"

    return (
        f"{format_number(real)} "
        f"{sign} "
        f"{format_number(abs(imag))}i"
    )


# ============================================================
# COMBINATION
# nCr
# ============================================================

def ncr(n, r):

    if not float(n).is_integer() or not float(r).is_integer():

        raise ValueError(
            "nCr requires whole numbers."
        )

    n = int(n)
    r = int(r)

    if n < 0 or r < 0:

        raise ValueError(
            "nCr requires non-negative numbers."
        )

    if r > n:

        raise ValueError(
            "In nCr, r cannot be greater than n."
        )

    return math.comb(n, r)


# ============================================================
# PERMUTATION
# nPr
# ============================================================

def npr(n, r):

    if not float(n).is_integer() or not float(r).is_integer():

        raise ValueError(
            "nPr requires whole numbers."
        )

    n = int(n)
    r = int(r)

    if n < 0 or r < 0:

        raise ValueError(
            "nPr requires non-negative numbers."
        )

    if r > n:

        raise ValueError(
            "In nPr, r cannot be greater than n."
        )

    return math.perm(n, r)