# Salus — sağlık öneri skillpack'i (Puras)

Bir sağlık uygulaması için **2 günde bir** kişisel öneriler üreten Puras
skillpack'i. API'ye **yalnızca bir `user_id`** gider; skill gerisini kendi yapar:

- Kullanıcının profilini ve diyet kısıtlarını DB'den **tipli tool'larla** (yalnız
  gereken alanlar) çeker — LLM'e tüm kaydı dökmek yerine, çok daha az token.
- Sayıları **deterministik** hesaplar (BMI, BMR/TDEE, kalori, su, protein).
- Önceki önerileri **workspace memory**'den hatırlar ve **tekrarlamadan** yeni
  ipuçları üretir; ürettiklerini tekrar memory'ye yazar.

> Demo amaçlı: `recommend/data/users.json` sahte bir kullanıcı DB'sidir. Gerçekte
> tool'lar kendi DB'nize (Postgres/Supabase) bağlanır; sözleşme aynı kalır.

## Yapı

```
salus/
  puras.yaml                       # pack manifest (slug: salus)
  recommend/
    skill.yaml                     # input(user_id) / output(tips) + tool'lar + evals
    SKILL.md                       # agentic pipeline (sistem promptu)
    data/users.json                # sahte kullanıcı DB'si (demo)
    tools/
      get_user_profile.py          # DB'den profil (sadece gerekli alanlar)
      get_dietary_restrictions.py  # DB'den diyet/sağlık kısıtları
      metrics.py                   # compute_metrics — deterministik metrikler
    evals/
      limits.py                    # usable_tips check grader
      cases.jsonl                  # test kullanıcıları
```

Geçmiş tutma/tekrar-etmeme için Puras'ın built-in `memory_search` / `memory_put`
tool'ları kullanılır (skill.yaml'da ayrıca tanımlanmaz).

## Pipeline (SKILL.md)

1. `get_user_profile(user_id)` → profil
2. `get_dietary_restrictions(user_id)` → kısıtlar
3. `compute_metrics(...)` → sayılar
4. `memory_search(kind=recommendation_history, key=user_id)` → geçmiş öneriler
5. Geçmişi tekrar etmeyen 3–5 yeni ipucu üret
6. `memory_put(...)` → bu döngüyü kaydet
7. `set_output(user_id, headline, tips, disclaimer)`

## Deploy

`puras` CLI ile (`pip install puras`):

```bash
puras login            # veya: export PURAS_API_KEY=puras_live_...
puras deploy           # 'salus' skillpack'i yoksa otomatik oluşturulur
```

## Çağırma

```bash
# CLI (uzun job'lar için async + logs)
puras run recommend --async --json '{"user_id":"u_1001"}'
puras logs <job_id>
```

HTTP / SDK ile (`workspace/salus/recommend` ya da skillpack_id):

```bash
curl -X POST "https://api.puras.co/v1/jobs?skillpack=<workspace>/salus" \
  -H "Authorization: Bearer puras_pub_<...>" \
  -H "Content-Type: application/json" \
  -d '{"skill":"recommend","inputs":{"user_id":"u_1001"}}'
```

Çıktının `output` alanı `{ user_id, headline, tips[], disclaimer }` döner.

> Not: Genel sağlık/beslenme bilgisi verir; tıbbi tavsiye değildir. Çıktıdaki
> `disclaimer` kullanıcıya gösterilmelidir.
