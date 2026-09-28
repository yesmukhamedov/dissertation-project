"""Assemble the defence speech and the analysis compendium from slides/NN-id/*.md.

Run:  python report/build.py
Out:  report/speech_kk.md, speech_ru.md, speech_en.md  — full talk, slide by slide, with timing
      report/ANALYSIS.md                                — all analysis.md in slide order
Slide files are the source; the outputs are rebuilt, never edited by hand.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDES = HERE.parent / "slides"
WPM = 90  # median speech rate of the council's defences (council/ru/23-презентация-доклад/структура.md)
TITLE = {"kk": "Баяндама мәтіні", "ru": "Текст доклада", "en": "Defence talk"}


def parse(path: Path) -> dict[str, str]:
    """Split a slide file into front matter fields, title, on-slide text and speech."""
    text = path.read_text(encoding="utf-8")
    fm, body = text.split("---", 2)[1:]
    meta = dict(re.findall(r"^(\w+): (.*)$", fm, flags=re.M))
    meta["title"] = re.search(r"^# (.+)$", body, flags=re.M).group(1)
    meta["speech"] = body.split("## Речь", 1)[1].strip()
    return meta


def words(s: str) -> int:
    return len(re.findall(r"\w+", s))


def build_speech(lang: str, dirs: list[Path]) -> None:
    rows, parts, total_s, total_w = [], [], 0, 0
    for d in dirs:
        m = parse(d / f"{lang}.md")
        sec, w = int(m["seconds"]), words(m["speech"])
        total_s += sec
        total_w += w
        rows.append(f"| {d.name[:2]} | {m['title']} | {sec} | {w} | {round(w / WPM * 60)} |")
        parts.append(f"## {d.name[:2]}. {m['title']}\n\n*{sec} с · {w} слов*\n\n{m['speech']}\n")
    head = [f"# {TITLE[lang]}", "",
            f"Собрано из `slides/*/{lang}.md` скриптом `report/build.py`. Не править руками.", "",
            f"**Итого:** {len(dirs)} слайдов · бюджет {total_s} с ({total_s / 60:.1f} мин) · {total_w} слов · "
            f"при {WPM} сл/мин ≈ {total_w / WPM:.1f} мин · регламент 20 мин", "",
            "| № | Слайд | Бюджет, с | Слов | При 90 сл/мин, с |", "|---|---|---|---|---|", *rows, ""]
    (HERE / f"speech_{lang}.md").write_text("\n".join(head) + "\n" + "\n".join(parts), encoding="utf-8")
    print(f"speech_{lang}.md: {total_w} words, {total_w / WPM:.1f} min, budget {total_s / 60:.1f} min")


def build_analysis(dirs: list[Path]) -> None:
    out = ["# Сводка решений по слайдам", "",
           "Все `slides/*/analysis.md` подряд. Собрано `report/build.py`, не править руками.", ""]
    for d in dirs:
        a = (d / "analysis.md").read_text(encoding="utf-8").strip()
        out += [re.sub(r"^# ", "## ", a, count=1).replace("\n## ", "\n### "), ""]
    (HERE / "ANALYSIS.md").write_text("\n".join(out), encoding="utf-8")
    print("ANALYSIS.md:", len(dirs), "slides")


def main() -> None:
    dirs = sorted(p for p in SLIDES.iterdir() if p.is_dir() and re.match(r"\d\d-", p.name))
    for lang in ("kk", "ru", "en"):
        build_speech(lang, dirs)
    build_analysis(dirs)


if __name__ == "__main__":
    main()
