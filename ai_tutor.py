"""Production-oriented AI study assistant for Kshitij Maths Solver.

Features:
- typed natural-language maths questions
- photos/PDFs/pages with multiple questions
- short videos containing maths questions
- automatic topic/chapter detection
- structured step-by-step JSON
- validation and normalization of model output
- transient-error retries with exponential backoff + jitter
- model fallback for temporary capacity problems
- configurable model list, timeout/retry limits, and upload size
- safe handling of API keys via GEMINI_API_KEY
"""

from __future__ import annotations

import json
import os
import random
import re
import time
from typing import Any

MAX_UPLOAD_MB = max(1, int(os.getenv("AI_MAX_UPLOAD_MB", "20")))
MAX_QUESTION_CHARS = max(1000, int(os.getenv("AI_MAX_QUESTION_CHARS", "12000")))
MAX_MEDIA_QUESTIONS = 20
MAX_RETRIES_PER_MODEL = max(0, min(6, int(os.getenv("AI_MAX_RETRIES", "3"))))
BASE_RETRY_SECONDS = max(0.25, float(os.getenv("AI_RETRY_BASE_SECONDS", "1.5")))

# 3.8 Flash is the current stable general Flash model. A second stable Flash
# model is kept as a fallback for temporary capacity/model-specific failures.
DEFAULT_MODELS = ["gemini-3.8-flash", "gemini-3.6-flash"]
MODEL_LIST = [
    x.strip() for x in os.getenv("GEMINI_MODELS", ",".join(DEFAULT_MODELS)).split(",")
    if x.strip()
] or DEFAULT_MODELS

ALLOWED_MIME = {
    "image/jpeg", "image/png", "image/webp", "image/heic", "image/heif",
    "application/pdf",
    "video/mp4", "video/mpeg", "video/mov", "video/quicktime",
    "video/avi", "video/x-flv", "video/mpg", "video/webm", "video/wmv",
    "video/3gpp",
}

SYSTEM_INSTRUCTION = r"""
You are the mathematics AI assistant inside Kshitij Class 11 Maths Solver.

MISSION
Understand the student's mathematics question and teach the method clearly.
The input can be typed text, a word-problem statement, an equation, an
expression, a photograph/PDF of a worksheet or textbook page, or a short video
showing a maths question.

AUTOMATIC TOPIC DETECTION
The student should not have to choose a chapter. Identify the most appropriate
topic/chapter from the actual problem. Use the supplied curriculum list as a
matching guide, not as a reason to force a chapter that does not fit.

MEDIA READING
- Inspect the uploaded media itself.
- If several distinct maths questions are visible, return one result for each
  reliably readable question, in top-to-bottom/left-to-right order.
- Read numbers, signs, fractions, superscripts, subscripts, roots, brackets,
  units, and visible diagram labels carefully.
- Do not invent values or silently repair ambiguous notation.
- If a question is blurry/cropped/occluded or a symbol is genuinely unclear,
  mark that question as needing clarification and state exactly what is unclear.
- Do not treat headings, examples, or explanatory notes as unanswered questions
  unless they actually ask for a result.

WORD PROBLEMS
Translate the statement into known quantities, the required quantity, and the
mathematical relationship. Show the setup before calculation. Preserve units.

MATH ACCURACY
- Show understandable school-level steps, not just a final answer.
- Prefer exact forms where useful, then give decimal approximations when useful.
- Check arithmetic/algebra and, where practical, substitute the result back into
  the original equation or otherwise verify it.
- Never invent a solution merely to satisfy the student.
- If the problem is outside reliable ability, say so clearly.
- Do not claim to solve every possible mathematical problem.

LANGUAGE
Use clear, simple English suitable for a school student. Keep notation readable
in plain text/Unicode. Avoid unnecessary theory.

OUTPUT
Return ONLY valid JSON matching:
{
  "questions": [
    {
      "question_read": "accurately transcribed/normalized question",
      "chapter": "best topic/chapter",
      "confidence": 0.0,
      "answer": "brief explanation of the method",
      "steps": ["Step 1...", "Step 2..."],
      "final_answer": "final answer, or empty if not reliably solvable",
      "needs_clarification": false,
      "clarification": "empty unless clarification is needed",
      "verification": "short verification/check, or empty"
    }
  ],
  "page_summary": "short summary",
  "overall_message": "short student-friendly message"
}
"""

