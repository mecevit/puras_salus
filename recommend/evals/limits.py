"""`usable_tips` — deterministic check grader for the `recommend` skill's
tip-based output. Runs after every job (and in the offline suite). Asserts the
tips are well-formed and showable to a user.

Grader contract: called with (inputs, output); returns
{"score": float, "passed": bool, "detail": str}.
"""

from __future__ import annotations

ALLOWED_CATEGORIES = {"nutrition", "hydration", "activity", "supplement", "habit", "sleep"}


def grade(inputs: dict, output: dict) -> dict:
    output = output or {}
    issues = []

    tips = output.get("tips")
    if not isinstance(tips, list) or not (3 <= len(tips) <= 5):
        issues.append(f"tips count not 3-5: {len(tips) if isinstance(tips, list) else tips!r}")
    else:
        seen_titles = set()
        for i, t in enumerate(tips):
            if not isinstance(t, dict):
                issues.append(f"tip[{i}] not an object")
                continue
            if t.get("category") not in ALLOWED_CATEGORIES:
                issues.append(f"tip[{i}] bad category: {t.get('category')!r}")
            title = (t.get("title") or "").strip()
            detail = (t.get("detail") or "").strip()
            if not title:
                issues.append(f"tip[{i}] empty title")
            if len(detail) < 10:
                issues.append(f"tip[{i}] detail too short")
            key = title.lower()
            if key and key in seen_titles:
                issues.append(f"tip[{i}] duplicate title within batch: {title!r}")
            seen_titles.add(key)

    if not (output.get("headline") or "").strip():
        issues.append("empty headline")
    if not (output.get("disclaimer") or "").strip():
        issues.append("empty disclaimer")
    if not (output.get("user_id") or "").strip():
        issues.append("missing user_id echo")

    passed = not issues
    return {
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "detail": "ok" if passed else "; ".join(issues),
    }
