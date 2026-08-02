# `results/` — portable knowledge base for the dissertation experiments

> ▶ **Updated for the 2026-08-02 run.** All values and verdicts in this folder have been replaced
> with the results of the latest run (`VALUES.md`). **The bottom line has flipped relative to the
> previous revision: 6 of 7 hypotheses are fully confirmed** (H-1, H-2, H-3, H-4, H-5, H-6), H-7 is
> partial (1 of 2 sets), and none are refuted. In addition: exp7 (small data) — significant positive,
> the SSL gate passed with both backbones, and a new **H-3** block appeared (domain distance, MMD/KL).
> The key methodological change: **confound CFC-2.8 has been decomposed** — the cumulative exp2
> ablation on full EyePACS under a single initialization reproduces the entire exp1 gain (+0.0655),
> i.e. the contribution of preprocessing has been measured separately from the contribution of the
> SSL initialization.
>
> ⚠️ **Provenance needs syncing.** The numbers were taken from `VALUES.md`. The raw run artifacts
> (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`) were **absent from
> `experiments/outputs/`** at the time of the update (the latest files there date from 2026-07-30),
> and `results/data/*.json` contain numbers from the **previous** run. This must be closed out
> before the chapters are written — see `data/MANIFEST.md` and `TODO_BEFORE_WRITING.md`.
>
> GPU locally: WSL Ubuntu + conda `dr-classifier` (torch cu121, RTX 3060), paths `/mnt/e/...`;
> the system Python `C:\Python312` is CPU-only — call WSL for GPU work.

> 🚫 **The provenance of this folder is internal. It does not carry over into the dissertation or
> into `defense/`.** Run dates ("the 2026-08-02 run"), the history of recomputations ("the previous
> run gave the opposite verdict"), artifact paths (`experiments/outputs/**`, `VALUES.md`,
> `summary.json`, `*.log`) and checkpoint identifiers are needed here for traceability — and only
> here. When prose is carried from `findings/` into the chapters, the result is stated as a property
> of the experiment, not of a dated run: "Experiment 1 yielded ΔwF1 +6.55 pp", not "the 2026-08-02
> run yielded…". Methodological facts (number of folds, sample sizes, stopping rule, single-fold
> evaluation as a limitation) must be carried over. Rule:
> `thesis/prompts/writing-session-system-prompt.md` §16; on output it is duplicated by the scrubber
> in `md2gost.py` (`strip_process_metadata`).

**Purpose.** A single entry point for assembling the experimental results and writing the
experimental chapters (ch. 4 "Experiments", ch. 5 "Validation", ch. 7 "Conclusion"). Assembled so
that **a new chat can continue the work by reading only this folder**, without re-exploring the
repository (token savings).

Candidate: Yesmukhamedov N.S., IITU. Topic: "Automated Diabetic Retinopathy Diagnosis via
Fundus Image Enhancement and CNN Classification". Central thesis: **model = preprocessing + CNN**
(the 8-stage preprocessing pipeline is an integral component of the model, not data preparation).

## How to continue in a new chat (read in this order)

1. **[STATUS.md](STATUS.md)** — status of all experiments + metrics and verdicts of the 2026-08-02 run.
2. **[INTEGRITY_NOTE.md](INTEGRITY_NOTE.md)** — ⚠️ discrepancy between demo/defense and the real data,
   plus the state of provenance. Mandatory reading before touching any numbers/figures.
3. **[CHAPTER_STATUS.md](CHAPTER_STATUS.md)** — what has been written in the dissertation, what is
   unblocked, what each section needs.
4. **[GAP_ANALYSIS.md](GAP_ANALYSIS.md)** — ✅/⬜ checklist: is everything assembled for the
   dissertation / presentation / demo; what is missing and how to obtain it.
5. **[HYPOTHESIS_COVERAGE.md](HYPOTHESIS_COVERAGE.md)** — reconciliation of the letter of
   `thesis/governance/HYPOTHESIS.md` with the actual artifacts (gaps G-1…G-12: what the run closed,
   what remains).
6. **[TOOLING.md](TOOLING.md)** — which metric/statistics/figure scripts to reuse.
7. **[hypotheses/](hypotheses/)** — verdict cards for each hypothesis (H-1…H-7 + exp7/SSL).
8. **[findings/](findings/)** — narrative conclusions for each experiment (draft prose for the chapters).
9. **[tables/](tables/)** — ready-made tables (source for TAB-4.x / TAB-5.x).
10. **[data/](data/)** — canonical result files (+ [MANIFEST](data/MANIFEST.md)).
    ⚠️ **contain numbers from the previous run** — require re-synchronization.

## Strategy (after the 2026-08-02 run)

- **The work rests on confirmed hypotheses.** 6 of 7 are confirmed, the pipeline effect is stable
  across all scenarios (in-domain, zero-shot, device change, external clinic, small data), remains
  significant after correction for multiplicity, and does not depend on the backbone.
- **The end-to-end mechanism is measured, not postulated.** H-3 shows a reduction in domain distance
  (MMD/KL, 6/6 domains); the exp2 ablation decomposes the gain across stages; and the same pattern
  recurs in every experiment (Δκ > ΔwF1, Δmacro-F1 > ΔwF1, ΔSens ≈ +0.10 with rising Spec).
  See `findings/summary-and-dominance.md`.
- **The boundaries of the claims are kept alongside the results** — this strengthens the work rather
  than weakening it. `INVARIANTS.md` remains in force: **NC-14** (Grad-CAM ≠ clinical localization) —
  for H-5 what is claimed is attention alignment, confirmed on 4/4 lesion types; the H-4/H-6
  thresholds apply to both arms, so the difference between arms rests on the comparison with baseline
  and on the reduction in spread, not on the threshold itself; H-7 is reported as partial — with an
  analysis of the bias in the Δ_drop metric, which itself goes into §5.4 as a contribution. The full
  list is in `findings/summary-and-dominance.md`, section "Limits of applicability and directions for
  further work".
- **Only numbers from this folder** (and from `experiments/outputs/` after synchronization). Do not
  use numbers from the demo/defense — see `INTEGRITY_NOTE.md`.

## Boundaries of this session

Done: all values and verdicts in `STATUS`, `tables/`, `hypotheses/`, `findings/` and the top-level
documents have been rewritten for the 2026-08-02 run, preserving the previous structure. Two new
files were added: `hypotheses/H-3.md` + `tables/H-3_domain_distance.md` (domain distance) and
`tables/exp2_flatfield_sigma_sweep.md` (σ sweep, not previously run).
**Not done:** synchronizing `data/*.json` and `experiments/outputs/` with the raw run artifacts
(they are not on disk).

## Next steps — working checklist

➡️ **[TODO_BEFORE_WRITING.md](TODO_BEFORE_WRITING.md)** — the canonical list. In brief:

- [ ] **Synchronize provenance** — publish the raw artifacts of the 2026-08-02 run into
      `experiments/outputs/` and update `results/data/*.json`. Blocks carrying numbers into the chapters.
- [ ] **G-3** — qualitative Grad-CAM overlays on the clinical (KZ) dataset; the only gap still open
      with respect to the wording of H-5 (`exp4_explainability.py` has no clinical branch).
- [ ] **Remainder of G-8** — isolate Stage 3 (FOV mask): requires a flag + a 3-channel model variant.
- [ ] **Synchronize demo/defense** with the real numbers (`demo/web/src/data.js`,
      `demo/web/generate_charts_*.py`, `defense/figures/`). Academic integrity ahead of the defense.
- [ ] **Write chapters 4/5/7/0** from the material in `findings/` + `tables/`
      (workflow: brief→draft→continuity→review→translation).

## Provenance

Revision of **2026-08-02**: values and verdicts carried over from `VALUES.md` (run of 02.08.2026).
The previous revision (2026-07-24…28) was assembled directly from `experiments/outputs/` and
contained the opposite verdicts — it has been fully replaced. The source of truth for metrics remains
`experiments/outputs/`; until the new run's artifacts appear there, `VALUES.md` is the sole carrier
of these numbers.
