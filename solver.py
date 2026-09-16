import sympy as sp
import math
import re
from collections import Counter

x, y, z = sp.symbols("x y z")


# ============================================================
# BASIC HELPERS
# ============================================================

def clean(text):
    text = text.strip()

    replacements = {
        "²": "^2",
        "³": "^3",
        "⁴": "^4",
        "⁵": "^5",
        "×": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "π": "pi",
        "∞": "oo",
        "√": "sqrt",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("^", "**")

    # 2x -> 2*x
    text = re.sub(r"(\d)\s*x", r"\1*x", text)

    return text


def expression(text):
    return sp.sympify(
        clean(text),
        locals={
            "x": x,
            "y": y,
            "z": z,
            "pi": sp.pi,
            "sqrt": sp.sqrt,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "cot": sp.cot,
            "sec": sp.sec,
            "csc": sp.csc,
            "log": sp.log,
            "ln": sp.log,
        },
    )


def pretty(value):
    return sp.pretty(sp.simplify(value), use_unicode=True)


# ============================================================
# CHAPTER DETECTION
# ============================================================

def detect_chapter(question):

    q = question.lower()

    keywords = [
        ("Sets", [
            "set", "union", "intersection",
            "subset", "complement", "venn"
        ]),

        ("Relations & Functions", [
            "function", "domain", "range",
            "relation", "mapping", "one-one", "onto"
        ]),

        ("Trigonometric Functions", [
            "sin", "cos", "tan", "cot",
            "sec", "cosec", "csc",
            "trigonometric", "trigonometry"
        ]),

        ("Complex Numbers & Quadratic Equations", [
            "complex", "imaginary",
            "quadratic", "discriminant",
            "roots of equation"
        ]),

        ("Linear Inequalities", [
            "inequality", "inequalities"
        ]),

        ("Permutations & Combinations", [
            "permutation", "combination",
            "factorial", "arrange", "arrangements"
        ]),

        ("Binomial Theorem", [
            "binomial", "coefficient"
        ]),

        ("Sequences & Series", [
            "ap", "a.p", "arithmetic progression",
            "gp", "g.p", "geometric progression",
            "sequence", "series", "nth term"
        ]),

        ("Straight Lines", [
            "straight line", "slope",
            "gradient", "equation of line",
            "distance between points"
        ]),

        ("Conic Sections", [
            "circle", "parabola",
            "ellipse", "hyperbola", "conic"
        ]),

        ("3D Geometry", [
            "3d", "three dimensional",
            "three-dimensional", "point in space"
        ]),

        ("Limits & Derivatives", [
            "limit", "derivative",
            "differentiate", "differentiation"
        ]),

        ("Statistics", [
            "mean", "median", "mode",
            "variance", "standard deviation",
            "statistics"
        ]),

        ("Probability", [
            "probability", "sample space",
            "event", "outcome"
        ]),
    ]

    for chapter, words in keywords:
        for word in words:
            if word in q:
                return chapter

    return "General Algebra"


# ============================================================
# SETS
# ============================================================

def solve_sets(q):

    numbers = [
        int(v) for v in re.findall(r"\b\d+\b", q)
    ]

    if (
        "union" in q.lower()
        and "intersection" in q.lower()
        and len(numbers) >= 3
    ):

        a, b, ab = numbers[:3]

        answer = a + b - ab

        return (
            "SETS\n\n"
            "Formula:\n"
            "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)\n\n"
            f"n(A ∪ B) = {a} + {b} − {ab}\n\n"
            f"Answer:\n{answer}"
        )

    return (
        "SETS\n\n"
        "Try a question involving:\n"
        "• Union\n"
        "• Intersection\n"
        "• Subsets\n"
        "• Complement\n"
        "• Venn diagrams"
    )


# ============================================================
# FUNCTIONS
# ============================================================

def solve_functions(q):

    match = re.search(
        r"f\s*\(\s*x\s*\)\s*=\s*(.+)",
        clean(q),
        re.IGNORECASE
    )

    if match:

        try:

            expr = expression(match.group(1))

            return (
                "RELATIONS & FUNCTIONS\n\n"
                f"Given:\n"
                f"f(x) = {pretty(expr)}\n\n"
                f"Simplified:\n"
                f"f(x) = {pretty(sp.simplify(expr))}"
            )

        except:
            pass

    return (
        "RELATIONS & FUNCTIONS\n\n"
        "Example:\n"
        "f(x) = x² + 2x + 1"
    )


# ============================================================
# TRIGONOMETRY
# ============================================================

def solve_trigonometry(q):

    try:

        expr = expression(q)

        answer = sp.trigsimp(expr)

        return (
            "TRIGONOMETRIC FUNCTIONS\n\n"
            f"Expression:\n{pretty(expr)}\n\n"
            "After trigonometric simplification:\n"
            f"{pretty(answer)}\n\n"
            f"Answer:\n{pretty(answer)}"
        )

    except:

        return (
            "TRIGONOMETRIC FUNCTIONS\n\n"
            "Try:\n"
            "sin(pi/6)\n"
            "cos(pi/3)\n"
            "sin(x)^2 + cos(x)^2"
        )


# ============================================================
# QUADRATIC EQUATIONS
# ============================================================

def solve_quadratic(q):

    try:

        text = clean(q)

        if "=" in text:

            left, right = text.split("=", 1)

            equation = sp.Eq(
                expression(left),
                expression(right)
            )

            roots = sp.solve(equation, x)

        else:

            expr = expression(text)

            roots = sp.solve(
                sp.Eq(expr, 0),
                x
            )

        return (
            "COMPLEX NUMBERS & QUADRATIC EQUATIONS\n\n"
            f"Equation:\n{q}\n\n"
            "Solving for x:\n"
            + "\n".join(
                f"x = {pretty(root)}"
                for root in roots
            )
            + "\n\n"
            "Answer:\n"
            + ", ".join(
                pretty(root)
                for root in roots
            )
        )

    except:

        return (
            "QUADRATIC EQUATION\n\n"
            "Example:\n"
            "x² - 5x + 6 = 0"
        )


# ============================================================
# LINEAR INEQUALITIES
# ============================================================

def solve_inequality(q):

    try:

        text = clean(q)

        if "<=" in text:
            left, right = text.split("<=", 1)
            relation = sp.Le(
                expression(left),
                expression(right)
            )

        elif ">=" in text:
            left, right = text.split(">=", 1)
            relation = sp.Ge(
                expression(left),
                expression(right)
            )

        elif "<" in text:
            left, right = text.split("<", 1)
            relation = sp.Lt(
                expression(left),
                expression(right)
            )

        elif ">" in text:
            left, right = text.split(">", 1)
            relation = sp.Gt(
                expression(left),
                expression(right)
            )

        else:
            return "Enter an inequality such as 2*x + 3 > 7"

        answer = sp.solve_univariate_inequality(
            relation,
            x
        )

        return (
            "LINEAR INEQUALITIES\n\n"
            f"Given:\n{q}\n\n"
            f"Solution:\n{answer}\n\n"
            f"Answer:\n{answer}"
        )

    except:

        return (
            "LINEAR INEQUALITIES\n\n"
            "Example:\n"
            "2*x + 3 > 7"
        )


# ============================================================
# PERMUTATIONS & COMBINATIONS
# ============================================================

def solve_permutations(q):

    text = q.lower().replace(" ", "")

    match = re.search(
        r"(\d+)(p|c)(\d+)",
        text
    )

    if not match:

        return (
            "PERMUTATIONS & COMBINATIONS\n\n"
            "Examples:\n"
            "10P3\n"
            "10C3"
        )

    n = int(match.group(1))
    r = int(match.group(3))
    kind = match.group(2)

    if r > n:

        return "r cannot be greater than n."

    if kind == "p":

        answer = math.factorial(n) // math.factorial(n - r)

        return (
            "PERMUTATIONS\n\n"
            f"n = {n}\n"
            f"r = {r}\n\n"
            "Formula:\n"
            "nPr = n! / (n-r)!\n\n"
            f"Answer:\n{answer}"
        )

    answer = (
        math.factorial(n)
        // (
            math.factorial(r)
            * math.factorial(n - r)
        )
    )

    return (
        "COMBINATIONS\n\n"
        f"n = {n}\n"
        f"r = {r}\n\n"
        "Formula:\n"
        "nCr = n! / r!(n-r)!\n\n"
        f"Answer:\n{answer}"
    )