def _client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        raise RuntimeError(
            "AI assistant is not configured. Set GEMINI_API_KEY in your terminal "
            "before starting the app."
        )
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError(
            "The AI package is missing. Run: pip install google-genai"
        ) from exc
    return genai.Client(api_key=key)

def _chapters_text(chapters):
    if not chapters:
        return "Class 11 Mathematics / automatically determine the best topic."
    return ", ".join(str(x) for x in list(chapters)[:100])

def _prompt(class_name, chapters, question="", media_mode=False):
    source = (
        "The primary source is uploaded media. Inspect it directly and find every "
        "reliably readable mathematics question."
        if media_mode else
        "The primary source is the student's typed question."
    )
    return f"""{SYSTEM_INSTRUCTION}

Student class: {class_name}
Possible curriculum topics:
{_chapters_text(chapters)}

{source}

Optional typed text:
{question or "(none — read the uploaded material)"}

Return one question object for each distinct maths question you can reliably
identify. Preserve source order.
"""

def _clean_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()

def _as_bool(value):
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes"}

def _normalise(data):
    if not isinstance(data, dict):
        data = {}

    questions = data.get("questions")
    if not isinstance(questions, list):
        if data.get("question_read") or data.get("answer") or data.get("final_answer"):
            questions = [data]
        else:
            questions = []

    clean = []
    for item in questions[:MAX_MEDIA_QUESTIONS]:
        if not isinstance(item, dict):
            continue
        steps = item.get("steps", [])
        if isinstance(steps, str):
            steps = [steps]
        if not isinstance(steps, list):
            steps = []

        try:
            confidence = float(item.get("confidence", 0))
        except (TypeError, ValueError):
            confidence = 0.0

        confidence = max(0.0, min(1.0, confidence))
        clarification = str(item.get("clarification", "")).strip()
        needs = _as_bool(item.get("needs_clarification", False)) or bool(clarification)

        clean.append({
            "question_read": str(item.get("question_read", "")).strip(),
            "chapter": str(item.get("chapter", "Auto detected")).strip() or "Auto detected",
            "confidence": confidence,
            "answer": str(item.get("answer", "")).strip(),
            "steps": [str(s).strip() for s in steps if str(s).strip()][:40],
            "final_answer": str(item.get("final_answer", "")).strip(),
            "needs_clarification": needs,
            "clarification": clarification,
            "verification": str(item.get("verification", "")).strip(),
        })

    return {
        "questions": clean,
        "page_summary": str(data.get("page_summary", "")).strip(),
        "overall_message": str(data.get("overall_message", "")).strip(),
    }

def _parse_response(response):
    raw = getattr(response, "text", "") or ""
    cleaned = _clean_json(raw)
    try:
        return _normalise(json.loads(cleaned))
    except Exception:
        if raw.strip():
            return {
                "questions": [{
                    "question_read": "",
                    "chapter": "Auto detected",
                    "confidence": 0,
                    "answer": raw.strip(),
                    "steps": [],
                    "final_answer": "",
                    "needs_clarification": True,
                    "clarification": "The AI response was not returned in the expected structured format.",
                    "verification": "",
                }],
                "page_summary": "",
                "overall_message": "The explanation was received but could not be formatted normally.",
            }
        raise RuntimeError("The AI returned an empty response.")

def _json_config():
    from google.genai import types
    # Keep this deliberately conservative for compatibility across SDK versions.
    return types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
    )

def _error_text(exc):
    return str(exc or "").lower()

def _status_code(exc):
    for attr in ("status_code", "code"):
        value = getattr(exc, attr, None)
        if isinstance(value, int):
            return value
    match = re.search(r"\b(408|429|500|502|503|504)\b", str(exc))
    return int(match.group(1)) if match else None

