"""Собрать экспертные отзывы практикующих офтальмологов на демонстрацию приложения.

Отзыв — жанр `council/en/16-review`: связная проза на бланке медицинской
организации, без печатных заголовков и нумерованных разделов. Документ состоит
из четырёх частей, разделённых визуально, а не заголовками:

    1. шапка — что это за бумага и что за приложение;
    2. протокол демонстрации — что и как было показано (у всех врачей дословно
       одинаков, различаются только дата и организация);
    3. слово офтальмолога — один из вариантов `voice_*_ru.md`;
    4. данные офтальмолога — безрамочный блок подписи.

Части 1 и 2 занимают первую страницу, части 3 и 4 — вторую; разрыв страницы
поставлен в шаблоне явно.

Данные врачей берутся из `ophthalmologists.toml` (единственный файл, который
правит кандидат). Данные докторанта, тема диссертации и образовательная
программа НЕ дублируются в нём: они читаются из `council/METADATA.toml`, поэтому
дословность реестра гарантируется построением, а не последующей сверкой.

Незаполненное поле превращается в плейсхолдер `<…>`, так что документ остаётся
пригодным для распечатки и заполнения от руки, пока врачи не названы.

Использование:
    python defense/docs/reviews/expert/build_expert_reviews.py
    python defense/docs/reviews/expert/build_expert_reviews.py --only 2
    python defense/docs/reviews/expert/build_expert_reviews.py --no-pdf
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent

ROOT = HERE
while ROOT.parent != ROOT and not (ROOT / "defense").is_dir():
    ROOT = ROOT.parent

REGISTRY = ROOT / "council/METADATA.toml"
DATA = HERE / "ophthalmologists.toml"
TEMPLATE = HERE / "template_ru.md"
MD2GOST = ROOT / ".claude/skills/council-docs/scripts/md2gost.py"

# Отзыв рассчитан ровно на две страницы: первая — что за бумага и что показали,
# вторая — слово врача и подпись. Без этой проверки бюджет молча уезжает при
# каждой правке текста, а трёхстраничный отзыв на бланке выглядит неряшливо.
EXPECTED_PAGES = 2

VARIANTS = {
    "screening": "voice_screening_ru.md",
    "interpretability": "voice_interpretability_ru.md",
}

# Как отзыв называет докторанта. Слово задаётся на врача, а не на весь комплект:
# два разных специалиста естественно пишут по-разному, и это заодно снимает
# дословное совпадение протокола демонстрации в двух отзывах. Внутри одного
# документа слово всегда одно — один человек не может называться двумя.
ROLES = {
    "докторант":     {"nom": "докторант",     "dat": "докторанту",     "ins": "докторантом"},
    "соискатель":    {"nom": "соискатель",    "dat": "соискателю",     "ins": "соискателем"},
    "исследователь": {"nom": "исследователь", "dat": "исследователю",  "ins": "исследователем"},
}

_MONTHS = (
    "января", "февраля", "марта", "апреля", "мая", "июня",
    "июля", "августа", "сентября", "октября", "ноября", "декабря",
)

_PAGE = re.compile(rb"/Type\s*/Page[^s]")


def renderer_python() -> str:
    """Интерпретатор, которым запускать md2gost.py.

    Скрипт часто запускают из активированного окружения демо (`demo/.venv`), где
    python-docx не установлен, — тогда `sys.executable` для рендера не годится.
    Берём первый интерпретатор, которому виден docx: сначала текущий, затем
    лаунчер `py -3` и `python`/`python3` с PATH.
    """
    candidates = [[sys.executable]]
    launcher = shutil.which("py")
    if launcher:
        candidates.append([launcher, "-3"])
    for name in ("python", "python3"):
        found = shutil.which(name)
        if found and found != sys.executable:
            candidates.append([found])
    for cmd in candidates:
        probe = subprocess.run(cmd + ["-c", "import docx"], capture_output=True)
        if probe.returncode == 0:
            return cmd
    raise SystemExit(
        "не найден интерпретатор с python-docx — он нужен md2gost.py. "
        "Установите его в текущее окружение: pip install python-docx"
    )


def resolve(reg: dict, dotted: str) -> str:
    """Достать значение реестра по точечному пути ("candidate.name_ru_gen")."""
    node = reg
    for part in dotted.split("."):
        node = node[part]
    return str(node)


def russian_date(iso: str) -> str:
    """ISO-дату привести к «1 сентября 2026 года»; пустую — к плейсхолдеру."""
    if not iso.strip():
        return "<дата>"
    try:
        year, month, day = (int(x) for x in iso.strip().split("-"))
        return f"{day} {_MONTHS[month - 1]} {year} года"
    except (ValueError, IndexError):
        raise SystemExit(f"demo_date «{iso}» — ожидается формат ГГГГ-ММ-ДД")


def signatory(doc: dict) -> str:
    """Левая колонка блока подписи: должность, категория, степень — и организация.

    Части первой строки соединяются запятыми без согласования — та же форма, что
    в блоке подписи протокола предзащиты («Заведующая кафедрой …, PhD,
    ассоциированный профессор»). Незаполненные необязательные поля исчезают
    целиком, а не печатаются пустой строкой.

    Стажа здесь нет намеренно: кандидат убрал его из оформления 2026-09-05.
    """
    head = [doc.get("position", "").strip() or "<должность>"]
    for optional in ("category", "degree"):
        if doc.get(optional, "").strip():
            head.append(doc[optional].strip())
    org = doc.get("organization", "").strip() or "<полное наименование медицинской организации>"
    line = ", ".join(head)
    return f"{line[:1].upper()}{line[1:]},<br>{org}"


def build(doc: dict, reg: dict, template: str, *, renderer: list[str] | None) -> tuple[Path, int | None]:
    slug = str(doc["slug"]).strip()
    variant = doc.get("variant", "").strip()
    if variant not in VARIANTS:
        raise SystemExit(
            f"врач {slug}: variant «{variant}» неизвестен; допустимы "
            + ", ".join(sorted(VARIANTS))
        )
    voice = (HERE / VARIANTS[variant]).read_text(encoding="utf-8").strip()

    role = doc.get("role", "").strip()
    if role not in ROLES:
        raise SystemExit(
            f"врач {slug}: role «{role}» неизвестна; допустимы " + ", ".join(ROLES)
        )
    forms = ROLES[role]

    text = template.replace("{{VOICE}}", voice)
    for token, value in {
        # Тема диссертации в отзыве намеренно не приводится: отзыв говорит о
        # продемонстрированном приложении, а не о работе, — поэтому
        # dissertation.title_ru здесь не подставляется и не сверяется.
        "{{CANDIDATE_GEN}}": resolve(reg, "candidate.name_ru_gen"),
        "{{PROGRAMME_CODE}}": resolve(reg, "programme.code"),
        "{{PROGRAMME_RU}}": resolve(reg, "programme.name_ru"),
        "{{DATE}}": russian_date(doc.get("demo_date", "")),
        "{{ORG}}": doc.get("organization", "").strip() or "<наименование медицинской организации>",
        "{{FIO}}": doc.get("fio", "").strip() or "<Фамилия И.О.>",
        "{{SIGNATORY}}": signatory(doc),
        "{{ROLE_NOM}}": forms["nom"],
        "{{ROLE_DAT}}": forms["dat"],
        "{{ROLE_INS}}": forms["ins"],
        "{{ROLE_INS_CAP}}": forms["ins"].capitalize(),
    }.items():
        text = text.replace(token, value)

    left = re.findall(r"\{\{[A-Z_]+\}\}", text)
    if left:
        raise SystemExit(f"врач {slug}: в шаблоне остались подстановки {sorted(set(left))}")

    md = HERE / f"expert_review_{slug}_ru.md"
    md.write_text(text, encoding="utf-8")
    if renderer is None:
        return md, None

    docx = md.with_suffix(".docx")
    subprocess.run(
        renderer + [str(MD2GOST), str(md), "-o", str(docx), "--pdf",
                    "--no-page-numbers", "--highlight-placeholders"],
        check=True, cwd=ROOT,
    )
    pdf_path = md.with_suffix(".pdf")
    if not pdf_path.is_file():
        raise SystemExit(f"врач {slug}: md2gost не выдал {pdf_path.name}")
    return md, len(_PAGE.findall(pdf_path.read_bytes()))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--only", metavar="SLUG", help="собрать отзыв одного врача")
    ap.add_argument("--no-pdf", action="store_true", help="только .md, без .docx/.pdf")
    args = ap.parse_args()

    reg = tomllib.loads(REGISTRY.read_text(encoding="utf-8"))
    docs = tomllib.loads(DATA.read_text(encoding="utf-8"))["ophthalmologist"]
    if args.only:
        docs = [d for d in docs if str(d["slug"]) == args.only]
        if not docs:
            raise SystemExit(f"врача со slug «{args.only}» нет в {DATA.name}")

    template = TEMPLATE.read_text(encoding="utf-8")
    renderer = None if args.no_pdf else renderer_python()
    overflow = []
    for doc in docs:
        md, pages = build(doc, reg, template, renderer=renderer)
        body = len(md.read_text(encoding="utf-8"))
        if pages is None:
            print(f"{md.name}  вариант {doc['variant']}  {body} знаков  (без PDF)")
            continue
        mark = "" if pages == EXPECTED_PAGES else "  ← НЕ ДВЕ СТРАНИЦЫ"
        print(f"{md.name}  вариант {doc['variant']}  {body} знаков  {pages} стр.{mark}")
        if pages != EXPECTED_PAGES:
            overflow.append(md.name)

    if overflow:
        print(
            f"\nОтзыв рассчитан ровно на {EXPECTED_PAGES} страницы; не уложились: "
            + ", ".join(overflow)
            + ".\nПравить нужно слово врача (voice_*_ru.md), а не протокол демонстрации.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
