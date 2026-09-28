"""Assemble the defence speech and the analysis compendium from slides/NN-id/*.md.

Run:  python report/build.py
Out:  report/speech_kk.md, speech_ru.md, speech_en.md  — full talk, slide by slide, with timing
      report/ANALYSIS.md                                — all analysis.md in slide order
Slide files are the source; the outputs are rebuilt, never edited by hand.
Reserve slides (R1-…, shown only on a question) go after the talk and are left out of the timing.
"""
from __future__ import annotations

import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLIDES = HERE.parent / "slides"
WPM = 90  # median speech rate of the council's defences (council/ru/23-презентация-доклад/структура.md)
TITLE = {"kk": "Баяндама мәтіні", "ru": "Текст доклада", "en": "Defence talk"}
# Candidate's rule (2026-09-28): every approbation is mentioned on at least one slide, at most one per slide.
# Publications stand in the italic footer; a certificate / patent is its own scan slide (key in the on-slide text).
# Key = a string unique to the item. Add each patent here once it is granted (TODO.md §2).
APPROBATION = {
    "EEJET 2025 [Scopus Q3]": "Eastern-European J. of Enterprise Technologies",
    "Procedia CS 2025, DS-2025 Istanbul [Scopus]": "Procedia Computer Science, 2025 (DS-2025, Istanbul)",
    "Herald of KBTU 2025": "Herald of KBTU",
    "News of NAN RK 2025": "News of NAN RK",
    "Вестник КазУТБ": "Вестник КазУТБ",
}
SCANS = {"Свидетельство № 78109": "78109"}
FOOTER = re.compile(r"^\*\*(?:Төменде|Внизу|Bottom) \((?:курсив|italic)\):\*\* \*(.+)\*$", flags=re.M)


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


def build_speech(lang: str, dirs: list[Path], reserve: list[Path]) -> None:
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
    if reserve:
        parts.append("---\n\n# Резерв — только на вопрос, в бюджет не входит\n")
    for d in reserve:
        m = parse(d / f"{lang}.md")
        parts.append(f"## {d.name[:2]}. {m['title']}\n\n*{words(m['speech'])} слов*\n\n{m['speech']}\n")
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
    reserve = sorted(p for p in SLIDES.iterdir() if p.is_dir() and re.match(r"R\d-", p.name))
    for lang in ("kk", "ru", "en"):
        build_speech(lang, dirs, reserve)
    build_analysis(dirs + reserve)
    check_approbation(dirs)


def check_approbation(dirs: list[Path]) -> None:
    """Print where each approbation stands; exit non-zero if one is on no slide or a slide carries more than one."""
    errors = []
    for lang in ("kk", "ru", "en"):
        texts = {d.name[:2]: (d / f"{lang}.md").read_text(encoding="utf-8") for d in dirs if "publications" not in d.name}
        footers = {n: " ".join(FOOTER.findall(t)) for n, t in texts.items()}
        onslide = {n: t.split("## Речь", 1)[0] for n, t in texts.items()}
        where = {name: [n for n, f in footers.items() if key in f] for name, key in APPROBATION.items()}
        where |= {name: [n for n, s in onslide.items() if key in s] for name, key in SCANS.items()}
        for name, on in where.items():
            if lang == "kk":
                print(f"  {name}: сл. {', '.join(on) if on else '—'}")
            if not on:
                errors.append(f"{name} ни на одном слайде ({lang})")
        for n, f in footers.items():
            k = sum(key in f for key in APPROBATION.values())
            if k > 1:
                errors.append(f"сл. {n}: {k} работы в одной строке ({lang})")
    if errors:
        raise SystemExit("Апробация: " + "; ".join(errors))
    print(f"Апробация: все {len(APPROBATION) + len(SCANS)} на слайдах, по одной на слайд, в трёх языках")


if __name__ == "__main__":
    main()