# ============================================================
# BINOMIAL THEOREM
# ============================================================

def solve_binomial(q):

    try:

        expr = expression(q)

        expanded = sp.expand(expr)

        return (
            "BINOMIAL THEOREM\n\n"
            f"Expression:\n{pretty(expr)}\n\n"
            "Expansion:\n"
            f"{pretty(expanded)}\n\n"
            f"Answer:\n{pretty(expanded)}"
        )

    except:

        return (
            "BINOMIAL THEOREM\n\n"
            "Example:\n"
            "(x + 2)^5"
        )


# ============================================================
# SEQUENCES & SERIES
# ============================================================

def solve_sequence(q):

    text = q.lower()

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        q
    )

    if len(numbers) >= 2:

        try:

            a = sp.Rational(numbers[0])
            second = sp.Rational(numbers[1])

            d = second - a

            n_match = re.search(
                r"(\d+)(?:st|nd|rd|th)?\s*term",
                text
            )

            if n_match:

                N = int(n_match.group(1))

                answer = a + (N - 1) * d

                return (
                    "SEQUENCES & SERIES\n\n"
                    f"First term, a = {a}\n"
                    f"Common difference, d = {d}\n"
                    f"Required term, n = {N}\n\n"
                    "Formula:\n"
                    "aₙ = a + (n − 1)d\n\n"
                    f"aₙ = {a} + ({N} − 1)({d})\n\n"
                    f"Answer:\n{pretty(answer)}"
                )

        except:
            pass

    return (
        "SEQUENCES & SERIES\n\n"
        "Example:\n"
        "AP 3, 7, 11, 15... 10th term"
    )


