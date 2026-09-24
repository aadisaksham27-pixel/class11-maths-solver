# ============================================================
# KSHITIJ CLASS 8-12 SOLVER
# ============================================================

import math
import re
from collections import Counter

import sympy as sp

# ============================================================
# IMPORT SCHOOL ENGINES
# ============================================================

try:
    from school_math import (
        solve_school_math,
        is_school_math_chapter,
        SCHOOL_MATH_CHAPTERS,
    )
except ImportError:
    SCHOOL_MATH_CHAPTERS = set()

    def is_school_math_chapter(chapter):
        return False

    def solve_school_math(question, chapter="Auto Detect"):
        return (
            "School Mathematics engine is not available. "
            "Please check school_math.py."
        )


try:
    from science_engine import (
        solve_science,
        is_science_chapter,
        SCIENCE_CHAPTERS,
    )
except ImportError:
    SCIENCE_CHAPTERS = set()

    def is_science_chapter(chapter):
        return False

    def solve_science(question, chapter="Auto Detect"):
        return (
            "Science engine is not available. "
            "Please check science_engine.py."
        )


# ============================================================
# SYMBOLS
# ============================================================

x, y, z = sp.symbols("x y z")


# ============================================================
# BASIC HELPERS
# ============================================================

def clean(text):

    text = str(text).strip()

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
        "≤": "<=",
        "≥": ">=",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("^", "**")

    # 2x -> 2*x
    text = re.sub(
        r"(\d)\s*x",
        r"\1*x",
        text,
        flags=re.IGNORECASE,
    )

    return text


def expression(text):

    return sp.sympify(
        clean(text),
        locals={
            "x": x,
            "y": y,
            "z": z,
            "pi": sp.pi,
            "oo": sp.oo,
            "sqrt": sp.sqrt,
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "cot": sp.cot,
            "sec": sp.sec,
            "csc": sp.csc,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "log": sp.log,
            "ln": sp.log,
            "exp": sp.exp,
        },
    )


def pretty(value):

    try:
        return sp.pretty(
            sp.simplify(value),
            use_unicode=True,
        )
    except Exception:
        return str(value)


# ============================================================
# CHAPTER ALIASES
# ============================================================

CHAPTER_ALIASES = {

    # Class 11 Mathematics
    "Introduction to Three Dimensional Geometry":
        "3D Geometry",

    "Complex Numbers and Quadratic Equations":
        "Complex Numbers & Quadratic Equations",

    "Permutations and Combinations":
        "Permutations & Combinations",

    "Sequences and Series":
        "Sequences & Series",

    "Limits and Derivatives":
        "Limits & Derivatives",

    # Common variations
    "3D Geometry":
        "3D Geometry",

    "Three Dimensional Geometry":
        "3D Geometry",

    "P & C":
        "Permutations & Combinations",

    # School math aliases
    "Pair of Linear Equations":
        "Pair of Linear Equations in Two Variables",

    "Linear Equations in Two Variables":
        "Linear Equations in Two Variables",

    "Surface Areas and Volumes":
        "Surface Area and Volume",
}


def normalize_chapter(chapter):

    if not chapter:
        return "Auto Detect"

    chapter = chapter.strip()

    return CHAPTER_ALIASES.get(
        chapter,
        chapter
    )


# ============================================================
# CLASS 11 CHAPTERS WITH DEDICATED SOLVERS
# ============================================================

CLASS_11_MATH_CHAPTERS = {
    "Sets",
    "Relations & Functions",
    "Trigonometric Functions",
    "Complex Numbers & Quadratic Equations",
    "Linear Inequalities",
    "Permutations & Combinations",
    "Binomial Theorem",
    "Sequences & Series",
    "Straight Lines",
    "Conic Sections",
    "3D Geometry",
    "Limits & Derivatives",
    "Statistics",
    "Probability",
}


# ============================================================
# ALL SUPPORTED SOLVER CHAPTERS
# ============================================================

SUPPORTED_SOLVER_CHAPTERS = set(
    CLASS_11_MATH_CHAPTERS
)

SUPPORTED_SOLVER_CHAPTERS.update(
    SCHOOL_MATH_CHAPTERS
)

