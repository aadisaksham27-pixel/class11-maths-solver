
"""
Kshitij Study Solver - Scientific Calculator Engine
---------------------------------------------------
A safe SymPy-based calculator/equation solver that returns
student-friendly step-by-step working.

This file replaces the old calculator.py.

Supported examples include:
    2+3*5
    sqrt(144)
    2^5
    10C3
    x+5=12
    2*x+5=15
    x^2-5*x+6=0
    x+y=10; x-y=2
    sin(30)
    log(8,2)
    2^(x+1)=16
    diff(x^2+3*x,x)
    integrate(2*x+3,x)

It is deliberately not advertised as "every possible equation".
When SymPy cannot reliably solve an input, the function returns a
clear message instead of inventing an answer.
"""

import math
import re
from typing import List, Tuple

try:
    import sympy as sp
    from sympy.parsing.sympy_parser import (
        parse_expr,
        standard_transformations,
        implicit_multiplication_application,
        convert_xor,
    )
except ImportError as exc:
    raise ImportError(
        "This calculator requires SymPy. Install it with: pip install sympy"
    ) from exc


TRANSFORMATIONS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)

# Common student-friendly names.
LOCAL_DICT = {
    "pi": sp.pi,
    "π": sp.pi,
    "e": sp.E,
    "E": sp.E,
    "I": sp.I,
    "i": sp.I,
    "inf": sp.oo,
    "infinity": sp.oo,
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
    "acot": sp.acot,
    "asec": sp.asec,
    "acsc": sp.acsc,
    "sinh": sp.sinh,
    "cosh": sp.cosh,
    "tanh": sp.tanh,
    "ln": sp.log,
    "log": sp.log,
    "log10": sp.log10,
    "exp": sp.exp,
    "abs": sp.Abs,
    "Abs": sp.Abs,
    "floor": sp.floor,
    "ceil": sp.ceiling,
    "factorial": sp.factorial,
    "fact": sp.factorial,
    "binomial": sp.binomial,
    "C": sp.binomial,
    "comb": sp.binomial,
    "P": lambda n, r: sp.factorial(n) / sp.factorial(n - r),
    "perm": lambda n, r: sp.factorial(n) / sp.factorial(n - r),
    "Derivative": sp.Derivative,
}

# Single-letter symbols are useful for school algebra.
for _letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
    LOCAL_DICT[_letter] = sp.Symbol(_letter)


def _clean_text(value) -> str:
    """Make SymPy output easier for students to read."""
    text = str(value)
    text = text.replace("**", "^")
    text = text.replace("*", " × ")
    text = text.replace("/", " / ")
    text = text.replace("sqrt(", "√(")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _pretty(value) -> str:
    """Unicode pretty-print without requiring terminal formatting."""
    try:
        return sp.pretty(value, use_unicode=True)
    except Exception:
        return _clean_text(value)


