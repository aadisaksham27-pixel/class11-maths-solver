# ============================================================
# KSHITIJ SCHOOL MATHEMATICS ENGINE
# Classes 8 - 10
# ============================================================

import math
import re
import sympy as sp


# ============================================================
# SYMBOLS
# ============================================================

x, y = sp.symbols("x y")


# ============================================================
# BASIC HELPERS
# ============================================================

def fmt(value):
    """Convert SymPy/numeric values into readable output."""

    try:
        value = sp.simplify(value)

        if value.is_Integer:
            return str(int(value))

        if value.is_Rational:
            return str(value)

        if value.is_Float:
            return f"{float(value):.10g}"

        return str(value)

    except Exception:
        return str(value)


def number(text):
    """Extract a number from text."""

    text = str(text).replace(",", "")

    match = re.search(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )

    if not match:
        raise ValueError("Could not find a number.")

    return float(match.group())


def numbers(text):
    """Extract all numbers."""

    text = str(text).replace(",", "")

    found = re.findall(
        r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)",
        text
    )

    if not found:
        raise ValueError("Could not find numbers.")

    return [float(v) for v in found]


def clean_expression(text):

    text = text.strip()

    replacements = {
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "²": "**2",
        "³": "**3",
        "^": "**",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def pretty(value):
    return fmt(value)


def answer(title, formula, steps, result):

    output = []

    output.append(f"### {title}")
    output.append("")
    output.append(f"**Formula:** {formula}")
    output.append("")

    if steps:
        output.append("**Steps:**")

        for i, step in enumerate(steps, 1):
            output.append(f"{i}. {step}")

        output.append("")

    output.append(f"**Answer:** {pretty(result)}")

    return "\n".join(output)


# ============================================================
# FRACTIONS / RATIONAL NUMBERS
# ============================================================

def solve_fraction(question):

    expression = clean_expression(question)

    # Look for a fraction operation such as:
    # 3/4 + 2/5
    match = re.search(
        r"([-+]?\d+(?:\.\d+)?)\s*/\s*"
        r"([-+]?\d+(?:\.\d+)?)\s*"
        r"([+\-*\/])\s*"
        r"([-+]?\d+(?:\.\d+)?)\s*/\s*"
        r"([-+]?\d+(?:\.\d+)?)",
        expression
    )

    if not match:
        return None

    a, b, op, c, d = match.groups()

    a = sp.Rational(a)
    b = sp.Rational(b)
    c = sp.Rational(c)
    d = sp.Rational(d)

    if b == 0 or d == 0:
        raise ValueError("Denominator cannot be zero.")

    left = a / b
    right = c / d

    if op == "+":
        result = left + right
    elif op == "-":
        result = left - right
    elif op == "*":
        result = left * right
    else:
        if right == 0:
            raise ValueError("Cannot divide by zero.")
        result = left / right

    return answer(
        "Fraction Calculation",
        "Apply the operation to the fractions",
        [
            f"First fraction = {left}",
            f"Second fraction = {right}",
            f"{left} {op} {right} = {result}"
        ],
        result
    )


# ============================================================
# PERCENTAGE
# ============================================================

def solve_percentage(question):

    q = question.lower()

    nums = numbers(question)

    if len(nums) < 2:
        return None

    # x% of y
    if "%" in q and "of" in q:

        percent = nums[0]
        value = nums[1]

        result = percent * value / 100

        return answer(
            "Percentage",
            "(Percentage × Number) / 100",
            [
                f"{percent}% of {value}",
                f"= ({percent} × {value}) / 100"
            ],
            result
        )

    # percentage increase/decrease
    if (
        "increase" in q
        or "decrease" in q
        or "increased" in q
        or "decreased" in q
    ):

        original = nums[0]
        percent = nums[1]

        change = original * percent / 100

        if "decrease" in q or "decreased" in q:
            result = original - change
            operation = "decrease"
        else:
            result = original + change
            operation = "increase"

        return answer(
            "Percentage Change",
            "Change = Original × Percentage / 100",
            [
                f"Change = {original} × {percent} / 100",
                f"Change = {change}",
                f"After {operation} = {result}"
            ],
            result
        )

    return None


# ============================================================
# PROFIT / LOSS / DISCOUNT
# ============================================================

def solve_profit_loss(question):

    q = question.lower()
    nums = numbers(question)

    if len(nums) < 2:
        return None

    if "profit" in q:

        cost = nums[0]
        selling = nums[1]

        profit = selling - cost

        percentage = (
            profit / cost * 100
            if cost != 0 else 0
        )

        return answer(
            "Profit",
            "Profit = SP − CP",
            [
                f"Profit = {selling} − {cost}",
                f"Profit = {profit}",
                f"Profit % = ({profit}/{cost}) × 100"
            ],
            f"{profit} ({percentage:.4g}%)"
        )

    if "loss" in q:

        cost = nums[0]
        selling = nums[1]

        loss = cost - selling

        percentage = (
            loss / cost * 100
            if cost != 0 else 0
        )

        return answer(
            "Loss",
            "Loss = CP − SP",
            [
                f"Loss = {cost} − {selling}",
                f"Loss = {loss}",
                f"Loss % = ({loss}/{cost}) × 100"
            ],
            f"{loss} ({percentage:.4g}%)"
        )

    if "discount" in q:

        marked = nums[0]
        percent = nums[1]

        discount = marked * percent / 100
        selling = marked - discount

        return answer(
            "Discount",
            "Discount = Marked Price × Discount% / 100",
            [
                f"Discount = {marked} × {percent} / 100",
                f"Discount = {discount}",
                f"Selling Price = {marked} − {discount}"
            ],
            selling
        )

    return None


# ============================================================
# SIMPLE INTEREST
# ============================================================

def solve_simple_interest(question):

    q = question.lower()

    if "simple interest" not in q and "si" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 3:
        return None

    p, r, t = nums[:3]

    si = p * r * t / 100
    amount = p + si

    return answer(
        "Simple Interest",
        "SI = P × R × T / 100",
        [
            f"SI = {p} × {r} × {t} / 100",
            f"SI = {si}",
            f"Amount = {p} + {si}"
        ],
        f"SI = {si}, Amount = {amount}"
    )


# ============================================================
# COMPOUND INTEREST
# ============================================================

def solve_compound_interest(question):

    q = question.lower()

    if "compound interest" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 3:
        return None

    p, r, t = nums[:3]

    amount = p * (1 + r / 100) ** t
    ci = amount - p

    return answer(
        "Compound Interest",
        "A = P(1 + R/100)^T",
        [
            f"A = {p}(1 + {r}/100)^{t}",
            f"A = {amount}",
            f"CI = A − P = {ci}"
        ],
        f"CI = {ci}, Amount = {amount}"
    )


# ============================================================
# RATIO
# ============================================================

def solve_ratio(question):

    q = question.lower()

    if "ratio" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 2:
        return None

    a, b = nums[:2]

    if b == 0:
        raise ValueError("Ratio denominator cannot be zero.")

    g = math.gcd(int(abs(a)), int(abs(b)))

    if g == 0:
        result = "0 : 0"
    else:
        result = f"{int(a/g)} : {int(b/g)}"

    return answer(
        "Ratio",
        "Divide both terms by their common factor",
        [
            f"Ratio = {a} : {b}",
            f"Common factor = {g}"
        ],
        result
    )


# ============================================================
# PROPORTION
# ============================================================

def solve_proportion(question):

    q = question.lower()

    if "proportion" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 3:
        return None

    a, b, c = nums[:3]

    if a == 0:
        raise ValueError("Cannot divide by zero.")

    d = b * c / a

    return answer(
        "Proportion",
        "a/b = c/d  →  d = bc/a",
        [
            f"d = ({b} × {c}) / {a}"
        ],
        d
    )


# ============================================================
# LINEAR EQUATION
# ============================================================

def solve_linear_equation(question):

    if "=" not in question:
        return None

    q = question.lower()

    # Avoid stealing coordinate or systems questions.
    if "coordinate" in q:
        return None

    expression = clean_expression(question)

    # Keep likely equation content.
    match = re.search(
        r"([0-9xX+\-*/().\s]+=[0-9xX+\-*/().\s]+)",
        expression
    )

    if not match:
        return None

    eq = match.group(1)

    try:

        left, right = eq.split("=", 1)

        left_expr = sp.sympify(
            left.replace("X", "x")
        )

        right_expr = sp.sympify(
            right.replace("X", "x")
        )

        equation = sp.Eq(
            left_expr,
            right_expr
        )

        solution = sp.solve(
            equation,
            x
        )

        if not solution:
            return answer(
                "Linear Equation",
                "Solve both sides for x",
                ["No value of x satisfies the equation."],
                "No solution"
            )

        return answer(
            "Linear Equation",
            "Move terms and isolate x",
            [
                f"Equation: {eq}",
                f"x = {solution[0]}"
            ],
            solution[0]
        )

    except Exception:
        return None


# ============================================================
# TWO LINEAR EQUATIONS
# ============================================================

def solve_two_linear_equations(question):

    q = question.lower()

    if (
        "simultaneous" not in q
        and "pair of linear" not in q
        and "equations" not in q
    ):
        return None

    matches = re.findall(
        r"([+-]?\d*x(?:\s*[+-]\s*\d*y)?\s*=\s*[+-]?\d+)",
        question.lower()
    )

    if len(matches) < 2:
        return None

    try:

        equations = []

        for text in matches[:2]:

            left, right = text.split("=")

            equations.append(
                sp.Eq(
                    sp.sympify(left),
                    sp.sympify(right)
                )
            )

        solution = sp.solve(
            equations,
            (x, y),
            dict=True
        )

        if not solution:
            return answer(
                "Pair of Linear Equations",
                "Solve the two equations simultaneously",
                [],
                "No unique solution"
            )

        result = solution[0]

        return answer(
            "Pair of Linear Equations",
            "Solve both equations simultaneously",
            [
                f"x = {result.get(x)}",
                f"y = {result.get(y)}"
            ],
            f"x = {result.get(x)}, y = {result.get(y)}"
        )

    except Exception:
        return None


# ============================================================
# POLYNOMIAL
# ============================================================

def solve_polynomial(question):

    q = question.lower()

    if (
        "polynomial" not in q
        and "factorise" not in q
        and "factorize" not in q
        and "expand" not in q
    ):
        return None

    expression = clean_expression(question)

    # Try extracting expression after common words.
    expression = re.sub(
        r"^(expand|factorise|factorize|factor|simplify)\s+",
        "",
        expression,
        flags=re.I
    )

    expression = expression.replace("=", "")

    try:

        expr = sp.sympify(expression)

        if "factor" in q:
            result = sp.factor(expr)

            return answer(
                "Polynomial Factorisation",
                "Factorise the polynomial",
                [f"{expr} = {result}"],
                result
            )

        if "expand" in q:
            result = sp.expand(expr)

            return answer(
                "Polynomial Expansion",
                "Expand and simplify",
                [f"{expr} = {result}"],
                result
            )

        result = sp.simplify(expr)

        return answer(
            "Polynomial",
            "Simplify the expression",
            [f"{expr} = {result}"],
            result
        )

    except Exception:
        return None


# ============================================================
# ALGEBRAIC IDENTITIES
# ============================================================

def solve_identity(question):

    q = question.lower()

    if "identity" not in q:
        return None

    expression = clean_expression(question)

    try:

        expr = sp.sympify(
            expression.replace("=", "")
        )

        expanded = sp.expand(expr)

        return answer(
            "Algebraic Identity",
            "(a+b)² = a² + 2ab + b² and related identities",
            [
                f"Original expression: {expr}",
                f"Expanded form: {expanded}"
            ],
            expanded
        )

    except Exception:
        return None


# ============================================================
# EXPONENTS
# ============================================================

def solve_exponents(question):

    q = question.lower()

    if not any(
        word in q
        for word in [
            "exponent",
            "power",
            "indices"
        ]
    ):
        return None

    expression = clean_expression(question)

    try:

        expr = sp.sympify(expression)

        result = sp.powsimp(
            expr,
            force=True
        )

        return answer(
            "Exponents and Powers",
            "Use laws of exponents",
            [
                f"Original: {expr}",
                f"Simplified: {result}"
            ],
            result
        )

    except Exception:
        return None


# ============================================================
# SQUARE ROOT / CUBE ROOT
# ============================================================

def solve_roots(question):

    q = question.lower()

    if (
        "square root" not in q
        and "sqrt" not in q
        and "cube root" not in q
    ):
        return None

    nums = numbers(question)

    if not nums:
        return None

    n = nums[0]

    if "cube root" in q:

        result = math.copysign(
            abs(n) ** (1 / 3),
            n
        )

        return answer(
            "Cube Root",
            "∛n",
            [f"∛{n} = {result}"],
            result
        )

    if n < 0:
        return None

    result = math.sqrt(n)

    return answer(
        "Square Root",
        "√n",
        [f"√{n} = {result}"],
        result
    )


# ============================================================
# SEQUENCE / AP
# ============================================================

def solve_sequence_school(question):

    q = question.lower()

    if not any(
        word in q
        for word in [
            "sequence",
            "arithmetic progression",
            "ap",
            "nth term"
        ]
    ):
        return None

    nums = numbers(question)

    if len(nums) < 2:
        return None

    a = nums[0]
    d = nums[1]

    # If question explicitly asks nth term
    if "nth" in q:

        n = nums[-1]

        term = a + (n - 1) * d

        return answer(
            "Arithmetic Progression",
            "aₙ = a + (n − 1)d",
            [
                f"a = {a}",
                f"d = {d}",
                f"n = {n}",
                f"aₙ = {a} + ({n} − 1) × {d}"
            ],
            term
        )

    return answer(
        "Arithmetic Progression",
        "aₙ = a + (n − 1)d",
        [
            f"First term a = {a}",
            f"Common difference d = {d}"
        ],
        f"aₙ = {a} + (n − 1)({d})"
    )


# ============================================================
# COORDINATE DISTANCE
# ============================================================

def solve_coordinate(question):

    q = question.lower()

    if (
        "coordinate" not in q
        and "distance between" not in q
    ):
        return None

    nums = numbers(question)

    if len(nums) < 4:
        return None

    x1, y1, x2, y2 = nums[:4]

    distance = math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

    return answer(
        "Coordinate Geometry",
        "d = √[(x₂−x₁)² + (y₂−y₁)²]",
        [
            f"Points: ({x1}, {y1}) and ({x2}, {y2})",
            f"d = √[({x2}−{x1})² + ({y2}−{y1})²]"
        ],
        distance
    )


# ============================================================
# MIDPOINT
# ============================================================

def solve_midpoint(question):

    q = question.lower()

    if "midpoint" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 4:
        return None

    x1, y1, x2, y2 = nums[:4]

    mx = (x1 + x2) / 2
    my = (y1 + y2) / 2

    return answer(
        "Midpoint",
        "M = ((x₁+x₂)/2, (y₁+y₂)/2)",
        [
            f"x-coordinate = ({x1}+{x2})/2",
            f"y-coordinate = ({y1}+{y2})/2"
        ],
        f"({mx}, {my})"
    )


# ============================================================
# STATISTICS
# ============================================================

def solve_statistics_school(question):

    q = question.lower()

    if not any(
        word in q
        for word in [
            "mean",
            "median",
            "mode",
            "average",
            "statistics"
        ]
    ):
        return None

    nums = numbers(question)

    if not nums:
        return None

    if "median" in q:

        data = sorted(nums)

        n = len(data)

        if n % 2:
            result = data[n // 2]
        else:
            result = (
                data[n // 2 - 1] +
                data[n // 2]
            ) / 2

        return answer(
            "Median",
            "Arrange data and find the middle value",
            [
                f"Ordered data = {data}"
            ],
            result
        )

    if "mode" in q:

        from collections import Counter

        counts = Counter(nums)

        highest = max(
            counts.values()
        )

        modes = [
            k for k, v in counts.items()
            if v == highest
        ]

        return answer(
            "Mode",
            "Most frequently occurring value",
            [
                f"Frequencies = {dict(counts)}"
            ],
            modes
        )

    result = sum(nums) / len(nums)

    return answer(
        "Mean",
        "Mean = Sum of observations / Number of observations",
        [
            f"Sum = {sum(nums)}",
            f"Number of observations = {len(nums)}"
        ],
        result
    )


# ============================================================
# PROBABILITY
# ============================================================

def solve_probability_school(question):

    q = question.lower()

    if "probability" not in q:
        return None

    nums = numbers(question)

    if len(nums) < 2:
        return None

    favorable = nums[0]
    total = nums[1]

    if total == 0:
        raise ValueError(
            "Total number of outcomes cannot be zero."
        )

    result = favorable / total

    return answer(
        "Probability",
        "P(E) = Favorable outcomes / Total outcomes",
        [
            f"Favorable outcomes = {favorable}",
            f"Total outcomes = {total}",
            f"P(E) = {favorable}/{total}"
        ],
        result
    )


# ============================================================
# GEOMETRY
# ============================================================

def solve_geometry(question):

    q = question.lower()

    nums = numbers(question)

    if not nums:
        return None

    # Rectangle
    if "rectangle" in q:

        if len(nums) < 2:
            return None

        length, width = nums[:2]

        area = length * width
        perimeter = 2 * (length + width)

        if "perimeter" in q:
            result = perimeter
            formula = "P = 2(l + w)"
        else:
            result = area
            formula = "A = l × w"

        return answer(
            "Rectangle",
            formula,
            [
                f"Length = {length}",
                f"Width = {width}"
            ],
            result
        )

    # Square
    if "square" in q:

        side = nums[0]

        if "perimeter" in q:
            result = 4 * side
            formula = "P = 4a"
        else:
            result = side ** 2
            formula = "A = a²"

        return answer(
            "Square",
            formula,
            [f"Side = {side}"],
            result
        )

    # Triangle
    if "triangle" in q:

        if len(nums) < 2:
            return None

        base = nums[0]
        height = nums[1]

        area = 0.5 * base * height

        return answer(
            "Triangle",
            "A = 1/2 × base × height",
            [
                f"Base = {base}",
                f"Height = {height}"
            ],
            area
        )

    # Circle
    if "circle" in q:

        radius = nums[0]

        if radius < 0:
            raise ValueError(
                "Radius cannot be negative."
            )

        if "circumference" in q:
            result = 2 * math.pi * radius
            formula = "C = 2πr"
        else:
            result = math.pi * radius ** 2
            formula = "A = πr²"

        return answer(
            "Circle",
            formula,
            [
                f"Radius = {radius}"
            ],
            result
        )

    return None


# ============================================================
# MENSURATION
# ============================================================

def solve_mensuration(question):

    q = question.lower()

    nums = numbers(question)

    if not nums:
        return None

    # Cuboid
    if "cuboid" in q:

        if len(nums) < 3:
            return None

        l, b, h = nums[:3]

        volume = l * b * h
        surface = 2 * (
            l*b + b*h + h*l
        )

        if "surface" in q:
            result = surface
            formula = "TSA = 2(lb + bh + hl)"
        else:
            result = volume
            formula = "V = lbh"

        return answer(
            "Cuboid",
            formula,
            [
                f"l = {l}",
                f"b = {b}",
                f"h = {h}"
            ],
            result
        )

    # Cube
    if "cube" in q:

        side = nums[0]

        if "surface" in q:
            result = 6 * side ** 2
            formula = "TSA = 6a²"
        else:
            result = side ** 3
            formula = "V = a³"

        return answer(
            "Cube",
            formula,
            [f"Side = {side}"],
            result
        )

    # Cylinder
    if "cylinder" in q:

        if len(nums) < 2:
            return None

        r, h = nums[:2]

        volume = math.pi * r ** 2 * h

        return answer(
            "Cylinder",
            "V = πr²h",
            [
                f"Radius = {r}",
                f"Height = {h}"
            ],
            volume
        )

    # Sphere
    if "sphere" in q:

        r = nums[0]

        volume = (
            4 / 3
            * math.pi
            * r ** 3
        )

        return answer(
            "Sphere",
            "V = 4/3 πr³",
            [f"Radius = {r}"],
            volume
        )

    return None


# ============================================================
# PYTHAGORAS
# ============================================================

def solve_pythagoras(question):

    q = question.lower()

    if (
        "pythagoras" not in q
        and "hypotenuse" not in q
    ):
        return None

    nums = numbers(question)

    if len(nums) < 2:
        return None

    a, b = nums[:2]

    result = math.sqrt(
        a ** 2 + b ** 2
    )

    return answer(
        "Pythagoras Theorem",
        "c² = a² + b²",
        [
            f"c² = {a}² + {b}²",
            f"c² = {a**2 + b**2}"
        ],
        result
    )


# ============================================================
# BASIC TRIGONOMETRY
# ============================================================

def solve_trigonometry_school(question):

    q = question.lower()

    if not any(
        word in q
        for word in [
            "sin",
            "cos",
            "tan",
            "sine",
            "cosine",
            "tangent"
        ]
    ):
        return None

    nums = numbers(question)

    if not nums:
        return None

    angle = nums[0]

    radians = math.radians(angle)

    if "sin" in q or "sine" in q:
        result = math.sin(radians)
        function = "sin"

    elif "cos" in q or "cosine" in q:
        result = math.cos(radians)
        function = "cos"

    else:
        result = math.tan(radians)
        function = "tan"

    return answer(
        "Trigonometry",
        f"{function}(θ)",
        [
            f"θ = {angle}°",
            f"{function}({angle}°) = {result}"
        ],
        result
    )


# ============================================================
# QUADRATIC EQUATION
# ============================================================

def solve_quadratic_school(question):

    if "=" not in question:
        return None

    q = question.lower()

    if (
        "quadratic" not in q
        and "roots" not in q
        and "solve" not in q
    ):
        return None

    expression = clean_expression(question)

    try:

        if "=" in expression:

            left, right = expression.split(
                "=",
                1
            )

            expr = (
                sp.sympify(left)
                - sp.sympify(right)
            )

        else:
            expr = sp.sympify(expression)

        poly = sp.Poly(
            expr,
            x
        )

        if poly.degree() != 2:
            return None

        roots = sp.solve(
            expr,
            x
        )

        return answer(
            "Quadratic Equation",
            "ax² + bx + c = 0",
            [
                f"Equation: {sp.Eq(expr, 0)}",
                f"Roots: {roots}"
            ],
            roots
        )

    except Exception:
        return None


# ============================================================
# REAL NUMBERS / HCF / LCM
# ============================================================

def solve_hcf_lcm(question):

    q = question.lower()

    if (
        "hcf" not in q
        and "gcd" not in q
        and "lcm" not in q
    ):
        return None

    nums = numbers(question)

    if len(nums) < 2:
        return None

    values = [
        int(n)
        for n in nums
    ]

    if "hcf" in q or "gcd" in q:

        result = values[0]

        for value in values[1:]:
            result = math.gcd(
                result,
                value
            )

        return answer(
            "HCF",
            "Highest common factor",
            [
                f"Numbers = {values}"
            ],
            result
        )

    result = values[0]

    for value in values[1:]:
        result = math.lcm(
            result,
            value
        )

    return answer(
        "LCM",
        "Least common multiple",
        [
            f"Numbers = {values}"
        ],
        result
    )


# ============================================================
# GENERAL EXPRESSION
# ============================================================

def solve_expression(question):

    expression = clean_expression(
        question
    )

    # Remove common instructional words.
    expression = re.sub(
        r"^(calculate|find|solve|evaluate|simplify)\s+",
        "",
        expression,
        flags=re.I
    )

    try:

        expr = sp.sympify(
            expression
        )

        result = sp.simplify(
            expr
        )

        return answer(
            "Mathematical Expression",
            "Evaluate and simplify the expression",
            [
                f"Expression = {expr}",
                f"Simplified = {result}"
            ],
            result
        )

    except Exception:
        return None


# ============================================================
# MAIN SCHOOL MATH ROUTER
# ============================================================

def solve_school_math(
    question,
    chapter="Auto Detect"
):

    if not question or not question.strip():
        return "Please enter a question."

    q = question.lower()

    # Most specific systems first.
    engines = [

        solve_compound_interest,
        solve_simple_interest,

        solve_two_linear_equations,
        solve_quadratic_school,

        solve_profit_loss,
        solve_percentage,

        solve_hcf_lcm,

        solve_coordinate,
        solve_midpoint,

        solve_pythagoras,

        solve_mensuration,
        solve_geometry,

        solve_probability_school,
        solve_statistics_school,

        solve_sequence_school,

        solve_ratio,
        solve_proportion,

        solve_roots,
        solve_exponents,

        solve_identity,
        solve_polynomial,

        solve_fraction,

        solve_trigonometry_school,

        solve_linear_equation,

    ]

    for engine in engines:

        try:

            result = engine(question)

            if result is not None:
                return result

        except Exception as error:

            return f"Unable to solve this question: {error}"

    # Last attempt:
    try:
        result = solve_expression(
            question
        )

        if result is not None:
            return result

    except Exception:
        pass

    return (
        "I could not confidently solve this question yet. "
        "Try writing the question with the numbers, "
        "equation, or required values clearly."
    )


# ============================================================
# CHAPTER SUPPORT
# ============================================================

SCHOOL_MATH_CHAPTERS = {

    # Class 8
    "Rational Numbers",
    "Linear Equations in One Variable",
    "Understanding Quadrilaterals",
    "Practical Geometry",
    "Data Handling",
    "Squares and Square Roots",
    "Cubes and Cube Roots",
    "Comparing Quantities",
    "Algebraic Expressions and Identities",
    "Visualising Solid Shapes",
    "Exponents and Powers",
    "Direct and Inverse Proportions",
    "Factorisation",
    "Introduction to Graphs",
    "Mensuration",

    # Class 9
    "Number System",
    "Introduction to Polynomials",
    "Sequences and Progressions",
    "Exploring Algebraic Identities",
    "Linear Equations in Two Variables",
    "Coordinate Geometry",
    "Introduction to Euclid's Geometry: Axioms and Postulates",
    "Lines and Angles",
    "Triangles - Congruence Theorems",
    "4-gons (Quadrilaterals)",
    "Circles",
    "Area and Perimeter",
    "Surface Area and Volume",
    "Statistics",
    "Introduction to Probability",

    # Class 10
    "Real Numbers",
    "Polynomials",
    "Pair of Linear Equations in Two Variables",
    "Quadratic Equations",
    "Arithmetic Progressions",
    "Coordinate Geometry",
    "Triangles",
    "Circles",
    "Introduction to Trigonometry",
    "Some Applications of Trigonometry",
    "Areas Related to Circles",
    "Surface Areas and Volumes",
    "Statistics",
    "Probability",
}


def is_school_math_chapter(chapter):

    return chapter in SCHOOL_MATH_CHAPTERS