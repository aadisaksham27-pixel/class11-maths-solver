"""Compatibility router: local school-math engine first, generic math second."""
from math_engine import solve_math, detect_topic
try:
    from school_math import solve_school_math, SCHOOL_MATH_CHAPTERS
except Exception:
    solve_school_math = None
    SCHOOL_MATH_CHAPTERS = []

def detect_chapter(question):
    return detect_topic(question)

def solve(question, chapter="Auto Detect"):
    result = solve_math(question)
    if result.get("success"):
        return _format(result)
    if solve_school_math is not None:
        try:
            out = solve_school_math(question, "Auto Detect")
            if out and "Unable to solve" not in str(out):
                return str(out)
        except Exception:
            pass
    raise ValueError(result.get("message") or "Unable to solve this question locally.")

def _format(r):
    lines=[f"Detected topic: {r.get('topic','General Mathematics')}","","Step-by-step solution:"]
    for i,s in enumerate(r.get("steps",[]),1): lines.append(f"{i}. {s}")
    lines += ["",f"Final answer: {r.get('final_answer','')}"]
    if r.get("decimal_answer"): lines.append(f"Decimal form: {r['decimal_answer']}")
    if r.get("verified"): lines.append("Verification: ✓")
    return "\n".join(lines)
