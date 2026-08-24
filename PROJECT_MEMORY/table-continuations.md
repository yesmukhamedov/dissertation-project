---
name: table-continuations
description: How the GOST "Continuation of table N" lines are placed in the exported volume — the hard page break that pins them, the head row duplicated inside the table, front-to-back order, the three defects the 2026-08-23 build shipped, and what the council's own sixteen dissertations do (11 of 16 carry the line; the Kazakh form is hyphenated)
metadata:
  type: project
---

`.claude/skills/council-docs/scripts/table_continuations.py` is a Word-COM
post-pass over the saved `.docx`: it finds the first row of every table that
starts on a later page than the table does, duplicates the head row there,
splits the table, and writes the GOST line ("Continuation of table 3.15" /
"3.15 кестенің жалғасы") into the paragraph the split leaves behind. GOST 7.32
requires the line, ten of the council's sixteen published samples carry it, and
the volume had 42 tables and zero continuations before the pass existed
([[gost-export-toolchain]]).

**The 2026-08-23 build shipped it broken** — the candidate found it in
`FULL_DISSERTATION_KZ` p. 86–87 (Кесте 3.14) and in EN tables 3.5, 3.15, А.1,
Б.1, 2.3. Three separate defects, all fixed on 2026-08-24:

1. **Labels drifted off the page head, and doubled.** A split is committed to the
   layout the moment it is made, on the page numbers Word reported *then*; the
   header row it inserts moves every break after it, so a later table's split
   pulled the break out from under a label already placed. Fix: the continuation
   paragraph carries `PageBreakBefore = True`, which pins it, and tables are
   walked **front to back** so a split is fixed before anything ahead of it
   moves. An earlier attempt to measure-then-undo a bad split instead left
   rejoined-but-not-merged tables with a blank leading row and no label at all
   (KZ 2.3, 3.1, 3.14, А.1, Б.1 in that build) — do not revive it.
2. **The repeated head row arrived on the wrong column grid.** Pasting row 1
   across from the other half of the split (`Row.Range.FormattedText`) carries
   the source column widths with it: the continued part of EN table 1.1 came out
   with an 11-column grid under a 6-column head, cells offset by one. Fix: the
   head row is duplicated **inside** the table, above the cut row, before the
   split — Word then builds it on the table's own grid.
3. **A caption plus a bare ribbon of column heads at the foot of a page.** When
   the first part would be nothing but the head row, the table is not split at
   all: a page break goes before its **caption** and the whole table moves to the
   next page. That is what KZ 3.14 (p. 86) and EN 3.5 needed; EN 3.5 now fits on
   one page and has no continuation line.

**What the peer corpus actually does** (checked 2026-08-24 against the full texts
in `D:\dissertation_council`, not against a summary): **11 of the 16 carry the
line** — `Продолжение таблицы N` in Бакирова (12×), Момынқулов (10×), Олжаев,
Базарбеков, Науменко, Муханов; `Continuation of table N` in Нәлгожина, Әйтім,
Мырзакерімова, Тохтахунов; `N-кестенің жалғасы` in Тоқтарова. The five without
it have no table broken across a page. The council's formatting instruction
(`_raw/norm_instrukciya_oformlenie.txt`, ll. 245–249) requires it and puts the
*title* over the first part only, which is what the pass does. In every sample
PDF the line is the **first line of the page, ranged left**. None of them repeats
the head row — Тоқтарова repeats only the column numbers (`1 2 3 4 5`), the rest
go straight into data. Repeating the whole head, as this export does, is the
stricter of the two forms the norm allows.

**The Kazakh label is hyphenated: `{num}-кестенің жалғасы`.** Тоқтарова writes
`1.1-кестенің жалғасы` (pp. 16/35/43/108) and this manuscript's own prose already
hyphenates — 59 references of the form `Б.1-кесте`, `2.3-кестеде` against one
spaced. The pass shipped the spaced form on the first fix and it was corrected
the same day. The *caption* keeps the word first (`Кесте 3.14 – Атауы`), exactly
as Тоқтарова heads hers; only the continuation label takes the number first.

A Paragraph taken from a temporary Range dies with that Range — caching the
caption paragraph and setting a format on it a few statements later raises
`E_OUTOFMEMORY`. Paragraphs are re-resolved by index against a Range the caller
holds open. Table objects, unlike Paragraphs, stay valid and auto-shift as the
document is edited, so the pass captures them all up front.

Counts after the fix: **EN 9 continuation lines, KZ 16**, all at the head of
their page in the rendered PDF, head rows matching their first part cell for
cell, CONTENTS page numbers 43/43 correct in both volumes. `build_full_dissertation.py`
runs the pass twice — on the body-only `.docx` **before** `dump_pages` reads the
CONTENTS page numbers, and again on the merged volume — and the two must report
the same count, or the CONTENTS is measuring a document that does not exist.

Not covered: the intermediate `defense/docs/DISSERTATION_{EN,KZ}_GOST_<date>.docx`
(manuscript body without front matter) never runs the pass and carries no
continuation lines. It feeds `build_toc.py`'s standalone CONTENTS deliverable,
whose page numbers therefore sit a few pages below the assembled volume's.
