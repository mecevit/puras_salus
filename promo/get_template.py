"""promo.get_template — return the polished reference animation HTML.

The agent should START from this (a hand-tuned Claude-Design piece with the full
motion machinery: camera, morph, cursor, spark, gerund loader, dark reveal,
plan checklist, __BLUR_SEGMENTS__) and ADAPT it to the brief — keeping all the
CSS/JS machinery, changing only scene copy, labels, palette accent and timings.
"""
from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(**inputs) -> dict:
    return {"html": (HERE / "template.html").read_text(encoding="utf-8")}
