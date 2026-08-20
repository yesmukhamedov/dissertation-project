---
name: citation-style-convention
description: Drafts use author-year; the GOST [N] pass was run on the four-chapter volume 2026-08-20 — 99 sources, list described per GOST 7.1-2003
metadata:
  type: project
---

## Состояние: пройдено 2026-08-20 на четырёхглавном томе

`python thesis/assembly/_finalize_citations.py` (после `_assemble_en.py`) → **99 источников**,
`[N]` по первому упоминанию, 133 скобки, 0 blocking / 0 unknown. Отчёт —
`_citation_resolution_final_2026-08-20.md`, рукопись — `DISSERTATION_EN_GOST_2026-08-20.md`.
Список литературы стоит **между заключением и приложениями** и нумеруется **без точки** («1 Kusuhara
S. …») — этого требует ГОСТ 7.32-2001 п. 6.11 и так во всех 16 образцах; прежние сборки печатали
«1.». Само описание — по **ГОСТ 7.1-2003**, а не APA: `_gost_bib.py` конвертирует поле APA-7
карточек в `_card_gost.tsv`, строки с `#pinned` правлены руками и при перегенерации не затираются.

Что стоит знать при повторном прогоне:

- **KZ не конвертируется**, пока нет `DISSERTATION_KZ_partial_<та же дата>.md`. Скрипт раньше брал
  «самый свежий» KZ и молча сконвертировал бы шестиглавный том под нумерацию четырёхглавного.
- **Самоцитаты нумеруются как все** (ГОСТ), рамка SIR-4 живёт в прозе и сохраняется. В переписывании
  статья EEJET названа двумя разными наборами авторов — `Sapakova et al., 2025` и
  `Yesmukhamedov and Sapakov, 2025`; по одной фамилии вторая форма разрешалась в статью НАН РК, где
  Сапакова-соавтора Sapakov нет вовсе. Ключ `yesmukhamedov-sapakov|2025` в `K2C` это чинит, а
  дедупликация внутри скобки схлопывает пару в одну `[16]` (этого же требует SIR-5).
- **Четыре записи достроены по опубликованной версии**, а не по карточке (в карточке нет издания):
  `zhou-2022`, `wang-2018`, `cheplygina-2018`, `sanchez-gutierrez-2022`. Перечислены в отчёте.
- Цитируется 99 карточек из 121; 22 некитируемые перечислены в отчёте — это норма после сжатия.

Ниже — исходное решение, которое этот прогон исполняет.

---

In-text citations in `thesis/chapters/**/drafts/` intentionally use **author-year**
(e.g. "Voets et al. (2019)", "In Sapakova, Yesmukhamedov and Sapakov (2025)"). This is a
**working/intermediate** style, NOT the final form — it is deliberately tied to literature
cards so reviewers can trace each claim to its source (writing-prompt: "cite by Literature
Card filename"). The draft header lists the card↔name mapping (e.g. #17 = voets-2019.md).

The **final dissertation** must cite by **numbered square brackets `[11]`** in order of first
appearance, with the reference list numbered in order of appearance, per GOST 7.32-2001 §6.9/§6.11
and GOST 7.1-2003 (binding RK rule, see `council/en/02-formatting/gost-formatting.md`). Page on
repeat: `[11, с. 88]`.

**Decision (2026-06-16):** leave author-year in drafts; do NOT convert per-file. Convert to
`[N]` in a single **citation-assembly pass at final assembly**, because:
- `[N]` ≠ literature-card ID (#17). It is the source's position by first appearance across the
  whole assembled document, so it cannot be computed per-section while chapters are still in flux.
- Self-citations use the same numbered `[N]` form; SIR-4 transparency is carried by the
  surrounding prose ("the candidate's own prior work … previously published results"), not by the
  citation format.

No chapter currently uses `[N]` form (verified: no `[\d+]` matches in `chapters/`). See
[[thesis-writing-status]], [[literature-corpus-120]].

The citation-assembly pass is specified in `thesis/prompts/citation-assembly.md` (Stage G,
written 2026-06-16): consumes the assembled PART 1 bodies in TOC order + the draft Sources-header
card↔name mappings + the cards' bibliographic fields; assigns `[N]` by first appearance, builds the
GOST 7.1-2003 "List of references used," emits a QA resolution report. KZ translation reuses the
same numbers/list.
