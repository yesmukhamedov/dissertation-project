# Ethics committee conclusion — layout of IITU's own blank

> **Parsed 2026-09-19** from the two blank forms IITU issues to doctoral candidates
> (`Заключение_Этической_комиссии_бланк_{рус,каз}.docx`, kept in `D:\personal\phd\council\`,
> outside the repository). The blanks were **only read**, never edited. What defines the look —
> page, fonts, spacing, column widths, row wording, signatories — is stored in
> `defense/docs/ethics/form_layout.json`, so this file and the generator work without the blanks.
> Content of the rows: [[structure]]. Peer samples (filled conclusions of 16 candidates) are a
> different archive and were not used for the layout.

## Page and type

| | |
|---|---|
| Paper | A4, portrait, one page |
| Margins | top 20 mm · bottom 20 mm · **left 30 mm · right 15 mm** (850 twips; the GOST volume uses 10 mm) |
| Font | Times New Roman throughout; language `ru-RU` / `kk-KZ` on the runs |
| Headline | 12 pt **bold**, centred |
| Table text | **11 pt**, left-aligned, vertically centred |
| Closing paragraph, signatures, date | 12 pt; closing paragraph justified with a ~6 mm first-line indent |
| Page number, header, footer | none |

## Header

| RU | KZ |
|---|---|
| `ЗАКЛЮЧЕНИЕ` / *(empty line)* / `Этической комиссии` / `АО «Международный университет информационных технологий»` (15 pt after) | `Халықаралық ақпараттық технологиялар университетінің` / `Әдеп комиссиясының` / *(empty line)* / `ҚОРЫТЫНДЫСЫ` |

The Kazakh committee is called **Әдеп комиссиясы** here — not «Зерттеулерді этикалық бағалау жөніндегі
комиссия», as in the Ибраева sample. The blank is the newer and the authoritative wording.

## Table

Single 0.5 pt black borders, 9 rows, no header row. Cell padding 5 pt top and bottom, 7.5 pt left and right.

| | RU | KZ |
|---|---|---|
| Columns (twips) | 2: **4390 / 4970** = 9360 | 3: **704 / 4111 / 4536** = 9351 |
| Row numbers | none | printed in column 1, centred, top-aligned |

Row wording is in `form_layout.json` (verbatim). It differs from the wording in [[structure]], which was
taken from the peer samples: e.g. row 2 is «Специальность (образовательная программа) докторантуры»,
row 3 in Kazakh «Докторантурада оқу **кезеңі**» (samples: *мерзімі*).

## Below the table

1. Closing paragraph — «Научные исследования докторанта **⟨Ф.И.О.⟩** на тему «⟨тема⟩» полностью
   соответствует этическим нормам и может быть реализовано в нынешнем виде.» Kazakh: «Докторанттың
   ⟨…⟩ «⟨…⟩» тақырыбындағы ғылыми зерттеулері әдеп нормаларына толық сәйкес келеді және қазіргі
   нұсқасында жүзеге асырылуы мүмкін.»
2. Two signature lines, chairman then secretary, then the date line.

| | RU | KZ |
|---|---|---|
| Chairman | `Председатель Этической комиссии` / `по оценке научных исследований АО «МУИТ»` `_____ Дузбаев Н.Т.` | `Әдеп комиссиясының төрағасы` `_____ Дузбаев Н.Т.` |
| Secretary | `Секретарь` `_____ Есмурзаева А.Б.` | `Әдеп комиссиясының хатшысы` `_____ Есмурзаева А.Б.` |
| Date | `Дата выдачи: ______ 2026 года` | `Берілген күні: ______ 2026 жыл` |

**The 2026 blank prints Дузбаев Н.Т. as chairman.** [[structure]] says Найзабаева Л.К. — that is what
the older peer samples show; the blank is newer.

## Differences between the blank and the form

- **9 rows, no AI rows.** [[structure]] recommends the 12-row form (Базарбеков). IITU's blank does not
  have rows 10–12; the generator follows the blank. How the AI statement is recorded is an open question
  — [[../00-regulatory-framework/ai-usage]].
- **Rows 7–9 come pre-filled in the RU blank** («Нарушения не выявлены» ×2; «В работе объекты живой
  природы и среды обитания не исследовались»). In the KZ blank row 8 is left empty and row 9 carries
  «Бұзушылықтар анықталмады» — a copy error: it answers a different question.

## What the generator does differently

`defense/docs/ethics/build_ethics_conclusion.py` rebuilds the document from `form_layout.json`. With
`--blank` it reproduces the blank verbatim; rendered by Word, every table rule and word sits at the same
coordinates as in the original (checked to 0.1 pt; 33 RU / 303 KZ of 967 590 pixels at 100 dpi still differ,
cause not investigated).
The filled document departs from the blank in five places, all to keep it on **one page**:

1. the empty spacer paragraph between the closing paragraph and the signatures is dropped;
2. two empty lines before the date become one;
3. the KZ blank's stray five-space paragraph before the closing paragraph is dropped;
4. signature lines are aligned by a tab stop instead of runs of spaces (in the blank the underscores of
   the two signatories do not line up);
5. row 6 is kept to 2–3 lines — the dataset list lives in the volume.

## Filling rules

| Row | Source |
|---|---|
| 1, 2 | `candidate.name_*`, `programme.code` + `programme.name_*` |
| 3 | `candidate.study_period` — **empty in the registry → `<…>`** |
| 4 | `dissertation.title_*` + order `№ 7-D`, 27.08.2022 (`topic_approval_*`) |
| 5 | `supervisor.*`, `foreign_consultant.*`; place = the organisation's, not citizenship — as in the samples |
| 6 | `defense/docs/ethics/conclusion.toml` |
| 7, 8 | printed by the blank itself (the commission's finding) |
| 9 | `conclusion.toml` — **left empty on purpose → `<…>`** |
| Signatories | the blank (`Дузбаев Н.Т.`, `Есмурзаева А.Б.`); override in `[signatories]` |
| Date | `ethics.conclusion_date`; empty → `______ 2026` |

Row 9 is not defaulted because the printed answer («living organisms not studied») may not hold for a
work that uses a clinical set; see [[structure]] for the Базарбеков pattern.

## Regenerate

```powershell
python defense/docs/ethics/parse_form.py                      # only if IITU changes the blank
python defense/docs/ethics/build_ethics_conclusion.py         # → ETHICS_CONCLUSION_{RU,KZ}.docx/.pdf
python defense/docs/ethics/build_ethics_conclusion.py --blank --out <dir>   # fidelity check
```

The build exits non-zero if a document is not exactly one page.
