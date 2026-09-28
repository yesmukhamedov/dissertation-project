"""Slide 02: rural ophthalmologists 20 % (inbusiness.kz, 2021) → ≈ 10 % (Semenova et al., Hum Resour Health 2026;
MoH RK: 156 rural of 1 610 in 2016). Run from defense/presentation/slides/02-relevance."""
from pathlib import Path

E = [
 ("kk.md", "офтальмологтардың 20 %-ы ғана ауылда жұмыс істейді.", "офтальмологтардың ≈ 10 %-ы ғана ауылда жұмыс істейді."),
 ("ru.md", "а работает лишь 20 % офтальмологов.", "а работает лишь ≈ 10 % офтальмологов."),
 ("en.md", "but only 20 % of ophthalmologists work in rural areas.", "but only ≈ 10 % of ophthalmologists work in rural areas."),
 ("kk.md", "офтальмологтардың бестен бірі ғана жұмыс істейді.", "офтальмологтардың оннан бірі ғана жұмыс істейді."),
 ("ru.md", "работает лишь пятая часть офтальмологов.", "работает лишь десятая часть офтальмологов."),
 ("en.md", "only a fifth of ophthalmologists work.", "only a tenth of ophthalmologists work."),
 ("kk.md", "ҚР ДСМ (2026); ҚР СЖРА ҰСБ (2026).*", "ҚР ДСМ (2026); Semenova Y. et al., Hum Resour Health, 2026; ҚР СЖРА ҰСБ (2026).*"),
 ("ru.md", "МЗ РК (2026); БНС АСПиР РК (2026).*", "МЗ РК (2026); Semenova Y. et al., Hum Resour Health, 2026; БНС АСПиР РК (2026).*"),
 ("en.md", "MoH RK (2026); Bureau of National Statistics RK (2026).*", "MoH RK (2026); Semenova Y. et al., Hum Resour Health, 2026; Bureau of National Statistics RK (2026).*"),
 ("img/make_charts.py", "    labels, vals, cols = [t[\"oph\"], t[\"pop\"]], [20, 36], [BLUE, GRAY]",
  "    # rural ophthalmologists: 156 of 1 610 (2016), MoH RK via Semenova et al., Hum Resour Health 2026;24:8 → 9.7 %\n"
  "    labels, vals, cols = [t[\"oph\"], t[\"pop\"]], [10, 36], [BLUE, GRAY]"),
 ("img/make_charts.py", "        ax.text(v + 1, y, f\"{v} %\", va=\"center\", color=INK, fontweight=\"bold\")",
  "        ax.text(v + 1, y, (\"≈ \" if y == 0 else \"\") + f\"{v} %\", va=\"center\", color=INK, fontweight=\"bold\")"),
]
for f, a, b in E:
    p = Path(f)
    t = p.read_text(encoding="utf-8")
    assert t.count(a) == 1, (f, a[:40])
    p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
