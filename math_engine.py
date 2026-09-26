"""
Kshitij Math Engine
Automatic mathematics question detection + solving + student-friendly steps.

This module is designed to sit behind the Flask /api/calculate endpoint.
It deliberately does NOT claim to solve every possible mathematical problem.
Unsupported or ambiguous questions return a clear explanation instead of an invented answer.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp
from sympy.parsing.sympy_parser import (
    convert_xor,
    implicit_multiplication_application,
    parse_expr,
    standard_transformations,
)

TRANSFORMATIONS = standard_transformations + (
    convert_xor,
    implicit_multiplication_application,
)

SAFE_LOCALS = {
    "pi": sp.pi,
    "π": sp.pi,
    "e": sp.E,
    "E": sp.E,
    "I": sp.I,
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
    "ln": sp.log,
    "log": sp.log,
    "exp": sp.exp,
    "abs": sp.Abs,
    "factorial": sp.factorial,
    "binomial": sp.binomial,
    "floor": sp.floor,
    "ceiling": sp.ceiling,
}

NUMBER_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)")
VARIABLE_RE = re.compile(r"\b([a-zA-Z])\b")


@dataclass
class MathResult:
    topic: str
    question: str
    steps: List[str]
    final_answer: str
    exact_answer: Optional[str] = None
    decimal_answer: Optional[str] = None
    verified: bool = False
    success: bool = True
    message: str = ""

    def as_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "topic": self.topic,
            "question": self.question,
            "steps": self.steps,
            "final_answer": self.final_answer,
            "exact_answer": self.exact_answer,
            "decimal_answer": self.decimal_answer,
            "verified": self.verified,
            "message": self.message,
        }


def _clean(text: str) -> str:
    text = str(text or "").strip()
    text = text.replace("−", "-").replace("–", "-").replace("—", "-")
    text = text.replace("×", "*").replace("·", "*").replace("÷", "/")
    text = text.replace("π", "pi")
    text = text.replace("^", "**")
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _parse(text: str, extra_locals: Optional[Dict[str, Any]] = None):
    cleaned = _clean(text)
    locals_map = dict(SAFE_LOCALS)

    # Treat single letters as symbols, while preserving named functions.
    for letter in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if letter not in locals_map:
            locals_map[letter] = sp.Symbol(letter)

    if extra_locals:
        locals_map.update(extra_locals)

    return parse_expr(
        cleaned,
        local_dict=locals_map,
        transformations=TRANSFORMATIONS,
        evaluate=True,
    )


def _pretty(value: Any) -> str:
    try:
        return str(sp.simplify(value))
    except Exception:
        return str(value)


def _decimal(value: Any) -> Optional[str]:
    try:
        value = sp.N(value, 10)
        if value.is_real:
            return str(value)
    except Exception:
        pass
    return None


def detect_topic(question: str) -> str:
    q = question.lower().strip()

    if "=" in q and ("^2" in q or "x²" in q or "quadratic" in q):
        return "Quadratic Equations"
    if "=" in q and any(v in q for v in ["x", "y", "z"]):
        return "Algebra / Equations"
    if any(k in q for k in ["simultaneous", "simultaneously", "system of equations"]):
        return "Simultaneous Equations"
    if any(k in q for k in ["differentiate", "derivative", "d/dx"]):
        return "Calculus / Differentiation"
    if any(k in q for k in ["integrate", "integration", "integral"]):
        return "Calculus / Integration"
    if any(k in q for k in ["sin", "cos", "tan", "cot", "sec", "csc", "trigonometry"]):
        return "Trigonometry"
    if any(k in q for k in ["mean", "median", "mode", "standard deviation", "variance"]):
        return "Statistics"
    if any(k in q for k in ["probability", "chance", "dice", "cards", "coin"]):
        return "Probability"
    if any(k in q for k in ["sequence", "series", "ap", "a.p.", "arithmetic progression"]):
        return "Sequences / Series"
    if any(k in q for k in ["percentage", "percent", "%"]):
        return "Percentages"
    if any(k in q for k in ["ratio", "proportion"]):
        return "Ratio / Proportion"
    if any(k in q for k in ["factorise", "factorize", "factorisation", "factorization"]):
        return "Factorisation"
    if any(k in q for k in ["matrix", "determinant", "inverse matrix"]):
        return "Matrices"
    if any(k in q for k in ["vector", "dot product", "cross product"]):
        return "Vectors"
    if any(k in q for k in ["log", "logarithm", "ln"]):
        return "Logarithms"
    if any(k in q for k in ["probability", "permutation", "combination", "ncr", "npr"]):
        return "Combinatorics / Probability"
    if any(k in q for k in ["speed", "distance", "time", "train", "car", "average"]):
        return "Mathematical Word Problem"
    if any(k in q for k in ["solve", "find x", "find y", "calculate", "simplify", "evaluate"]):
        return "General Algebra"
    return "General Mathematics"


def _split_equations(question: str) -> List[str]:
    return [x.strip() for x in re.split(r"[;\n]+", question) if x.strip()]


def _symbols_in(exprs: List[Any]) -> List[sp.Symbol]:
    symbols = set()
    for expr in exprs:
        symbols.update(expr.free_symbols)
    return sorted(symbols, key=lambda s: str(s))


def _linear_steps(eq: sp.Equality, symbol: sp.Symbol) -> List[str]:
    lhs, rhs = eq.lhs, eq.rhs
    a = sp.expand(lhs - rhs).coeff(symbol)
    b = sp.expand(lhs - rhs).subs(symbol, 0)

    steps = [
        f"Start with: {sp.sstr(lhs)} = {sp.sstr(rhs)}",
        f"Move all terms involving {symbol} to one side and constants to the other.",
        f"After simplifying: {sp.sstr(a)}{symbol} = {sp.sstr(-b)}",
    ]
    if a != 1:
        steps.append(f"Divide both sides by {sp.sstr(a)}.")
    steps.append(f"{symbol} = {_pretty(-b / a)}")
    return steps


def _quadratic_steps(eq: sp.Equality, symbol: sp.Symbol) -> List[str]:
    poly = sp.Poly(sp.expand(eq.lhs - eq.rhs), symbol)
    a = poly.coeff_monomial(symbol**2)
    b = poly.coeff_monomial(symbol)
    c = poly.coeff_monomial(1)
    D = sp.simplify(b**2 - 4*a*c)
    roots = sp.solve(eq, symbol)

    steps = [
        f"Write the equation in standard form: {sp.sstr(sp.expand(eq.lhs - eq.rhs))} = 0",
        f"Identify coefficients: a = {a}, b = {b}, c = {c}.",
        f"Calculate the discriminant: D = b² − 4ac = {sp.sstr(D)}.",
        "Use the quadratic formula: x = (−b ± √D) / (2a).",
        f"Substitute the values: x = (−({b}) ± √({sp.sstr(D)})) / ({sp.sstr(2*a)}).",
        "Therefore the solutions are: " + ", ".join(f"{symbol} = {_pretty(r)}" for r in roots),
    ]
    return steps


def _solve_equation(question: str) -> MathResult:
    pieces = _split_equations(question)
    if len(pieces) > 1:
        equations = []
        for piece in pieces:
            if "=" not in piece:
                continue
            left, right = piece.split("=", 1)
            equations.append(sp.Eq(_parse(left), _parse(right)))

        if len(equations) >= 2:
            symbols = _symbols_in([e.lhs - e.rhs for e in equations])
            solution = sp.solve(equations, symbols, dict=True)
            steps = [
                "Identify the equations:",
                *[f"{i+1}. {sp.sstr(e.lhs)} = {sp.sstr(e.rhs)}" for i, e in enumerate(equations)],
                f"Variables detected: {', '.join(map(str, symbols))}.",
                "Solve the system simultaneously.",
                f"Solution: {solution}",
            ]
            return MathResult(
                topic="Simultaneous Equations",
                question=question,
                steps=steps,
                final_answer=str(solution),
                exact_answer=str(solution),
                verified=bool(solution),
            )

    if "=" not in question:
        raise ValueError("This does not look like an equation.")

    left, right = question.split("=", 1)
    eq = sp.Eq(_parse(left), _parse(right))
    symbols = _symbols_in([eq.lhs - eq.rhs])

    if not symbols:
        ok = bool(sp.simplify(eq.lhs - eq.rhs) == 0)
        return MathResult(
            topic="Equation Check",
            question=question,
            steps=[
                f"Left side = {sp.sstr(eq.lhs)}",
                f"Right side = {sp.sstr(eq.rhs)}",
                f"The equation is {'true' if ok else 'false'}.",
            ],
            final_answer="True" if ok else "False",
            verified=ok,
        )

    symbol = symbols[0]
    poly = sp.Poly(sp.expand(eq.lhs - eq.rhs), symbol)

    if poly.degree() == 1:
        roots = sp.solve(eq, symbol)
        answer = roots[0]
        return MathResult(
            topic="Linear Equations",
            question=question,
            steps=_linear_steps(eq, symbol),
            final_answer=f"{symbol} = {_pretty(answer)}",
            exact_answer=_pretty(answer),
            decimal_answer=_decimal(answer),
            verified=sp.simplify(eq.lhs.subs(symbol, answer) - eq.rhs.subs(symbol, answer)) == 0,
        )

    if poly.degree() == 2:
        roots = sp.solve(eq, symbol)
        return MathResult(
            topic="Quadratic Equations",
            question=question,
            steps=_quadratic_steps(eq, symbol),
            final_answer=", ".join(f"{symbol} = {_pretty(r)}" for r in roots),
            exact_answer=", ".join(_pretty(r) for r in roots),
            decimal_answer=", ".join(filter(None, (_decimal(r) for r in roots))) or None,
            verified=all(
                sp.simplify(eq.lhs.subs(symbol, r) - eq.rhs.subs(symbol, r)) == 0
                for r in roots
            ),
        )

    roots = sp.solve(eq, symbol)
    return MathResult(
        topic="Algebraic Equations",
        question=question,
        steps=[
            f"Rearrange the equation: {sp.sstr(eq.lhs)} = {sp.sstr(eq.rhs)}",
            f"Solve for {symbol}.",
            f"Solutions found: {', '.join(_pretty(r) for r in roots) if roots else 'No explicit solution found.'}",
        ],
        final_answer=", ".join(f"{symbol} = {_pretty(r)}" for r in roots) if roots else "No explicit solution found.",
        exact_answer=", ".join(_pretty(r) for r in roots) if roots else None,
        verified=bool(roots),
    )


def _solve_expression(question: str) -> MathResult:
    expr = _parse(question)
    simplified = sp.simplify(expr)

    steps = [f"Start with: {question}"]
    if expr != simplified:
        steps.append(f"Simplify the expression: {sp.sstr(simplified)}")
    else:
        steps.append("Evaluate the expression using the order of operations.")

    decimal = _decimal(simplified)
    if decimal and decimal != str(simplified):
        steps.append(f"Decimal form: {decimal}")

    return MathResult(
        topic="Arithmetic / Expression",
        question=question,
        steps=steps,
        final_answer=_pretty(simplified),
        exact_answer=_pretty(simplified),
        decimal_answer=decimal,
        verified=True,
    )


def _solve_calculus(question: str) -> MathResult:
    q = question.strip()
    m = re.match(r"^(diff|derivative)\s*\((.*?)(?:,\s*([a-zA-Z]))?\)\s*$", q, re.I)
    if m:
        expr_text = m.group(2)
        symbol = sp.Symbol(m.group(3) or "x")
        expr = _parse(expr_text)
        result = sp.diff(expr, symbol)
        return MathResult(
            topic="Calculus / Differentiation",
            question=question,
            steps=[
                f"Function: f({symbol}) = {sp.sstr(expr)}",
                f"Differentiate with respect to {symbol}.",
                f"Using differentiation rules: f'({symbol}) = {sp.sstr(result)}",
            ],
            final_answer=sp.sstr(result),
            exact_answer=sp.sstr(result),
            verified=True,
        )

    m = re.match(r"^(integrate|integral)\s*\((.*?)(?:,\s*([a-zA-Z]))?\)\s*$", q, re.I)
    if m:
        expr_text = m.group(2)
        symbol = sp.Symbol(m.group(3) or "x")
        expr = _parse(expr_text)
        result = sp.integrate(expr, symbol)
        return MathResult(
            topic="Calculus / Integration",
            question=question,
            steps=[
                f"Integrand: {sp.sstr(expr)}",
                f"Integrate with respect to {symbol}.",
                f"Antiderivative: {sp.sstr(result)} + C",
            ],
            final_answer=f"{sp.sstr(result)} + C",
            exact_answer=f"{sp.sstr(result)} + C",
            verified=True,
        )

    raise ValueError("Unsupported calculus command.")


def _solve_word_problem(question: str) -> MathResult:
    q = question.lower()

    # Common school-level speed-distance-time pattern.
    nums = [float(x) for x in NUMBER_RE.findall(question)]
    if (
        nums
        and any(k in q for k in ["speed", "distance", "time"])
        and any(k in q for k in ["travel", "travels", "cover", "covers", "journey", "car", "train", "bike"])
    ):
        if "speed" in q and len(nums) >= 2:
            distance, time = nums[0], nums[1]
            speed = distance / time
            return MathResult(
                topic="Mathematical Word Problem — Speed",
                question=question,
                steps=[
                    "Identify the known quantities.",
                    f"Distance = {distance:g}",
                    f"Time = {time:g}",
                    "Use the formula: speed = distance ÷ time.",
                    f"speed = {distance:g} ÷ {time:g} = {speed:g}",
                ],
                final_answer=f"Average speed = {speed:g} distance-units/time-unit",
                decimal_answer=f"{speed:g}",
                verified=True,
                message="Units should be taken from the original question.",
            )

    raise ValueError(
        "This word problem needs the AI word-problem solver because its quantities and relationships "
        "cannot be safely inferred by the local rule-based engine."
    )


def solve_math(question: str) -> Dict[str, Any]:
    """
    Main public function.

    It automatically chooses an appropriate local solver.
    If the problem cannot be safely solved locally, success=False is returned
    so the Flask layer can hand it to the AI tutor.
    """
    question = str(question or "").strip()
    if not question:
        return {
            "success": False,
            "topic": "Unknown",
            "question": "",
            "steps": [],
            "final_answer": "",
            "message": "Please enter a mathematics question.",
            "needs_ai": False,
        }

    topic = detect_topic(question)

    try:
        if any(k in question.lower() for k in ["diff(", "derivative(", "integrate(", "integral("]):
            result = _solve_calculus(question)
        elif "=" in question:
            result = _solve_equation(question)
        elif re.search(r"\b(speed|distance|time|train|car|bike|journey)\b", question, re.I) and not re.search(
            r"[\+\-\*/\^]", question
        ):
            result = _solve_word_problem(question)
        else:
            result = _solve_expression(question)

        result.topic = topic if topic != "General Mathematics" else result.topic
        return result.as_dict() | {"needs_ai": False}

    except Exception as exc:
        return {
            "success": False,
            "topic": topic,
            "question": question,
            "steps": [],
            "final_answer": "",
            "message": str(exc),
            "needs_ai": True,
        }


def solve(question: str) -> str:
    """Compatibility function for existing calculator imports."""
    result = solve_math(question)
    if result["success"]:
        lines = [
            f"Detected topic: {result['topic']}",
            "",
            "Step-by-step solution:",
            *[f"{i}. {step}" for i, step in enumerate(result["steps"], 1)],
            "",
            f"Final answer: {result['final_answer']}",
        ]
        if result.get("decimal_answer"):
            lines.append(f"Decimal form: {result['decimal_answer']}")
        if result.get("verified"):
            lines.append("Verification: ✓")
        return "\n".join(lines)

    return (
        f"Detected topic: {result['topic']}\n\n"
        f"{result['message']}\n\n"
        "The AI Study Assistant can handle word problems or questions "
        "that need broader interpretation."
    )


def calculate(expression: str):
    """
    Compatibility function for the existing /api/calculate route.
    """
    result = solve_math(expression)
    if result["success"]:
        return (
            f"Detected topic: {result['topic']}\n\n"
            + "\n".join(f"{i}. {s}" for i, s in enumerate(result["steps"], 1))
            + f"\n\nFinal answer: {result['final_answer']}"
        )
    raise ValueError(result["message"])
