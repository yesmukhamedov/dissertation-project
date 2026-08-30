---
name: abstract-annotation-alignment
description: thesis/output abstracts (EN/RU/KZ) rewritten 2026-08-23 to the measured corpus genre — run-in rubrics, flowing prose, EN 7 / RU 8 / KZ 8 pp; content current against the rebuilt volume (113 pp / 19 tables / 16 figures / 102 sources)
metadata:
  type: project
---

The trilingual аннотация/abstract (`thesis/output/abstract_{en,ru,kz}.md`) was aligned on
2026-06-18 to the **real authorefarat samples** of IITU doctoral candidates in
`D:/phd/council/Образцы документов/авторы/` (Tokhtakhunov, Daurenbayeva, et al.),
**not just** the council template `council/en/11-abstract-annotation/structure.md`. The template
diverged from what candidates actually submit — trust the real samples for the section set/order.

Canonical structure now (all 3 languages, kept fully parallel — 20 `##` sections, identical order):
title (`# ABSTRACT` / `# АННОТАЦИЯ` / `# АҢДАТПА` — **no "(АВТОРЕФЕРАТ)"**) + bold descriptor →
General characteristics of the research → Relevance → Aim → Objectives → Object → Subject →
Methodology and methods → Empirical (experimental) basis → Scientific novelty → Main results →
Statements for defense → Theoretical significance → Practical significance → Reliability →
Approbation + connection with scientific programmes → **Publications (with the numbered works list
folded inline)** → Main content of the work (chapter overview) → Author's personal contribution →
**ends on Structure and length of the dissertation**.

Removed as отсебятина / template-isms that real samples don't have (flagged by the candidate):
- `(АВТОРЕФЕРАТ)` subtitle (was pre-existing in RU/KZ, not from samples).
- Umbrella `# GENERAL CHARACTERISTICS OF THE WORK` heading.
- Separate `# CONCLUSION` / `ЗАКЛЮЧЕНИЕ` / `ҚОРЫТЫНДЫ` section.
- Trailing standalone `LIST OF PUBLISHED WORKS` section (list moved into Publications, in the body).

Content added per samples + real RK normative docs: state-programmes (AI Concept 2024–2029,
President's Address «Kazakhstan in the Era of AI» 8 Sep 2025, Law «On AI» No. 230-VIII 17 Nov 2025,
Law «On Science» art. 20); "Author's personal contribution" section; "General characteristics" lead
para. KZ terminology fixed: Latin "pipeline" → "конвейер" (correct case forms; sentence-start caps).

Build via [[council-docs-skill]] → `defense/docs/abstracts/`. (The Scopus percentile, outstanding
here for months, was closed on 2026-08-23 — see the last section.)
NOTE: `defense/docs/**/*.docx` lock if open in Word — close before rebuild.

## Currency pass against the finished manuscript — 2026-08-13

The abstracts were resynchronised against the approved Chapter-0 sections (§0.2–§0.16) and §7, which are
authoritative; **six factual defects** were fixed, in all three languages at the same line positions:
1. **The Aim asserted its own result** ("producing a statistically measurable and reproducible improvement").
   §0.3 states the goal neutrally — *what difference the specification makes*. An aim that presupposes the
   finding contradicts the pre-registration argument the whole reliability section rests on.
2. **"Classical computer-vision detection" for OD/fovea** — the detector is a pre-trained, frozen
   heatmap-regression model, not co-trained with the classifier ([[od-fovea-heatmap-detector-plan]], §0.7).
3. **"Implementation acts and approbation certificates: see appendices"** — *no such documents exist*.
   Appendices are A–F and App D holds only the publication/indexing record. Replaced with an App-D pointer.
4. **The Kazakh clinical set was described as "qualitative validation"** — that examination was never carried
   out (G-3); its real use is training in a data-scarce regime (Exp 7).
5. **Structure-and-length gave no volume at all** — the template requires it. Now carries §0.16's figures.
6. Missing: the ~53,576-image unlabelled pretraining split (SB-2.4 disjointness), the §0.15 "correspondence,
   not funding/commission/mandate" disclaimer, and §0.13's third reliability qualification.
Also: Main results now state the seven hypothesis outcomes with their fences (they previously said only that
each was "evaluated"); novelty gained the cumulative-ablation item, the two non-empirical contributions, and
the SIR-4 lineage on CLAHE; the H-7 margin is given as 0.0041 per §0.8.

