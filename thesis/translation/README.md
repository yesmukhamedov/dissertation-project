# translation/ — EN ↔ RU ↔ KZ translation kit for the local Qwen

Built 2026-09-27. Lets the local Qwen3.8-27B (`C:\AI`, llama.cpp) translate the dissertation between
English, Russian and Kazakh at the standard of the approved volume. The model is not fine-tuned
(a 27B model cannot be trained on a 12 GB GPU); it is taught through context, and every chunk it
produces is checked mechanically.

| File | Role |
|---|---|
| `rules/common.md` | what every translation must do (content fidelity, what stays unchanged, output form) |
| `rules/{en,ru,kz}.md` | target-language conventions: separators, citations, dash, references, register |
| `termbase.tsv` | trilingual terms `en ru kz rule note`; KZ forms taken from the approved translations, not the stale glossary |
| `tm/tm.jsonl` | translation memory: paragraph-aligned EN–KZ pairs of 31 sections + the EN–RU–KZ abstract |
| `translate.py` | the translator (chunking, prompt assembly, check + one retry, cache, report) |
| `check.py` | mechanical acceptance: numbers, names/codes, [n] citations, headings, tables, leftover source language, forbidden forms, length, terms |
| `eval.py` | quality measurement against held-out approved translations (chrF++, check pass rate) |
| `build_tm.py`, `build_termbase.py`, `termbase_fill.py` | rebuild the TM and the termbase from the sources |
| `rules/genre-council.md` | official documents of the dissertation council (role, official-administrative formulas, lists, legal references, decimal comma in KZ) |
| `extract_body.py` | body text only (no title blocks, headings, running heads, tables/forms, signatures) of council .docx / pdftotext .txt → `corpus/` or `<doc>.body.md` |
| `corpus/` | extracted council texts: 16 trilingual abstracts (`abstracts/<slug>.{ru,kz,en}.md`) + GD_01 guide RU/KZ |
| `work/gold/` | Opus's reference translations of the 8 frozen council test items (`_draft/` = frozen source + human text) |
| `work/` | intermediate files, eval runs (`work/eval/results.tsv`) |

## How a chunk is translated
1. The section's PART 1 text is split into chunks of ≤ 450 words; tables and code are never split,
   code/markers/rules are copied verbatim, PART 2/3 checklists and translator notes are dropped.
2. Prompt = rules (fixed prefix, cached by llama.cpp) + the termbase rows found in the chunk + the two
   most similar approved example pairs from the TM + (RU↔KZ) the aligned English original as pivot +
   the tail of the previous translated chunk + the chunk.
3. `check.py` runs on the output. Any error → one retry with the error list in the prompt; the better
   attempt is kept; chunks still failing are reported as `NEEDS_REVIEW`.

## Sources of truth
Terminology and style follow the approved Kazakh edition (`chapters/*/translations/`) and the approved
Russian abstract (`output/abstract_ru.md`), and the volume gate `scripts/conformance.py` (short dash,
«т.б.», «сондықтан», sentence length). `glossary/GLOSSARY_KZ.md` is partly stale (e.g. it keeps
"pipeline" in Latin, the volume says «алдын ала өңдеу конвейері»), so it was used only as a candidate list.

## Results (2026-09-27, iteration 1)
chrF++ against approved human text the model never saw as an example. Scale: an unrelated Kazakh
section scores 30, the first half of the reference alone scores 55.