def _parse(text: str):
    """Parse an expression without using Python eval()."""
    text = text.strip()

    # User-friendly Unicode operators.
    replacements = {
        "×": "*",
        "·": "*",
        "÷": "/",
        "−": "-",
        "–": "-",
        "—": "-",
        "√": "sqrt",
        "π": "pi",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Degree marker: sin(30°) -> sin(30*pi/180)
    text = re.sub(
        r"(\d+(?:\.\d+)?)\s*°",
        r"(\1*pi/180)",
        text,
    )

    # Friendly combination notation: 10C3 -> binomial(10,3)
    text = re.sub(
        r"(?<![A-Za-z_])(\d+(?:\.\d+)?)\s*[Cc]\s*(\d+(?:\.\d+)?)",
        r"binomial(\1,\2)",
        text,
    )

    # Factorial shorthand remains supported by SymPy.
    return parse_expr(
        text,
        local_dict=LOCAL_DICT,
        transformations=TRANSFORMATIONS,
        evaluate=True,
    )


def _split_equations(text: str) -> List[str]:
    """Split systems written with ';', newline, or comma."""
    return [
        part.strip()
        for part in re.split(r"[;\n]+", text)
        if part.strip()
    ]


def _format_number(value) -> str:
    """Readable numerical result."""
    value = sp.N(value, 12)
    if value.is_Integer:
        return str(int(value))
    if value.is_Rational:
        return str(value)
    if value.is_real:
        try:
            f = float(value)
            if math.isfinite(f) and abs(f - round(f)) < 1e-12:
                return str(int(round(f)))
        except Exception:
            pass
    return _clean_text(value)


def _is_equation(text: str) -> bool:
    return "=" in text


def _parse_equation(text: str):
    left, right = text.split("=", 1)
    if not left.strip() or not right.strip():
        raise ValueError("An equation needs something on both sides of '='.")
    lhs = _parse(left)
    rhs = _parse(right)
    return sp.Eq(lhs, rhs)


def _variables_from_equations(equations) -> List[sp.Symbol]:
    symbols = set()
    for eq in equations:
        symbols.update(eq.free_symbols)
    return sorted(symbols, key=lambda s: str(s))


def _numeric_expression_steps(expr) -> List[str]:
    """Generate useful, conservative working for numerical expressions."""
    steps: List[str] = []

    def add(label, value):
        line = f"{label}: {_clean_text(value)}"
        if not steps or steps[-1] != line:
            steps.append(line)

    # Work from inner operations outward.
    if isinstance(expr, sp.Number):
        return steps

    # Powers / roots.
    if isinstance(expr, sp.Pow):
        base, exponent = expr.as_base_exp()
        if base.is_number and exponent.is_number:
            add(
                "Evaluate the power/root",
                f"{_clean_text(base)}^{_clean_text(exponent)} = {_format_number(expr)}",
            )
            return steps

    # Standard mathematical functions.
    if expr.is_Function:
        args = expr.args
        name = expr.func.__name__
        if all(arg.is_number for arg in args):
            evaluated = sp.N(expr, 12)
            add(
                f"Evaluate {name}",
                f"{_clean_text(expr)} = {_format_number(evaluated)}",
            )
            return steps

    # For addition/multiplication, show each operation if possible.
    if expr.is_Add:
        args = list(expr.args)
        if len(args) > 1 and all(a.is_number for a in args):
            running = args[0]
            for item in args[1:]:
                new_value = sp.simplify(running + item)
                add(
                    "Add",
                    f"{_clean_text(running)} + {_clean_text(item)} = {_format_number(new_value)}",
                )
                running = new_value
            return steps

    if expr.is_Mul:
        args = list(expr.args)
        if len(args) > 1 and all(a.is_number for a in args):
            running = args[0]
            for item in args[1:]:
                new_value = sp.simplify(running * item)
                add(
                    "Multiply",
                    f"{_clean_text(running)} × {_clean_text(item)} = {_format_number(new_value)}",
                )
                running = new_value
            return steps

    # General fallback: show simplification if it changes the expression.
    simplified = sp.simplify(expr)
    if simplified != expr:
        add("Simplify", simplified)

    return steps


def _solve_single_equation(eq: sp.Equality) -> str:
    symbols = _variables_from_equations([eq])

    if not symbols:
        truth = sp.simplify(eq.lhs - eq.rhs) == 0
        return (
            "Step 1 — Compare both sides\n"
            f"{_pretty(eq.lhs)} = {_pretty(eq.rhs)}\n\n"
            f"Answer: {'True' if truth else 'False'}"
        )

    if len(symbols) != 1:
        raise ValueError(
            "This equation contains multiple variables. "
            "For multiple variables, enter a system such as "
            "x+y=10; x-y=2."
        )

    x = symbols[0]
    expression = sp.expand(eq.lhs - eq.rhs)

    # Polynomial route: particularly clear for school algebra.
    try:
        degree = sp.Poly(expression, x).degree()
    except Exception:
        degree = None

    if degree == 1:
        a = sp.expand(expression).coeff(x, 1)
        b = sp.expand(expression).coeff(x, 0)

        if a == 0:
            raise ValueError("This equation does not have a unique linear solution.")

        steps = [
            "Step 1 — Move everything to one side",
            f"{_pretty(expression)} = 0",
            "",
            "Step 2 — Isolate the variable",
            f"{_pretty(a)}{x} = {_pretty(-b)}",
            "",
            "Step 3 — Divide by the coefficient of the variable",
            f"{x} = {_pretty(sp.simplify(-b / a))}",
        ]

        solution = sp.solve(eq, x)
        if solution:
            steps += ["", f"Final Answer: {x} = {_pretty(solution[0])}"]
        return "\n".join(steps)

    if degree == 2:
        poly = sp.Poly(expression, x)
        a, b, c = poly.all_coeffs()
        discriminant = sp.simplify(b**2 - 4*a*c)
        solutions = sp.solve(eq, x)

        steps = [
            "Step 1 — Write the equation in standard form",
            f"{_pretty(a)}{x}² + {_pretty(b)}{x} + {_pretty(c)} = 0",
            "",
            "Step 2 — Identify a, b and c",
            f"a = {_pretty(a)}",
            f"b = {_pretty(b)}",
            f"c = {_pretty(c)}",
            "",
            "Step 3 — Calculate the discriminant",
            "D = b² − 4ac",
            f"D = {_pretty(discriminant)}",
            "",
            "Step 4 — Use the quadratic formula",
            "x = (−b ± √D) / (2a)",
        ]

        if solutions:
            steps += [
                "",
                "Step 5 — Calculate the solutions",
            ]
            for index, sol in enumerate(solutions, 1):
                steps.append(f"x{index} = {_pretty(sol)}")
            steps += [
                "",
                "Final Answer: " + ", ".join(
                    f"x{index} = {_pretty(sol)}"
                    for index, sol in enumerate(solutions, 1)
                )
            ]

        return "\n".join(steps)

    # General symbolic solver.
    solutions = sp.solve(eq, x)
    if not solutions:
        return (
            f"Equation: {_pretty(eq.lhs)} = {_pretty(eq.rhs)}\n\n"
            "The equation has no solution that SymPy can express in the "
            "current form."
        )

    return (
        "Step 1 — Rearrange the equation\n"
        f"{_pretty(eq.lhs)} = {_pretty(eq.rhs)}\n\n"
        "Step 2 — Solve for the variable\n"
        f"{x} = " + ", ".join(_pretty(s) for s in solutions) +
        "\n\nFinal Answer: " +
        ", ".join(f"{x} = {_pretty(s)}" for s in solutions)
    )


def _solve_system(lines: List[str]) -> str:
    equations = [_parse_equation(line) for line in lines]
    variables = _variables_from_equations(equations)

    if len(variables) < 2:
        return _solve_single_equation(equations[0])

    if len(equations) < len(variables):
        raise ValueError(
            "A system needs enough equations for its variables."
        )

    solutions = sp.solve(equations, variables, dict=True)

    steps = [
        "Step 1 — Write the system",
        *[
            f"{index}. {_pretty(eq.lhs)} = {_pretty(eq.rhs)}"
            for index, eq in enumerate(equations, 1)
        ],
        "",
        "Step 2 — Solve the simultaneous equations",
    ]

    if not solutions:
        steps.append("No solution was found.")
        return "\n".join(steps)

    for solution_set in solutions:
        for variable in variables:
            if variable in solution_set:
                steps.append(
                    f"{variable} = {_pretty(solution_set[variable])}"
                )

    steps.append("")
    steps.append("Final Answer:")
    for solution_set in solutions:
        steps.append(
            ", ".join(
                f"{v} = {_pretty(solution_set[v])}"
                for v in variables
                if v in solution_set
            )
        )

    return "\n".join(steps)


def _calculus_command(text: str):
    """
    Supports:
      diff(expression, variable)
      derivative(expression, variable)
      integrate(expression, variable)
      integral(expression, variable)
    """
    match = re.match(
        r"^\s*(diff|derivative|integrate|integral)\s*\((.*)\)\s*$",
        text,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return None

    command = match.group(1).lower()
    inside = match.group(2)

    # Split the final comma so expressions can contain commas in functions.
    parts = inside.rsplit(",", 1)
    if len(parts) != 2:
        raise ValueError(
            "Use diff(expression, x) or integrate(expression, x)."
        )

    expression_text, variable_text = parts
    variable_text = variable_text.strip()

    if not re.fullmatch(r"[A-Za-z]\w*", variable_text):
        raise ValueError("Please provide a valid variable such as x.")

    variable = sp.Symbol(variable_text)
    expression = _parse(expression_text)

    if command in ("diff", "derivative"):
        result = sp.diff(expression, variable)
        title = "Derivative"
        formula = f"d/d{variable} ({_pretty(expression)})"
    else:
        result = sp.integrate(expression, variable)
        title = "Integral"
        formula = f"∫({_pretty(expression)}) d{variable}"

    return (
        f"Step 1 — Write the expression\n"
        f"{formula}\n\n"
        f"Step 2 — Apply the {title.lower()} rule\n"
        f"{_pretty(result)}\n\n"
        f"Final Answer: {_pretty(result)}"
        + ("" if command in ("diff", "derivative") else " + C")
    )


def calculate(expression: str):
    """
    Main function used by app.py.

    Returns a string because the existing Flask route already converts
    the result to JSON with str(result).
    """
    if expression is None:
        raise ValueError("Enter a calculator expression.")

    text = str(expression).strip()

    if not text:
        raise ValueError("Enter a calculator expression.")

    if len(text) > 1000:
        raise ValueError("Expression is too long. Please enter a shorter expression.")

    # Calculus commands.
    calculus = _calculus_command(text)
    if calculus is not None:
        return calculus

    # Systems / equations.
    if _is_equation(text):
        lines = _split_equations(text)

        # Support comma-separated systems only when each comma-separated
        # part clearly contains an equals sign.
        if len(lines) == 1 and text.count("=") > 1:
            lines = [
                part.strip()
                for part in re.split(r",", text)
                if part.strip()
            ]

        if len(lines) > 1:
            return _solve_system(lines)

        return _solve_single_equation(_parse_equation(lines[0]))

    # Normal expression.
    expr = _parse(text)

    if expr.free_symbols:
        simplified = sp.simplify(expr)
        if simplified != expr:
            return (
                "Step 1 — Simplify the expression\n"
                f"{_pretty(expr)}\n\n"
                f"Step 2 — Simplified form\n"
                f"{_pretty(simplified)}\n\n"
                f"Final Answer: {_pretty(simplified)}"
            )

        return (
            "This is a symbolic expression.\n\n"
            f"Expression: {_pretty(expr)}\n\n"
            "No value can be calculated until values are assigned "
            "to the variables."
        )

    steps = _numeric_expression_steps(expr)
    exact = sp.simplify(expr)
    numerical = sp.N(exact, 12)

    output = ["Step-by-step solution"]

    if steps:
        output.append("")
        for index, step in enumerate(steps, 1):
            output.append(f"Step {index} — {step}")

    output.extend([
        "",
        f"Exact Answer: {_pretty(exact)}",
        f"Decimal Answer: {_format_number(numerical)}",
    ])

    return "\n".join(output)
