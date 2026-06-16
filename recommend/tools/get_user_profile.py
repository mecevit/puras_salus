"""`get_user_profile` — fake DB'den TEK bir kullanıcının SADECE profil alanlarını
çeker (demografi + hedef + aktivite + ilerleme). Diyet/sağlık bilgisi ayrı
tool'da (`get_dietary_restrictions`).

Demo'nun ana fikri: LLM'e tüm kullanıcı kaydını dökmek yerine, agent sadece
ihtiyacı olan alanları tipli bir tool ile çeker → çok daha az token.

Gerçekte burası kendi DB'ne (Postgres, Supabase, vb.) bir sorgu olur; sözleşme
aynı: user_id → profil. Veri `__file__` üzerinden çözülür, cwd'den bağımsız.
"""

from __future__ import annotations

import json
from pathlib import Path


def _user(user_id: str) -> dict:
    path = Path(__file__).resolve().parent.parent / "data" / "users.json"
    users = json.loads(path.read_text(encoding="utf-8"))
    u = users.get((user_id or "").strip())
    if not u:
        raise ValueError(f"unknown user_id: {user_id!r}")
    return u


def run(user_id: str) -> dict:
    u = _user(user_id)
    return {
        "name": u.get("name", ""),
        "age": u["age"],
        "sex": u["sex"],
        "height_cm": u["height_cm"],
        "weight_kg": u["weight_kg"],
        "goal": u["goal"],
        "activity_level": u["activity_level"],
        "target_weight_kg": u.get("target_weight_kg"),
        "locale": u.get("locale", "tr"),
        "progress": u.get("progress", []),
    }