# ============================================================
# STRAIGHT LINES
# ============================================================

def solve_straight_lines(q):

    points = re.findall(
        r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*\)",
        clean(q)
    )

    if len(points) >= 2:

        x1, y1 = map(sp.Rational, points[0])
        x2, y2 = map(sp.Rational, points[1])

        if "slope" in q.lower():

            if x2 == x1:
                answer = "Undefined (vertical line)"

            else:
                answer = sp.simplify(
                    (y2 - y1) / (x2 - x1)
                )

            return (
                "STRAIGHT LINES\n\n"
                f"P₁ = ({x1}, {y1})\n"
                f"P₂ = ({x2}, {y2})\n\n"
                "Formula:\n"
                "m = (y₂ − y₁)/(x₂ − x₁)\n\n"
                f"Answer:\n{answer}"
            )

        if "distance" in q.lower():

            answer = sp.sqrt(
                (x2 - x1) ** 2
                +
                (y2 - y1) ** 2
            )

            return (
                "STRAIGHT LINES\n\n"
                "Distance formula:\n"
                "d = √[(x₂−x₁)² + (y₂−y₁)²]\n\n"
                f"Answer:\n{pretty(answer)}"
            )

    return (
        "STRAIGHT LINES\n\n"
        "Examples:\n"
        "Find slope between (1,2) and (4,8)\n"
        "Find distance between (2,3) and (6,6)"
    )


# ============================================================
# CONIC SECTIONS
# ============================================================

def solve_conics(q):

    try:

        expr = expression(q)

        return (
            "CONIC SECTIONS\n\n"
            f"Expression:\n{pretty(expr)}\n\n"
            f"Simplified:\n{pretty(sp.expand(expr))}"
        )

    except:

        return (
            "CONIC SECTIONS\n\n"
            "Examples:\n"
            "y² = 4ax\n"
            "x² + y² = r²"
        )


# ============================================================
# 3D GEOMETRY
# ============================================================

def solve_3d(q):

    points = re.findall(
        r"\(\s*(-?\d+)\s*,\s*(-?\d+)\s*,\s*(-?\d+)\s*\)",
        clean(q)
    )

    if len(points) >= 2:

        p1 = list(map(sp.Rational, points[0]))
        p2 = list(map(sp.Rational, points[1]))

        answer = sp.sqrt(
            sum(
                (p2[i] - p1[i]) ** 2
                for i in range(3)
            )
        )

        return (
            "3D GEOMETRY\n\n"
            "Distance formula:\n"
            "d = √[(x₂−x₁)² + (y₂−y₁)² + (z₂−z₁)²]\n\n"
            f"Answer:\n{pretty(answer)}"
        )

    return (
        "3D GEOMETRY\n\n"
        "Example:\n"
        "Find distance between (1,2,3) and (4,6,3)"
    )


# ============================================================
# LIMITS & DERIVATIVES
# ============================================================

def solve_limits(q):

    try:

        text = clean(q)

        if (
            "differentiate" in q.lower()
            or "derivative" in q.lower()
        ):

            match = re.search(
                r"(?:differentiate|derivative\s+of)\s+(.+)",
                text,
                re.IGNORECASE
            )

            if match:

                expr = expression(
                    match.group(1)
                )

            else:

                expr = expression(text)

            answer = sp.diff(expr, x)

            return (
                "LIMITS & DERIVATIVES\n\n"
                f"Function:\n{pretty(expr)}\n\n"
                "Derivative:\n"
                f"d/dx = {pretty(answer)}\n\n"
                f"Answer:\n{pretty(answer)}"
            )

        match = re.search(
            r"limit\s+(.+?)\s+(?:as\s+)?x\s*(?:->|→)\s*(-?\d+)",
            text,
            re.IGNORECASE
        )

        if match:

            expr = expression(match.group(1))
            value = sp.Rational(match.group(2))

            answer = sp.limit(
                expr,
                x,
                value
            )

            return (
                "LIMITS & DERIVATIVES\n\n"
                f"Limit:\nlim x→{value} {pretty(expr)}\n\n"
                f"Answer:\n{pretty(answer)}"
            )

    except:
        pass

    return (
        "LIMITS & DERIVATIVES\n\n"
        "Examples:\n"
        "differentiate x^3 + 2*x^2\n"
        "limit (x^2-1)/(x-1) as x->1"
    )