**Page figures stated: 265 pp in ALL THREE abstracts** (264 until the 2026-08-14 rebuild; source of record is `council/METADATA.toml`), with 42 tables, 26 figures, 2 diagrams and 107
sources, all excluding appendices. The defense is held in Kazakh, so the Kazakh edition is the defended
volume and every abstract cites *its* extent regardless of the abstract's own language — the English one
included. See [[defense-language-kazakh]] for why §0.16 of the English manuscript still says 238 and must
not be synced to this figure.

⚠ **The 15-page cap (§6.9 of the Statute) is the binding constraint on any edit.** Density differs sharply
by language: EN ≈ 400 words/page, **RU/KZ ≈ 285–290**. The first, fuller revision produced 15/18/17 pages and
had to be cut back twice. Final: **EN 13 pp / RU 15 / KZ 15** at 5110 / 4572 / 4375 words. RU and KZ are **at
the cap** — any future addition there must be paid for by a cut. Enrichment that was dropped for space (kept
in this note so it is not re-attempted blindly): the expanded five-part theoretical significance, the
four-part practical significance with the ingestion protocol and the disowned national projections, and the
"principal finding is consistency" closing paragraph from §7.

## Resync to the four-chapter volume — 2026-08-20

All three abstracts were brought level with the rewritten volume ([[four-chapter-rewrite]]).
Seven classes of desync were closed, at identical positions in EN/RU/KZ:

1. **Volume figures** — 265 pp / 42 tables / 26 figures / 2 diagrams / 107 sources →
   **117 pp / 19 tables / 16 figures / 99 sources**, diagrams dropped (the four structural
   views live in an appendix and the counts exclude appendices). The Kazakh figure still
   governs all three abstracts, per [[defense-language-kazakh]]; registry `council/METADATA.toml`.
2. **Objectives** — six, one per old chapter → **four**, mirroring the introduction.
3. **Main content of the work** — six chapter paragraphs → **four**, titled from
   `outline/TABLE_OF_CONTENTS_{EN,KZ}.md` (RU titles translated to match).
4. **Structure rubric** — six chapters and six appendices (A–F) → four chapters and five
   appendices; EN «A–E», KZ «А, Ә, Б, В, Г», RU unlettered (Russian letters would clash with Ә).
5. **The publication/approbation appendix no longer exists** — both pointers to «Appendix D»
   removed (Practical significance, Approbation); the five works stay listed in Publications.
6. **«No prototype was implemented» is now false** — SB-4.1 was amended in INVARIANTS v7.1.0
   and Chapter 4 describes a **deployed working demonstrator**. Fixed in four places per
   language (novelty 12, main result 9, provision 11, Practical significance), each keeping
   the bound: it establishes realisability and operating behaviour, is evidence for no
   diagnostic claim, and the deployment-oriented parts remain specification.
7. **Governance codes H-1…H-7 removed** (24 per language) — the rewritten volume carries
   **zero** of them (the hypothesis rubric was dissolved as having no corpus precedent), so
   each «(H-5)» pointed at nothing a council reader could find. The outcomes and their
   qualifications stay; only the labels went. **P1/P2 were kept** — the abstract defines
   those itself, so they are not dangling; removing them is available but was not done.

Also KZ only: **«біріктірілген» → «интеграцияланған»** throughout (26 occurrences) — the
translated volume settled on the latter for the integrated arm, and keeps «біріктірілген»
for its other sense, *pooled* (pooled folds).

**The 15-page cap still binds and is still met**: rebuilt EN 13 / RU 15 / KZ 15 pp
(5241 / 4652 / 4427 words) via `build_all.py --only abstract_en abstract_ru abstract_kz`,
run under **system Python 3.13**, not the demo venv. `check_metadata.py` reports nothing new.

⚠ **The same desync is still open in the council reviews**: both official reviewers reports
(six files) and the supervisor review describe a six-chapter volume of 265 pp with 42 tables,
26 figures and 107 sources, and reason chapter by chapter over the old structure — a rewrite,
not a numeric patch. The foreign consultant review is **signed and dispatched**
([[foreign-consultant-dispatch]]) and must not be re-edited.
*(Closed 2026-08-20 — the nine reviewer files were patched, not rewritten; see
[[four-chapter-rewrite]].)*

## Resync to the rebuilt volume — 2026-08-21

