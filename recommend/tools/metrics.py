"""`compute_metrics` — deterministik sağlık metrikleri.

Salus'un sayısal omurgası. Agent bu tool'u her run'da bir kez çağırır ve dönen
değerleri (BMI, BMR, TDEE, günlük kalori hedefi, su, protein) çıktısında aynen
kullanır — modele sayı "uydurtmayız". Saf stdlib, harici bağımlılık yok; bu
yüzden requirements.txt gerekmez.

Tool entrypoint sözleşmesi: fonksiyonun parametreleri skill.yaml'daki tool
`input_schema` alanlarıdır; dönüş, `output_schema` şeklinde bir dict'tir.
"""

from __future__ import annotations

# Haftalık aktivite seviyesi → TDEE çarpanı (yaygın Mifflin-St Jeor pratiği).
ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

# Hedefe göre günlük kalori ayarı (TDEE'ye eklenir/çıkarılır).
GOAL_CALORIE_DELTA = {
    "lose_weight": -500,   # ~0.45 kg/hafta açık
    "gain_muscle": +300,   # kontrollü fazlalık
    "maintain": 0,
    "improve_energy": 0,
    "general_health": 0,
}

# Hedefe göre günlük protein hedefi (g / kg vücut ağırlığı).
GOAL_PROTEIN_PER_KG = {
    "lose_weight": 1.8,    # kas korumak için yüksek protein
    "gain_muscle": 2.0,
    "maintain": 1.6,
    "improve_energy": 1.4,
    "general_health": 1.4,
}

# Güvenli minimum günlük kalori tabanı (cinsiyete göre).
CALORIE_FLOOR = {"male": 1500, "female": 1200}


def _bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "underweight"
    if bmi < 25:
        return "normal"
    if bmi < 30:
        return "overweight"
    return "obese"


def run(
    sex: str,
    age: int,
    height_cm: float,
    weight_kg: float,
    activity_level: str,
    goal: str,
) -> dict:
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m * height_m)

    # Mifflin-St Jeor BMR (dinlenme metabolizma hızı).
    bmr = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age
    bmr += 5.0 if sex == "male" else -161.0

    tdee = bmr * ACTIVITY_FACTORS.get(activity_level, 1.2)

    target = tdee + GOAL_CALORIE_DELTA.get(goal, 0)
    target = max(target, CALORIE_FLOOR.get(sex, 1200))  # güvenli alt sınır

    # Günlük su: ~35 ml/kg; yoğun aktivitede +500 ml. 50 ml'ye yuvarla, 1500–5000 ml'ye sıkıştır.
    water = weight_kg * 35.0
    if activity_level in ("active", "very_active"):
        water += 500.0
    water = max(1500.0, min(5000.0, water))
    water_ml = int(round(water / 50.0) * 50)

    protein_g = weight_kg * GOAL_PROTEIN_PER_KG.get(goal, 1.4)

    return {
        "bmi": round(bmi, 1),
        "bmi_category": _bmi_category(bmi),
        "bmr_kcal": int(round(bmr)),
        "tdee_kcal": int(round(tdee)),
        "target_calories_kcal": int(round(target)),
        "water_ml": water_ml,
        "protein_target_g": int(round(protein_g)),
    }
