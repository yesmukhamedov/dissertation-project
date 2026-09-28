"""Normalise the figure lines of slides 02, 15, 32 for numbering; slide 02 rural share 20 % → ≈ 10 %. Run from slides/."""
from pathlib import Path

E = [
 ("02-relevance/kk.md", "**Графиктер:** `img/chart1_kk.png` — есепте тұрған қант диабеті науқастары, 2014–2024; `img/chart2_kk.png` — ауылдағы үлес: халық 36 % / офтальмологтар 20 %.",
  "Суреттер: есепте тұрған қант диабеті науқастары, 2014–2024 (`img/chart1_kk.png`); ауылдағы үлес: халық 36 % / офтальмологтар ≈ 10 % (`img/chart2_kk.png`)"),
 ("02-relevance/ru.md", "**Графики:** `img/chart1_ru.png` — больные сахарным диабетом на учёте, 2014–2024; `img/chart2_ru.png` — доля на селе: население 36 % / офтальмологи 20 %.",
  "Рисунки: больные сахарным диабетом на учёте, 2014–2024 (`img/chart1_ru.png`); доля на селе: население 36 % / офтальмологи ≈ 10 % (`img/chart2_ru.png`)"),
 ("02-relevance/en.md", "**Charts:** `img/chart1_en.png` — registered diabetes patients, 2014–2024; `img/chart2_en.png` — rural share: population 36 % / ophthalmologists 20 %.",
  "Figures: registered diabetes patients, 2014–2024 (`img/chart1_en.png`); rural share: population 36 % / ophthalmologists ≈ 10 % (`img/chart2_en.png`)"),
 ("15-clahe/kk.md", "→ 5-кезең, CLAHE (`img/stages45_kk.png`)", "→ 5-кезең, полярлы CLAHE (`img/stages45_kk.png`)"),
 ("15-clahe/ru.md", "→ этап 5, CLAHE (`img/stages45_ru.png`)", "→ этап 5, полярный CLAHE (`img/stages45_ru.png`)"),
 ("15-clahe/en.md", "→ stage 5, CLAHE (`img/stages45_en.png`)", "→ stage 5, polar CLAHE (`img/stages45_en.png`)"),
 ("32-certificate/kk.md", "Скан куәлігінің (`img/certificate_kz.png`), бір слайдқа бір құжат. Қолтаңба: «№ 78109, 04.09.2026 — бағдарламалық кешен»",
  "Сурет: авторлық құқық объектісіне құқықтарды тіркеу туралы куәлік № 78109, 04.09.2026 — бағдарламалық кешен (`img/certificate_kz.png`); бір слайдқа бір құжат"),
 ("32-certificate/ru.md", "Скан свидетельства (`img/certificate_ru.png` или kk), один документ на слайд. Подпись: «№ 78109 от 04.09.2026 — программный комплекс»",
  "Рисунок: свидетельство о внесении сведений в госреестр прав на объекты авторского права № 78109 от 04.09.2026 — программный комплекс (`img/certificate_ru.png`); один документ на слайд"),
 ("32-certificate/en.md", "Scan of the certificate (`img/certificate_kz.png`), one document per slide. Caption: \"No. 78109, 04.09.2026 — software package\"",
  "Figure: certificate of registration of copyright No. 78109, 04.09.2026 — software package (`img/certificate_kz.png`); one document per slide"),
]
for f, a, b in E:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    assert t.count(a) == 1, (f, a[:40])
    p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
