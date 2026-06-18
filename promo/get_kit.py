"""promo.get_kit — return the craft KIT (tokens + boilerplate + components).

Deliberately contains NO finished scene flow: the model composes its own timeline
from the brief's concept, lifting the kit's tokens, helpers and components.
"""
from __future__ import annotations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def run(**inputs) -> dict:
    return {"kit": (HERE / "kit.md").read_text(encoding="utf-8")}