| Direction | Test | chrF++ | Chunks clean first try |
|---|---|---|---|
| EN→KZ | held-out 3.4, 4.2, 1.3 vs `translations/` | 70.2 | 7/8 (the 8th: a long dash copied from a figure caption — now normalised) |
| EN→RU | 4 abstract paragraphs vs `abstract_ru.md`, no RU examples | 66.4 | 1/1 |
| KZ→EN | 4.2 vs the English draft | 70.4 | 2/2 |
| RU→KZ | 4.2 (Qwen's own RU) vs `translations/` | 66.2 | 2/2 |
| RU→EN | 4.2 (Qwen's own RU) vs the English draft | 74.3 | 2/2 |

Speed: ~2–4 min per chunk (≈ 450 EN words), prompt ~220 tok/s, generation ~6–7 tok/s.

Errors found and fed back into the kit in iteration 1: DR → ДР in Russian; "performance" is «качество»,
not «производительность»; grading → «градация»; parameter sweep / re-implementation calques; long dash
from captions; short abbreviations (CAM, DR) matching inside other words.

Full EN→RU run of the volume (2026-09-27 03:11–06:58, 3 h 48 min): 36 files, 121 chunks, 115 clean on
the first try; the 4 flagged chunks were false alarms (translated institution names and table-row names;
the checker now warns on Title-Case hyphenated compounds instead of failing). 43,581 EN words →
38,837 RU words. A manual read of sample paragraphs found about one stylistic slip per paragraph and an
occasional weakened/shifted phrase — the Russian text is a strong draft that still needs a human read
before it is submitted anywhere.

Defects found in the approved Kazakh text by `check.py` (not fixed here): `et al` left in 1.1; decimal
commas `0,951` / `0,853` in 1.2; a long dash in appendix C; "Intersection-over-Union" dropped in D.

## Genre 2: dissertation-council documents (iteration 2, 2026-09-27)
Paths moved to `C:\VirtualD` (the D: drive is retired). Two genres now: `thesis` (chapter files) and `council`
(any other file: regulations, guides, abstracts, reviews). A genre selects its rules file (its first paragraph
replaces the dissertation role of `common.md`, the rest overrides earlier rules), the termbase rows of its
domain (6th column: empty = all, `thesis`, `council`) and prefers TM examples of its domain.
TM: + ~500 aligned council rows (13 abstracts × RU–KZ/EN–RU/EN–KZ, second half of GD_01); held out:
bakirova, bazarbekov, toktarova and the first half of GD_01 (`build_tm.COUNCIL_HOLDOUT`; frozen eval texts are
also filtered out of the TM by content).
Eval: `python eval.py --set council --tag cN` — 8 items (~700 source words each), 6 directions. chrF++ against the
human text, and chrF_gold against Opus's corrected reference in `work/gold/` (the human council translations
contain omissions, typos, Russian words and misalignments, so chrF_gold is the main number).
Checks added for this genre: definition formula «(далее – X)» ↔ «(бұдан әрі – X)» ↔ "(hereinafter – X)",
list markers, spaced dash inside Kazakh compounds (сондай – ақ), Latin ə in Kazakh, lowercase paragraph starts,
numeric dates (25.05.2026 may be written out), English copied from a non-English source is not a leftover.

### Results, council genre (2026-09-27)
chrF_gold = chrF++ against Opus's corrected reference (`work/gold/`); probes = the 28 concrete errors Opus found
reading c0 (`work/probes.py`); `work/rescore.py <tags>` recomputes the table.

| Direction | c0 (kit as-is) | c1 | c2 | c3 |
|---|---|---|---|---|
| RU→KZ | 79.2 | 82.1 | 82.3 | 83.6 |
| KZ→RU | 84.7 | 87.3 | 86.4 | 87.2 |
| EN→RU | 87.6 | 88.6 | 87.8 | 86.3 |
| RU→EN | 86.4 | 85.6 | 86.3 | 86.0 |
| EN→KZ | 77.0 | 81.9 | 80.9 | 81.4 |
| KZ→EN | 77.9 | 78.3 | 79.3 | 78.9 |
| mean | 82.1 | 84.0 | 83.8 | 83.9 |
| probes firing | 28/28 | 2/28 | 0/28 | 1/28 |

Run-to-run noise (temperature 0.3) is about ±1 chrF per direction, so c1–c3 are a plateau; the gain is in the
errors removed (13 meaning, 14 term, 1 format in c0), not in the chrF decimals.
Thesis regression (reg2, same rules): EN→KZ 69.3 (it1 70.2, −0.9, within noise), EN→RU 67.7 (it1 66.4).

Validation on texts never read while tuning (v3: olzhayev RU→KZ, KZ→EN; mukhanov EN→RU, KZ→RU; ~2 150 words;
chrF vs human 72.7 / 71.2 / 85.9 / 72.0): Opus's full read found 1 meaning error repeated 5× («қазақ таңба
әліпбиі» → «казахский тюркский алфавит», a missing term), term slips (supervised learning → «супервизорное»,
representative → «өкілдік», видео-/бейне- mixed), one spelled-out number, one typo. All were turned into termbase
rows / rules afterwards, so v3 can no longer serve as an unbiased check; a fresh validation needs new texts.

What the model still does: occasional word-order/participle heaviness in Kazakh, Russian passive-with-agent into
Kazakh (rule added late), unknown domain terms → it guesses. Human reading of every official document remains
necessary; the checks catch form, numbers, names, lists, calques and Kazakh letters, not meaning.
Known input issue: pdftotext breaks two-column bullet lists (olzhayev RU) - Qwen reassembles them, but the
list-marker check then fires.

## Full EN→KZ run (2026-09-27 20:51 – 09-28 03:27, 6 h 36 min)
Output kept apart from the approved edition: `chapters/<ch>/translated-kk-qwen/<id>-kz.md` (`--out`).
36 files, 121 chunks, 114 clean on the first try, 1 NEEDS_REVIEW (B chunk 4: `1,000` / `35,126` with
thousands commas).
Error fed back: appendix letters. Qwen ignored the rule in `rules/kz.md` and mixed Latin (C.1), wrong Kazakh
(Б for B) and lookalikes (С, Д, Е); `check.py` now fails an EN→KZ chunk whose appendix letters are not the mapped
source letters (A→А, B→Ә, C→Б, D→В, E→Г, F→Ғ).
Still open: «, сондықтан» 72 times (conformance allows ≤ 12 per volume); term warnings (mainly
«нөлді қамтымайтын аралық», «өлшем»); a spot-read of the conclusion found two garbled phrases (a suspected dropped clause was
my misreading) — the text is a draft that needs a full human read.
Corrections are made only by Qwen: `fix.py` (reviewer's task -> Qwen rewrites the chunk -> check.py -> cache);
Opus reviews and writes the tasks, never edits the outputs.
