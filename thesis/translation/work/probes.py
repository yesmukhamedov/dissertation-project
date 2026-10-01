"""Errors Opus found by reading the c0 council translations, as probes: python work/probes.py c0 c1 ...
A probe fires when the wrong form is present (or the required form is absent) in that item's output."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval import COUNCIL_ITEMS, body_text
from lib import HERE

# (item, kind, regex, must_be_absent?, description)
PROBES = [
    ("gd01-ru-kz", "term", r"Бюро", True, "Офис послевузовского образования -> «Бюро»"),
    ("gd01-ru-kz", "meaning", r"ертіс", True, "гербовая печать -> nonsense «мемлекеттік ертіс»"),
    ("gd01-ru-kz", "term", r"Ережелер", True, "Правила -> «Ережелер» (must be Қағидалар)"),
    ("gd01-ru-kz", "term", r"ЗРК", True, "ЗРК kept in Kazakh (ҚРЗ)"),
    ("gd01-ru-kz", "term", r"аннотация", True, "аннотация not translated (аңдатпа)"),
    ("gd01-ru-kz", "format", r"(?m)^(кворум|диссертацияны|егер|қорғауға|кеңейтілген)", True, "paragraphs start lowercase"),
    ("gd01-ru-kz", "meaning", r"25\.05\.2026 жылғы|жылғы 25\.05", True, "date duplicated"),
    ("gd01-ru-kz", "meaning", r"PhD дәрежесін алуға арналған диссертацияны қорғау бойынша PhD", True, "first sentence duplicated"),
    ("gd01-kz-ru", "term", r"церемониал", True, "рәсім -> «церемониал»"),
    ("gd01-kz-ru", "term", r"[әғқңөұүһі]", True, "Kazakh letters left (Изденуші)"),
    ("gd01-kz-ru", "term", r"Научн\w+ совет", True, "Ғылыми кеңес -> «Научный совет» (Ученый совет)"),
    ("gd01-kz-ru", "term", r"представлени\w+ (диссертации )?на защиту|представляется на защиту", True, "қорғауға ұсыну -> «представление на защиту»"),
    ("bazarbekov-ru-kz", "meaning", r"Зерттеудің нысаны – оқыту|нысаны – оқыту", True, "предмет исследования rendered as нысан (object)"),
    ("bazarbekov-ru-kz", "term", r"машиналық оқу(?!ы)", True, "машиналық оқу (оқыту)"),
    ("bazarbekov-ru-kz", "term", r"\bБА\b|ИМУ", True, "Russian abbreviations БА/ИМУ kept"),
    ("bazarbekov-ru-kz", "term", r"нейросет|сверткал|рывок", True, "Russian calques нейросеттік/сверткалық/рывок"),
    ("bazarbekov-ru-kz", "meaning", r"қалаушы", True, "добровольцы -> «қалаушылар»"),
    ("bazarbekov-ru-kz", "meaning", r"жазу қолы", True, "почерк -> «жазу қолы»"),
    ("toktarova-kz-ru", "meaning", r"замен\w+ символ", True, "кодты ауыстыру -> «замена символов»"),
    ("toktarova-kz-ru", "meaning", r"ассоциированн", False, "қауымдастырылған профессор lost"),
    ("toktarova-kz-ru", "term", r"[әғқңөұүһі]", True, "Kazakh letters in names (Сұлтанұлы)"),
    ("bakirova-en-ru", "term", r"бенчмарк", True, "benchmark -> «бенчмаркинг»"),
    ("bazarbekov-ru-en", "meaning", r"\bIn conclusion\b", True, "В заключении (chapter) -> «In conclusion»"),
    ("bakirova-en-kz", "meaning", r"жанжал", True, "burnout -> «жанжал» (conflict)"),
    ("bakirova-en-kz", "meaning", r"білім беру орталықтар", True, "environments -> «орталықтар» (centres)"),
    ("bakirova-en-kz", "term", r"глобалды", True, "global -> «глобалды»"),
    ("bakirova-en-kz", "meaning", r"қарастырылсын", True, "broken sentence «... қарастырылсын»"),
    ("bakirova-kz-en", "meaning", r"educational cent", True, "орталарында -> «educational centres»"),
]


def run(tag):
    fired = []
    for item, kind, rx, absent, desc in PROBES:
        sl, tl = next((s, t) for i, d, s, t in COUNCIL_ITEMS if i == item)
        p = os.path.join(HERE, "work", "eval", tag, "council", f"{item}.{sl}.{tl}.md")
        if not os.path.exists(p):
            continue
        hit = bool(re.search(rx, body_text(p)))
        if hit == absent:
            fired.append((item, kind, desc))
    return fired


if __name__ == "__main__":
    for tag in sys.argv[1:]:
        f = run(tag)
        kinds = {k: sum(1 for x in f if x[1] == k) for k in ("meaning", "term", "format")}
        print(f"{tag}: {len(f)}/{len(PROBES)} probes fire  {kinds}")
        for x in f:
            print("   ", *x)