Numeric patch only, at the same single line in each language: **117 pp → 118**, **99 sources →
102** (the introduction now cites the candidate's five own publications, and three cards entered
the reference list). Tables 19, figures 16 and the four diagrams are unchanged. The same two
figures were patched in the nine official-reviewer files and in `council/METADATA.toml`.

⚠ **A second, much stricter page cap surfaced with the GD-01 guide** — the annotation filed with
the Office and with the council is capped at **5 pages per language**, against the 15 of §6.9 that
these abstracts were written to. Ours are EN 13 / RU 15 / KZ 15 and do not meet it. Whether the two
caps govern the same document is unresolved — see [[annotation-page-cap-conflict]] before editing
these files for length again.

## Currency pass — 2026-08-23 (after the v7.2.1 rebuild)

Checked against `council/METADATA.toml`, `outline/TABLE_OF_CONTENTS_{EN,KZ}.md` and the
council structure spec. **Current and needing nothing**: the volume figures (113 pp / 19 tables /
16 figures / 102 sources, Kazakh edition, per [[defense-language-kazakh]]), the topic on all three
languages, the programme code 8D06102, the four chapter titles, the five appendices with the Kazakh
letters А, Ә, Б, В, Г, the five publications, and the built `.docx`/`.pdf` in
`defense/docs/abstracts/` (rebuilt with the volume in v7.2.1). `check_metadata.py` clean.

**Two things had fallen behind and were fixed:**