def _is_transient(exc):
    code = _status_code(exc)
    if code in {408, 429, 500, 502, 503, 504}:
        return True
    text = _error_text(exc)
    return any(x in text for x in (
        "unavailable", "service unavailable", "temporarily", "overloaded",
        "resource exhausted", "rate limit", "too many requests",
        "internal server error", "deadline exceeded", "timeout",
        "connection reset", "temporarily unavailable",
    ))

def _friendly_error(exc, attempted):
    code = _status_code(exc)
    if code == 503:
        return (
            "The AI service is temporarily busy (503). The app retried "
            f"automatically across {attempted} model attempt(s). Please try again shortly."
        )
    if code == 429:
        return (
            "The AI service rate limit was reached (429). The app retried "
            "automatically. Please wait a little and try again."
        )
    if code in {408, 504}:
        return "The AI request timed out. Please try again, or use a smaller image/video."
    if code in {400, 403}:
        return f"The AI request was rejected ({code}). Check the API key, model access, and request settings."
    return f"The AI service could not complete the request after automatic retries: {exc}"

def _generate_with_retry(client, contents):
    last_exc = None
    attempts = 0

    for model in MODEL_LIST:
        for retry_index in range(MAX_RETRIES_PER_MODEL + 1):
            try:
                attempts += 1
                response = client.models.generate_content(
                    model=model,
                    contents=contents,
                    config=_json_config(),
                )
                return response
            except Exception as exc:
                last_exc = exc
                if not _is_transient(exc):
                    raise RuntimeError(_friendly_error(exc, attempts)) from exc

                if retry_index >= MAX_RETRIES_PER_MODEL:
                    break

                delay = min(
                    30.0,
                    BASE_RETRY_SECONDS * (2 ** retry_index) + random.uniform(0, 0.6)
                )
                time.sleep(delay)

    raise RuntimeError(_friendly_error(last_exc, attempts))

def solve_with_ai(question, class_name="Class 11", chapters=None):
    question = (question or "").strip()
    if not question:
        raise ValueError("Please enter a maths question, statement, or word problem.")
    if len(question) > MAX_QUESTION_CHARS:
        raise ValueError(f"Question is too long. Maximum is {MAX_QUESTION_CHARS} characters.")

    client = _client()
    response = _generate_with_retry(
        client,
        _prompt(class_name, chapters or [], question, media_mode=False),
    )
    return _parse_response(response)

def solve_with_media(file_storage, question="", class_name="Class 11", chapters=None):
    if not file_storage or not getattr(file_storage, "filename", ""):
        raise ValueError("Please choose a photo, PDF, or short video first.")

    mime = (getattr(file_storage, "mimetype", "") or "").lower()
    if mime == "video/quicktime":
        mime = "video/mov"
    if mime not in ALLOWED_MIME:
        raise ValueError(
            "Unsupported file. Use JPG, PNG, WEBP, HEIC, PDF, MP4, MOV, WEBM, "
            "or another supported maths-page format."
        )

    data = file_storage.read()
    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise ValueError(f"File is too large. Maximum size is {MAX_UPLOAD_MB} MB.")
    if not data:
        raise ValueError("The uploaded file is empty.")

    if question and len(question.strip()) > MAX_QUESTION_CHARS:
        raise ValueError(f"Question text is too long. Maximum is {MAX_QUESTION_CHARS} characters.")

    try:
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("The AI package is missing. Run: pip install google-genai") from exc

    client = _client()
    media_part = types.Part.from_bytes(data=data, mime_type=mime)

    response = _generate_with_retry(
        client,
        [
            media_part,
            _prompt(class_name, chapters or [], question.strip(), media_mode=True),
        ],
    )
    return _parse_response(response)

def get_ai_configuration():
    """Useful for a health/debug endpoint without exposing the API key."""
    return {
        "configured": bool(os.getenv("GEMINI_API_KEY", "").strip()),
        "models": MODEL_LIST,
        "max_upload_mb": MAX_UPLOAD_MB,
        "max_retries_per_model": MAX_RETRIES_PER_MODEL,
    }
