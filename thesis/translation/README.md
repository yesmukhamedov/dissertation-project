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