# ============================================================
# STATISTICS
# ============================================================

def solve_statistics(q):

    values = [
        float(v)
        for v in re.findall(
            r"-?\d+(?:\.\d+)?",
            q
        )
    ]

    if not values:

        return (
            "STATISTICS\n\n"
            "Example:\n"
            "Find mean, median and standard deviation of "
            "2, 4, 4, 6, 8"
        )

    values_sorted = sorted(values)

    mean = sum(values) / len(values)

    if len(values) % 2 == 1:

        median = values_sorted[
            len(values) // 2
        ]

    else:

        middle = len(values) // 2

        median = (
            values_sorted[middle - 1]
            +
            values_sorted[middle]
        ) / 2

    counts = Counter(values)

    highest_frequency = max(
        counts.values()
    )

    if highest_frequency == 1:

        mode = "No mode"

    else:

        mode = ", ".join(
            str(v)
            for v, count in counts.items()
            if count == highest_frequency
        )

    variance = sum(
        (v - mean) ** 2
        for v in values
    ) / len(values)

    standard_deviation = math.sqrt(
        variance
    )

    return (
        "STATISTICS\n\n"
        f"Data:\n{values}\n\n"
        f"Mean = {mean:g}\n"
        f"Median = {median:g}\n"
        f"Mode = {mode}\n"
        f"Variance = {variance:g}\n"
        f"Standard deviation = {standard_deviation:g}"
    )


# ============================================================
# PROBABILITY
# ============================================================

def solve_probability(q):

    text = q.lower()

    if "coin" in text:

        return (
            "PROBABILITY\n\n"
            "For a fair coin:\n"
            "Sample space = {H, T}\n\n"
            "Favourable outcomes = 1\n"
            "Total outcomes = 2\n\n"
            "P(H) = 1/2\n\n"
            "Answer:\n1/2"
        )

    if "die" in text or "dice" in text:

        return (
            "PROBABILITY\n\n"
            "For a fair die:\n"
            "Sample space = {1,2,3,4,5,6}\n\n"
            "Probability of one specified number:\n"
            "P(E) = 1/6\n\n"
            "Answer:\n1/6"
        )

    return (
        "PROBABILITY\n\n"
        "Example:\n"
        "A coin is tossed once. Find the probability "
        "of getting a head."
    )


# ============================================================
# GENERAL ALGEBRA
# ============================================================

def solve_general(q):

    try:

        text = clean(q)

        if "=" in text:

            left, right = text.split("=", 1)

            equation = sp.Eq(
                expression(left),
                expression(right)
            )

            solutions = sp.solve(
                equation,
                x
            )

            if solutions:

                return (
                    "ALGEBRA\n\n"
                    f"Equation:\n{q}\n\n"
                    "Solutions:\n"
                    +
                    "\n".join(
                        f"x = {pretty(v)}"
                        for v in solutions
                    )
                )

        expr = expression(text)

        answer = sp.simplify(expr)

        return (
            "ALGEBRA\n\n"
            f"Input:\n{pretty(expr)}\n\n"
            f"Simplified:\n{pretty(answer)}"
        )

    except:

        return (
            "I couldn't understand that question yet.\n\n"
            "Try writing it like:\n"
            "x^2 - 5*x + 6 = 0"
        )


# ============================================================
# MAIN SOLVER
# ============================================================

def solve(question, chapter="Auto Detect"):

    if not question.strip():

        return "Please enter a question."

    if chapter == "Auto Detect":

        chapter = detect_chapter(question)

    if chapter == "Sets":
        return solve_sets(question)

    if chapter == "Relations & Functions":
        return solve_functions(question)

    if chapter == "Trigonometric Functions":
        return solve_trigonometry(question)

    if chapter == "Complex Numbers & Quadratic Equations":
        return solve_quadratic(question)

    if chapter == "Linear Inequalities":
        return solve_inequality(question)

    if chapter == "Permutations & Combinations":
        return solve_permutations(question)

    if chapter == "Binomial Theorem":
        return solve_binomial(question)

    if chapter == "Sequences & Series":
        return solve_sequence(question)

    if chapter == "Straight Lines":
        return solve_straight_lines(question)

    if chapter == "Conic Sections":
        return solve_conics(question)

    if chapter == "3D Geometry":
        return solve_3d(question)

    if chapter == "Limits & Derivatives":
        return solve_limits(question)

    if chapter == "Statistics":
        return solve_statistics(question)

    if chapter == "Probability":
        return solve_probability(question)

    return solve_general(question)