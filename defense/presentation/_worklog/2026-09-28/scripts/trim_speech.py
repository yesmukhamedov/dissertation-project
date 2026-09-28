"""Trim the kk/ru/en speech of slide 15 (whole paragraph) and the added sentence of slide 22. Run from slides/."""
from pathlib import Path

S15 = {
 "kk": "Төртінші кезең жарықтандыруды теңестіреді: кескіннен оның бұлдыратылған көшірмесі алынады, масштабы — көру "
       "алаңы диаметрінің 0,07 үлесі. Бесінші кезең — полярлы CLAHE: контраст фовеаны айнала сақиналар мен "
       "секторларда жергілікті күшейтіледі, тамырлар тығыз жерде секторлар ұсағырақ; клип-лимит — екі шектеудің "
       "минимумы. Нәтижесінде ұсақ тамырлар мен микроаневризмалар — ретинопатияның ерте белгілері — анық көрінеді.",
 "ru": "Четвёртый этап выравнивает освещённость: из снимка вычитается его размытая копия, масштаб — 0,07 диаметра "
       "поля зрения. Пятый этап — полярный CLAHE: контраст усиливается локально в кольцах и секторах вокруг фовеа, "
       "где сосудов больше — секторы мельче; клип-лимит — минимум двух ограничений. В итоге чётко видны мелкие "
       "сосуды и микроаневризмы — ранние признаки ретинопатии.",
 "en": "Stage four evens out the illumination: a blurred copy is subtracted from the image, at a scale of 0.07 of the "
       "field-of-view diameter. Stage five is polar CLAHE: contrast is enhanced locally in rings and sectors around "
       "the fovea, finer where vessels are denser; the clip limit is the minimum of two constraints. Fine vessels and "
       "microaneurysms — the early signs of retinopathy — become clearly visible.",
}
S22 = {
 "kk": ("Негізгі конфигурациялар клип-фактор 2,0 және табалдырық 0,01 мәндерімен оқытылған, яғни оптимумда емес, — "
        "олардың нәтижесі параметрлерді іріктеу есебінен асырылмаған.",
        "Негізгі конфигурациялар 2,0 және 0,01 мәндерімен оқытылған — оптимумда емес, сондықтан нәтиже іріктеумен асырылмаған."),
 "ru": ("Основные конфигурации обучены при клип-факторе 2,0 и пороге 0,01, то есть не в оптимуме, — их результат не "
        "завышен подбором параметров.",
        "Основные конфигурации обучены при 2,0 и 0,01 — не в оптимуме, так что результат не завышен подбором."),
 "en": ("The main configurations were trained at clip factor 2.0 and threshold 0.01, that is, off the optimum, so their "
        "result is not inflated by parameter tuning.",
        "The main configurations were trained at 2.0 and 0.01 — off the optimum, so the result is not inflated by tuning."),
}
for lang, text in S15.items():
    p = Path("15-clahe") / f"{lang}.md"
    t = p.read_text(encoding="utf-8")
    head, _ = t.split("## Речь", 1)
    p.write_text(head + "## Речь\n\n" + text + "\n", encoding="utf-8")
for lang, (a, b) in S22.items():
    p = Path("22-exp2") / f"{lang}.md"
    t = p.read_text(encoding="utf-8")
    assert t.count(a) == 1, (p, a[:40])
    p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
