"""One-off (2026-09-28, second pass): polar CLAHE on slide 15, training parameters on slide 22, figure lines of 25 and R1.
Run from defense/presentation/slides."""
from pathlib import Path

LANGS = ("kk", "ru", "en")
REPL = {
"15-clahe": {
 "kk": [("# Жарықтандыруды түзету және бейімделгіш контраст теңестіру (CLAHE)", "# Жарықтандыруды түзету және полярлы CLAHE"),
        ("Бесінші кезең — CLAHE. CLAHE — кескіннің контрастын жергілікті деңгейде күшейтетін әдіс; ол LAB кеңістігінің жарықтық арнасында қолданылады. Клип-лимит гистограммаға және торкөзге қатысты екі шектеудің минимумы ретінде есептеледі, ал оқыту кезінде стохастикалық қолданылады.",
         "Бесінші кезең — полярлы CLAHE, LAB кеңістігінің жарықтық арнасында контрастты жергілікті күшейту әдісі. Ұяшықтар шаршы тор емес, көру алаңының ортасын айнала сақиналар мен секторлар: тамырлар тығыз жерде секторлар ұсағырақ, ал көрші секторлар арасында интерполяция жүргізіледі, сондықтан жіктер көрінбейді. Клип-лимит екі шектеудің минимумы ретінде есептеледі, оқыту кезінде кезең стохастикалық қолданылады.")],
 "ru": [("# Коррекция освещённости и адаптивный CLAHE", "# Коррекция освещённости и полярный CLAHE"),
        ("Пятый этап — CLAHE. CLAHE — метод локального усиления контраста; он применяется к каналу яркости пространства LAB. Клип-лимит вычисляется как минимум двух ограничений — по гистограмме и по ячейке — и при обучении применяется стохастически.",
         "Пятый этап — полярный CLAHE, метод локального усиления контраста на канале яркости LAB. Ячейки — не квадратная сетка, а кольца и секторы вокруг центра поля зрения: где сосудов больше, секторы мельче, а между соседними секторами — интерполяция, поэтому швов нет. Клип-лимит — минимум двух ограничений, при обучении этап применяется стохастически.")],
 "en": [("# Flat-field correction and adaptive CLAHE", "# Flat-field correction and polar CLAHE"),
        ("Stage five is CLAHE. CLAHE is a local contrast enhancement method, applied to the lightness channel of LAB space. The clip limit is computed as the minimum of two constraints — histogram- and tile-relative — and is applied stochastically in training.",
         "Stage five is polar CLAHE, local contrast enhancement on the lightness channel of LAB. Its cells are not a square grid but rings and sectors around the centre of the field of view: where vessels are denser the sectors are finer, and neighbouring sectors are interpolated, so no seams appear. The clip limit is the minimum of two constraints, and the stage is applied stochastically in training.")],
 "seconds": ("seconds: 30", "seconds: 35"),
},
"22-exp2": {
 "kk": [("клип-фактор 2,5, табалдырық 0,03, түзету масштабы 0,07.",
         "клип-фактор 2,5, табалдырық 0,03, түзету масштабы 0,07. Негізгі конфигурациялар клип-фактор 2,0 және табалдырық 0,01 мәндерімен оқытылған, яғни оптимумда емес, — олардың нәтижесі параметрлерді іріктеу есебінен асырылмаған.")],
 "ru": [("клип-фактор 2,5, порог 0,03, масштаб коррекции 0,07.",
         "клип-фактор 2,5, порог 0,03, масштаб коррекции 0,07. Основные конфигурации обучены при клип-факторе 2,0 и пороге 0,01, то есть не в оптимуме, — их результат не завышен подбором параметров.")],
 "en": [("clip factor 2.5, threshold 0.03, correction scale 0.07.",
         "clip factor 2.5, threshold 0.03, correction scale 0.07. The main configurations were trained at clip factor 2.0 and threshold 0.01, that is, off the optimum, so their result is not inflated by parameter tuning.")],
 "seconds": ("seconds: 35", "seconds: 40"),
},
}
LINE15 = {
"25-exp4": (
 "Суреттер: сол жақта — зақымдану түрлері бойынша ALO және ALO анықтамасы (`img/exp4_kk.png`); оң жақта — Grad-CAM жұбы: базалық · интеграцияланған · сарапшы маскасы, IDRiD_007 — томдағы D.1-сурет (`img/gradcam_kk.png`)",
 "Рисунки: слева — ALO по типам поражений и определение ALO (`img/exp4_ru.png`); справа — пара Grad-CAM: базовая · интегрированная · маска эксперта, IDRiD_007 — рис. D.1 тома (`img/gradcam_ru.png`)",
 "Figures: left — ALO by lesion type and the ALO definition (`img/exp4_en.png`); right — the Grad-CAM pair: baseline · integrated · expert mask, IDRiD_007 — fig. D.1 of the volume (`img/gradcam_en.png`)"),
"R1-limitations": (
 "Сурет: EfficientNet-B3, ДР дәрежелері бойынша F1 (`img/perclass_kk.png`)",
 "Рисунок: EfficientNet-B3, F1 по степеням ДР (`img/perclass_ru.png`)",
 "Figure: EfficientNet-B3, F1 by DR grade (`img/perclass_en.png`)"),
}

for d, spec in REPL.items():
    for lang in LANGS:
        p = Path(d) / f"{lang}.md"
        t = p.read_text(encoding="utf-8")
        for a, b in spec[lang] + [spec["seconds"]]:
            assert t.count(a) == 1, (p, a[:40])
            t = t.replace(a, b)
        p.write_text(t, encoding="utf-8")
for d, lines in LINE15.items():
    for lang, new in zip(LANGS, lines):
        p = Path(d) / f"{lang}.md"
        rows = p.read_text(encoding="utf-8").split("\n")
        assert rows[14].startswith(("Сурет", "Рисун", "Figure")), (p, rows[14])
        rows[14] = new
        p.write_text("\n".join(rows), encoding="utf-8")
print("ok")
