"""`get_dietary_restrictions` — fake DB'den kullanıcının SADECE diyet kısıtlarını
ve sağlık durumlarını/alerjilerini çeker. Profil alanlarından ayrı tutulur ki
agent neyi ne zaman çektiğini seçebilsin (selektif erişim = az token).

Gerçekte kendi DB'nde ayrı bir tablo/sorgu olur; sözleşme: user_id → kısıtlar.
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
        "dietary_restrictions": u.get("dietary_restrictions", []),
        "health_conditions": u.get("health_conditions", []),
    }