1. **The Scopus percentile was missing.** `council/en/11-abstract-annotation/structure.md` asks for
   quartile *and* percentile; the abstracts gave «Q3» alone, although the percentile was researched
   and written into the registry (`percentile = "42"`, CiteScore 2025 = 2,5, Computer Science
   Applications #590/1022) and into the nine official-reviewer files. Added in both places per
   language — the Publications summary line and entry 1 of the works list — in the reviewer files'
   own wording, incl. the Kazakh house form «42-перцентиль», «… санатында».
2. **The Kazakh register repair of v7.2.1 never reached `abstract_kz.md`.** That pass covered the
   35 translation sources only; the abstract still carried **13 mid-sentence «, сондықтан»** in
   4 431 words — the volume's whole ceiling (12) in a text a sixth its length — and **zero**
   sentence-initial connectives, i.e. every causal join was the English «…, so …» comma. Ten were
   moved to the causal suffix (-дықтан/-діктен/-тықтан), three became new sentences opening on
   Сондықтан / Демек / Осылайша. `conformance.kazakh_register()` now passes all three checks on the
   abstract (0 calques, 0 mid-sentence, top connective 33 %).
   ⚠ The gate runs over the volume, **not** over `thesis/output/` — the council documents are outside
   its scope, so a volume-wide register or notation repair has to be applied to them by hand.

Rebuilt via [[council-docs-skill]] (`build_all.py --only abstract_en abstract_ru abstract_kz`,
system Python 3.13). **Page counts did not move: EN 13 / RU 15 / KZ 15** — the additions fit inside
the existing pages, so the 15-page cap did not have to be paid for by a cut. The 5-vs-15-page
conflict of [[annotation-page-cap-conflict]] remains open and untouched.


## Rewritten to the corpus genre — 2026-08-23

`D:/phd/council/temp/АНАЛИЗ_АННОТАЦИЙ.md` measured all seventeen candidates'
abstracts on three languages (we are **A17**). It settles what the genre is, and we were
outside it on two axes at once.

**The genre.** An abstract in this council is not a one-page summary but a **shortened
introduction**: the same rubrics with **bold run-in lead-ins**, in flowing prose. Nobody has
standalone subheadings, numbered rubrics, tables or figures — enumerations run **inline**
inside the paragraph («Задачи исследования: 1. … 2. …»), publication lists included.
Median 18,315 characters, 16 rubrics, **6–8 pages**; Times New Roman 14 pt, single spacing,
justified, first-line indent 10–12.5 mm, bold 2.2–10.2 % of characters.

**Where we stood.** Ours was **39,269 chars / 15 pages** — the largest of the seventeen by
35 % over the next (A11, 29,032) and more than double the median — and built from `##`
headings plus real numbered lists, so it printed subheadings on their own lines and measured
a 7.0 mm indent (the hanging indent of list items, not the body indent). The rubric **set**
was never the problem: we are the only candidate with all fourteen mandatory rubrics present
and our order already mirrors A15. §8 of the analysis put the divergence in two rubrics —
**положения 10.1× the corpus median, новизна 7.6×** — written as long qualified formulations
where the corpus writes a terse list.

**What was done.** All three languages rewritten as run-in rubrics in flowing prose, keeping
the 20-rubric set and order, enumerations inline, no `---` rule. Result: **EN 22.6k / RU 22.2k
/ KZ 22.1k chars, EN 7 / RU 8 / KZ 8 pages** — inside the corpus band (A13 is 22,663 / 8 pp)
and at its modal page count, with the three versions within 3 % of each other (corpus norm
±10 %). Built docx measure bold 3.8–3.9 %, indent 1.25 cm, and **no all-bold own-line
paragraph except the title block** — which is exactly the corpus form.

**How the qualifications survived the cut.** The bounds attached to each provision are binding
(INVARIANTS CFC-2.8, SB-4.x, DGL-4) and could not simply be deleted to reach corpus length.
They did not need to be: **the introduction had already solved this** on 2026-08-22 — the
corpus hedges a provision in 1 of 16, so the volume's provisions became assertions carrying
their effect sizes and the bounds moved to the reliability rubric ([[peer-intro-norms]]). The
abstract now mirrors that: provisions state the numbers (6.54/6.55 pp wF1, 0.032/0.036 AUC,
0.11 κ, ablation 0.7538→0.8193, distance 0.070–0.093, G 0.898 vs 0.858, +0.069/+0.054 vs
MCID 0.050, ALO 0.099–0.129 at p ≤ 0.0148), and **Достоверность carries three general and
four provision-specific qualifications plus the «не выносятся на защиту» list**. Nothing was
dropped; CFC-2.8's "the configuration as a whole, not preprocessing alone" is verbatim in all
three languages.

⚠ Two things to know before touching these again. The abstract is **not** in
`conformance.py`'s scope — the gate reads the volume only — so the Kazakh register checks and
anything else volume-wide has to be run against `thesis/output/` by hand; they pass here
(0 calques, 0 mid-sentence «сондықтан», top connective 33 %). And the GD-01 five-page cap of
[[annotation-page-cap-conflict]] is now **much closer but still not met** — 7/8/8 against 5;
the corpus itself does not meet it either (only A01, A12 and A16 are at 4 pages), which is
evidence that the 15-page reading of §6.9 is the operative one.

### Вёрстка титульного блока и списка публикаций — 2026-08-23

Две вещи, которые разбор по рубрикам показать не мог (`Аннотация_по_рубрикам.txt` склеивает
абзацы — по нему список публикаций выглядит идущим внутри абзаца). Сняты с самих PDF образцов
через `pymupdf`, по x-координатам строк:

1. **Титульный блок центрируется целиком.** У Бакировой, Дауренбаевой, Мырзакерімовой каждая
   строка блока — «АННОТАЦИЯ», ФИО, тема в кавычках, формула степени, шифр ОП — центрирована
   и полужирная, без абзацного отступа; Word переносит блок сам. У нас дескриптор шёл обычным
   абзацем по ширине с отступом 1,25 см.
2. **Каждая публикация — отдельный абзац с номером.** У Әйтім рубрика «Публикации.» — проза,
   затем отдельный абзац «Результаты… представлены в следующих публикациях:», затем по абзацу
   на работу: первая строка с обычным абзацным отступом (100,4 pt при поле 72), продолжение
   вровень с полем, по ширине. **Это не список с висячим отступом**, который даёт
   `md2gost._list_item` (−7 мм).

`md2gost.py` получил под это два расширения (обе копии, `.claude/` и `.agents/`):
`_body(..., center=True)` и директива **`<!-- runlist -->`**, после которой нумерованный блок
печатается обычными абзацами с номером внутри текста. Директива `<!-- center -->` теперь
действует и на обычный абзац, а не только на блок с жёсткими переносами (её прежнее
применение — шапка списка научных трудов — идёт через `_line_block` и не затронуто, проверено
пересборкой). Объём не сдвинулся: **EN 7 / RU 8 / KZ 8**.

### Титульный блок переносится вручную, а не Word'ом — 2026-08-24

Уточнение к пункту 1 выше: «Word переносит блок сам» верно только для кириллицы. Замеры
шестнадцати английских аннотаций архива (`Образцы документов/авторы/*/Abstract*eng*.pdf`,
x-координаты строк через `pymupdf`) показывают ширины строк шапки 281–466 pt при полосе
471–485 pt, с разбросом внутри блока до 170 pt (Бакирова: 301/290/403/459). Такой рваный край
автоматическим переносом не получается — образцы **набирают шапку жёсткими переносами** по
смыслу: ФИО / часть темы / часть темы + «submitted» / формула степени / шифр ОП.

У нас RU и KZ выглядели правильно случайно: длинные кириллические слова сами оставляли рваный
край. **EN давал 473.8 / 470.5 / 470.7 / 472.6 pt при полосе 485** — все строки в пределах 15 pt
от полей, и блок читался как обычный абзац по ширине, а не как заголовок. Исправлено 2026-08-24:
`abstract_en.md` набран пятью строками с жёсткими переносами (две концевых пробела), каждая в
своём `**…**`, под той же директивой `<!-- center -->` — она уводит блок в
`md2gost._line_block(center=True)`. Ширины стали 402/428/439/381/372 pt. Объём не сдвинулся
(7 страниц), текст, кроме мест переноса, не менялся. RU/KZ не трогали.

Тем же замером снят второй параметр шапки: **от последней её строки до первой строки текста
у образцов ровно два интерлиньяжа** — 31.8–32.4 pt при TNR 14 pt и одинарном интервале, то есть
одна пустая строка, у семи из восьми англоязычных образцов с текстовым слоем (у Дауренбаевой две).
У нас было 16.1 pt, то есть без отбивки. `md2gost` теперь закрывает центрированную шапку пустым
абзацем (`_blank_line`) на обоих путях — и `_line_block(center=True)`, и `_body(center=True)`, —
так что отбивка одинакова на всех трёх языках; замер после пересборки 32.2–32.3 pt. Объём не
сдвинулся (EN 7 / RU 8 / KZ 8), в RU и KZ одна строка переехала через границу страницы, текст
не менялся. Та же директива стоит в `publications_list_ru.md`, поэтому шапка списка научных
трудов тоже получила отбивку (16.6 → 32.8 pt, по-прежнему 3 страницы) — у единственного образца
списка с текстовым слоем (Тохтахунов) там тоже разрыв.

⚠ Побочное: разбиение темы жёстким переносом рвёт её на два `**…**`-спана, и
`check_metadata.normalise()` переставал находить `dissertation.title_en` в исходнике. Функция
теперь снимает `**` перед сравнением (обе копии скилла) — разметка не должна прятать значение
реестра; заодно перестаёт прятаться и запрещённая форма, разорванная жирным.

⚠ **`docx2pdf` конвертирует папку целиком.** Пересборка одного отзыва перештамповала все PDF в
`defense/docs/reviews/`, включая подписанный и отправленный отзыв зарубежного консультанта;
восстановлено через `git checkout`. Собирая один документ, проверяй `git status` после.

## Пятистраничная редакция — 2026-08-25

Аннотации сокращены до **потолка GD-01 в 5 страниц** и заменены на месте: 22,4/22,2/22,8 тыс.
знаков → **RU 14 269 / KZ 14 602 / EN 15 176**, по 5 страниц каждая, 21 абзац в каждой (паритет
абзац к абзацу — самая дешёвая проверка того, что три версии режутся по одному месту).
Все 14 рубрик сохранены в каноническом порядке; жанр (полужирные лид-ины в сплошной прозе, без
подзаголовков, без таблиц) не менялся.

Что уцелело намеренно: все семь положений с их величинами эффектов; оговорка при положении 2
(ветви различаются и инициализацией); в «Достоверности» — предрегистрация критериев, три общих
и четыре частных оговорки и фраза «Не выносятся на защиту…»; «врач в контуре», статус
демонстратора и «соответствие по замыслу, а не сертифицированное»; формулировка про
соответствие приоритетам, а не финансирование; объёмы и тема по `council/METADATA.toml`.

Что снято: **полный список публикаций** (1 684 знака — в бюджет 5 страниц не входил; сводная
рубрика с индексацией осталась и отсылает к `publications_list_ru.md`), сквозные дубли между
«Основными результатами» и «Положениями», пересказ актуальности в «Общей характеристике» и
детализация в пересказе глав. `check_metadata.py` больше не требует `pub:1…5` от аннотаций —
эти DOI сверяются в списке научных трудов.

Итог замера: 0 расхождений с реестром, обе KZ-проверки регистра чистые. См.
[[annotation-page-cap-conflict]] (потолок и плотность знаков на страницу) и
[[peer-annotation-norms]] (где это ставит нас в корпусе).