SUPPORTED_SOLVER_CHAPTERS.update(
    SCIENCE_CHAPTERS
)


def is_chapter_supported(chapter):

    chapter = normalize_chapter(chapter)

    return chapter in SUPPORTED_SOLVER_CHAPTERS


def get_supported_chapters():

    return sorted(
        SUPPORTED_SOLVER_CHAPTERS
    )


# ============================================================
# CHAPTER DETECTION
# ============================================================

def detect_chapter(question):

    q = question.lower()

    keywords = [

        # ----------------------------------------------------
        # HIGH PRIORITY — CLASS 11 MATH
        # ----------------------------------------------------

        (
            "Sets",
            [
                "set",
                "union",
                "intersection",
                "subset",
                "complement",
                "venn",
            ],
        ),

        (
            "Relations & Functions",
            [
                "function",
                "domain",
                "range",
                "relation",
                "mapping",
                "one-one",
                "one one",
                "onto",
            ],
        ),

        (
            "Trigonometric Functions",
            [
                "sin",
                "cos",
                "tan",
                "cot",
                "sec",
                "cosec",
                "csc",
                "trigonometric",
                "trigonometry",
            ],
        ),

        (
            "Complex Numbers & Quadratic Equations",
            [
                "complex number",
                "complex numbers",
                "imaginary",
                "quadratic equation",
                "quadratic",
                "discriminant",
                "roots of equation",
            ],
        ),

        (
            "Linear Inequalities",
            [
                "inequality",
                "inequalities",
            ],
        ),

        (
            "Permutations & Combinations",
            [
                "permutation",
                "permutations",
                "combination",
                "combinations",
                "npr",
                "ncr",
            ],
        ),

        (
            "Binomial Theorem",
            [
                "binomial theorem",
                "binomial",
            ],
        ),

        (
            "Sequences & Series",
            [
                "arithmetic progression",
                "geometric progression",
                "a.p",
                "ap",
                "g.p",
                "gp",
                "sequence",
                "series",
                "nth term",
            ],
        ),

        (
            "Straight Lines",
            [
                "straight line",
                "slope",
                "gradient",
                "equation of line",
            ],
        ),

        (
            "Conic Sections",
            [
                "parabola",
                "ellipse",
                "hyperbola",
                "conic section",
                "conic",
            ],
        ),

        (
            "3D Geometry",
            [
                "3d",
                "3-d",
                "three dimensional",
                "three-dimensional",
                "point in space",
            ],
        ),

        (
            "Limits & Derivatives",
            [
                "limit",
                "derivative",
                "differentiate",
                "differentiation",
            ],
        ),

        (
            "Statistics",
            [
                "mean",
                "median",
                "mode",
                "variance",
                "standard deviation",
                "statistics",
            ],
        ),

        (
            "Probability",
            [
                "probability",
                "sample space",
                "probability of",
            ],
        ),
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
        int(v)
        for v in re.findall(
            r"\b\d+\b",
            q
        )
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
# RELATIONS & FUNCTIONS
# ============================================================

def solve_functions(q):

    match = re.search(
        r"f\s*\(\s*x\s*\)\s*=\s*(.+)",
        clean(q),
        re.IGNORECASE,
    )

    if match:

        try:

            expr = expression(
                match.group(1)
            )

            simplified = sp.simplify(expr)

            return (
                "RELATIONS & FUNCTIONS\n\n"
                f"Given:\n"
                f"f(x) = {pretty(expr)}\n\n"
                f"Simplified:\n"
                f"f(x) = {pretty(simplified)}"
            )

        except Exception:
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
            f"Expression:\n"
            f"{pretty(expr)}\n\n"
            "After simplification:\n"
            f"{pretty(answer)}\n\n"
            f"Answer:\n{pretty(answer)}"
        )

    except Exception:

        return (
            "TRIGONOMETRIC FUNCTIONS\n\n"
            "Examples:\n"
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

            left, right = text.split(
                "=",
                1
            )

            equation = sp.Eq(
                expression(left),
                expression(right),
            )

            roots = sp.solve(
                equation,
                x,
            )

        else:

            expr = expression(text)

            roots = sp.solve(
                sp.Eq(expr, 0),
                x,
            )

        if not roots:

            return (
                "QUADRATIC EQUATION\n\n"
                "No roots were found."
            )

        return (
            "COMPLEX NUMBERS & QUADRATIC EQUATIONS\n\n"
            f"Equation:\n{q}\n\n"
            "Solutions:\n"
            +
            "\n".join(
                f"x = {pretty(root)}"
                for root in roots
            )
            +
            "\n\nAnswer:\n"
            +
            ", ".join(
                pretty(root)
                for root in roots
            )
        )

    except Exception:

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

            left, right = text.split(
                "<=",
                1
            )

            relation = sp.Le(
                expression(left),
                expression(right),
            )

        elif ">=" in text:

            left, right = text.split(
                ">=",
                1
            )

            relation = sp.Ge(
                expression(left),
                expression(right),
            )

        elif "<" in text:

            left, right = text.split(
                "<",
                1
            )

            relation = sp.Lt(
                expression(left),
                expression(right),
            )

        elif ">" in text:

            left, right = text.split(
                ">",
                1
            )

            relation = sp.Gt(
                expression(left),
                expression(right),
            )

        else:

            return (
                "LINEAR INEQUALITIES\n\n"
                "Example:\n"
                "2*x + 3 > 7"
            )

        answer = sp.solve_univariate_inequality(
            relation,
            x,
        )

        return (
            "LINEAR INEQUALITIES\n\n"
            f"Given:\n{q}\n\n"
            f"Solution:\n{answer}\n\n"
            f"Answer:\n{answer}"
        )

    except Exception:

        return (
            "LINEAR INEQUALITIES\n\n"
            "Example:\n"
            "2*x + 3 > 7"
        )


# ============================================================
# PERMUTATIONS & COMBINATIONS
# ============================================================

def solve_permutations(q):

    text = q.lower().replace(
        " ",
        ""
    )

    match = re.search(
        r"(\d+)(p|c)(\d+)",
        text,
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

    if n < 0 or r < 0:

        return "n and r must be non-negative."

    if kind == "p":

        answer = (
            math.factorial(n)
            //
            math.factorial(n - r)
        )

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
        //
        (
            math.factorial(r)
            *
            math.factorial(n - r)
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

        text = clean(q)

        # Extract expression if question starts with words.
        text = re.sub(
            r"^(expand|solve|find|calculate)\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        expr = expression(text)

        expanded = sp.expand(expr)

        return (
            "BINOMIAL THEOREM\n\n"
            f"Expression:\n{pretty(expr)}\n\n"
            "Expansion:\n"
            f"{pretty(expanded)}\n\n"
            f"Answer:\n{pretty(expanded)}"
        )

    except Exception:

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

    values = re.findall(
        r"-?\d+(?:\.\d+)?",
        q,
    )

    if len(values) >= 2:

        try:

            a = sp.Rational(values[0])
            second = sp.Rational(values[1])

            d = second - a

            n_match = re.search(
                r"(\d+)(?:st|nd|rd|th)?\s*term",
                text,
            )

            if n_match:

                n = int(
                    n_match.group(1)
                )

                answer = (
                    a
                    +
                    (n - 1) * d
                )

                return (
                    "SEQUENCES & SERIES\n\n"
                    f"First term, a = {a}\n"
                    f"Common difference, d = {d}\n"
                    f"n = {n}\n\n"
                    "Formula:\n"
                    "aₙ = a + (n − 1)d\n\n"
                    f"aₙ = {a} + ({n} − 1)({d})\n\n"
                    f"Answer:\n{pretty(answer)}"
                )

        except Exception:
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
        r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*"
        r"(-?\d+(?:\.\d+)?)\s*\)",
        clean(q),
    )

    if len(points) >= 2:

        x1, y1 = map(
            sp.Rational,
            points[0],
        )

        x2, y2 = map(
            sp.Rational,
            points[1],
        )

        lower = q.lower()

        if "slope" in lower:

            if x2 == x1:

                answer = "Undefined"

            else:

                answer = sp.simplify(
                    (y2 - y1)
                    /
                    (x2 - x1)
                )

            return (
                "STRAIGHT LINES\n\n"
                f"P₁ = ({x1}, {y1})\n"
                f"P₂ = ({x2}, {y2})\n\n"
                "Formula:\n"
                "m = (y₂ − y₁)/(x₂ − x₁)\n\n"
                f"Answer:\n{answer}"
            )

        if "distance" in lower:

            answer = sp.sqrt(
                (x2 - x1) ** 2
                +
                (y2 - y1) ** 2
            )

            return (
                "STRAIGHT LINES\n\n"
                "Formula:\n"
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

        text = clean(q)

        # Try to remove instructional words.
        text = re.sub(
            r"^(find|solve|calculate|simplify)\s+",
            "",
            text,
            flags=re.IGNORECASE,
        )

        expr = expression(text)

        simplified = sp.expand(expr)

        return (
            "CONIC SECTIONS\n\n"
            f"Expression:\n{pretty(expr)}\n\n"
            f"Simplified:\n{pretty(simplified)}"
        )

    except Exception:

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
        r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*"
        r"(-?\d+(?:\.\d+)?)\s*,\s*"
        r"(-?\d+(?:\.\d+)?)\s*\)",
        clean(q),
    )

    if len(points) >= 2:

        p1 = list(
            map(
                sp.Rational,
                points[0],
            )
        )

        p2 = list(
            map(
                sp.Rational,
                points[1],
            )
        )

        distance = sp.sqrt(
            sum(
                (
                    p2[i] - p1[i]
                ) ** 2
                for i in range(3)
            )
        )

        return (
            "3D GEOMETRY\n\n"
            "Distance formula:\n"
            "d = √[(x₂−x₁)² + "
            "(y₂−y₁)² + "
            "(z₂−z₁)²]\n\n"
            f"Answer:\n{pretty(distance)}"
        )

    return (
        "3D GEOMETRY\n\n"
        "Example:\n"
        "Find distance between "
        "(1,2,3) and (4,6,3)"
    )


# ============================================================
# LIMITS & DERIVATIVES
# ============================================================

def solve_limits(q):

    try:

        text = clean(q)
        lower = q.lower()

        if (
            "differentiate" in lower
            or "derivative" in lower
        ):

            match = re.search(
                r"(?:differentiate|"
                r"derivative\s+of)\s+(.+)",
                text,
                re.IGNORECASE,
            )

            if match:

                expr = expression(
                    match.group(1)
                )

            else:

                expr = expression(
                    text
                )

            derivative = sp.diff(
                expr,
                x,
            )

            return (
                "LIMITS & DERIVATIVES\n\n"
                f"Function:\n{pretty(expr)}\n\n"
                "Derivative:\n"
                f"{pretty(derivative)}\n\n"
                f"Answer:\n{pretty(derivative)}"
            )

        match = re.search(
            r"limit\s+(.+?)\s+"
            r"(?:as\s+)?x\s*(?:->|→)\s*"
            r"(-?\d+(?:\.\d+)?)",
            text,
            re.IGNORECASE,
        )

        if match:

            expr = expression(
                match.group(1)
            )

            value = sp.Rational(
                match.group(2)
            )

            answer = sp.limit(
                expr,
                x,
                value,
            )

            return (
                "LIMITS & DERIVATIVES\n\n"
                f"Limit:\n"
                f"lim x→{value} {pretty(expr)}\n\n"
                f"Answer:\n{pretty(answer)}"
            )

    except Exception:
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
            q,
        )
    ]

    if not values:

        return (
            "STATISTICS\n\n"
            "Example:\n"
            "Find mean, median and standard "
            "deviation of 2, 4, 4, 6, 8"
        )

    ordered = sorted(values)

    mean = (
        sum(values)
        /
        len(values)
    )

    if len(values) % 2:

        median = ordered[
            len(values) // 2
        ]

    else:

        middle = len(values) // 2

        median = (
            ordered[middle - 1]
            +
            ordered[middle]
        ) / 2

    counts = Counter(values)

    highest = max(
        counts.values()
    )

    if highest == 1:

        mode = "No mode"

    else:

        mode = ", ".join(
            str(value)
            for value, count
            in counts.items()
            if count == highest
        )

    variance = sum(
        (value - mean) ** 2
        for value in values
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
        f"Standard deviation = "
        f"{standard_deviation:g}"
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
        "A coin is tossed once. "
        "Find the probability of getting a head."
    )


# ============================================================
# GENERAL ALGEBRA
# ============================================================

def solve_general(q):

    try:

        text = clean(q)

        if "=" in text:

            left, right = text.split(
                "=",
                1,
            )

            equation = sp.Eq(
                expression(left),
                expression(right),
            )

            solutions = sp.solve(
                equation,
                x,
            )

            if solutions:

                return (
                    "ALGEBRA\n\n"
                    f"Equation:\n{q}\n\n"
                    "Solutions:\n"
                    +
                    "\n".join(
                        f"x = {pretty(value)}"
                        for value in solutions
                    )
                )

        expr = expression(text)

        answer = sp.simplify(
            expr
        )

        return (
            "ALGEBRA\n\n"
            f"Input:\n{pretty(expr)}\n\n"
            f"Simplified:\n{pretty(answer)}"
        )

    except Exception:

        return (
            "I couldn't understand that question yet.\n\n"
            "Try writing it like:\n"
            "x^2 - 5*x + 6 = 0"
        )


# ============================================================
# CLASS 11 MATH ROUTER
# ============================================================

def solve_class11_math(
    question,
    chapter,
):

    chapter = normalize_chapter(
        chapter
    )

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

    return None


# ============================================================
# MAIN SOLVER
# ============================================================

def solve(
    question,
    chapter="Auto Detect",
):

    if question is None:

        return "Please enter a question."

    question = str(
        question
    ).strip()

    if not question:

        return "Please enter a question."

    # Normalize selected chapter.
    chapter = normalize_chapter(
        chapter
    )

    # --------------------------------------------------------
    # AUTO DETECTION
    # --------------------------------------------------------

    if chapter == "Auto Detect":

        chapter = detect_chapter(
            question
        )

    # --------------------------------------------------------
    # CLASS 8-10 MATHEMATICS
    # --------------------------------------------------------

    if is_school_math_chapter(
        chapter
    ):

        return solve_school_math(
            question,
            chapter,
        )

    # --------------------------------------------------------
    # CLASS 8-10 SCIENCE
    # --------------------------------------------------------

    if is_science_chapter(
        chapter
    ):

        return solve_science(
            question,
            chapter,
        )

    # --------------------------------------------------------
    # CLASS 11 MATHEMATICS
    # --------------------------------------------------------

    if chapter in CLASS_11_MATH_CHAPTERS:

        output = solve_class11_math(
            question,
            chapter,
        )

        if output is not None:

            return output

    # --------------------------------------------------------
    # UNSUPPORTED CHAPTER
    # --------------------------------------------------------

    if not is_chapter_supported(
        chapter
    ):

        return (
            f"'{chapter}' is available in the curriculum, "
            "but its dedicated solver is not implemented yet."
        )

    # --------------------------------------------------------
    # FINAL ALGEBRA FALLBACK
    # --------------------------------------------------------

    return solve_general(
        question
    )


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    tests = [

        (
            "Class 11 quadratic",
            "x^2 - 5*x + 6 = 0",
            "Complex Numbers & Quadratic Equations",
        ),

        (
            "Class 11 derivative",
            "differentiate x^3 + 2*x^2",
            "Limits & Derivatives",
        ),

        (
            "Class 11 probability",
            "A fair coin is tossed",
            "Probability",
        ),

        (
            "General algebra",
            "2*x + 5 = 15",
            "Auto Detect",
        ),
    ]

    print("=" * 60)
    print("KSHITIJ SOLVER TEST")
    print("=" * 60)

    for name, question, chapter in tests:

        print()
        print("-" * 60)
        print(name)
        print("-" * 60)

        try:

            print(
                solve(
                    question,
                    chapter,
                )
            )

        except Exception as error:

            print(
                "ERROR:",
                error
            )