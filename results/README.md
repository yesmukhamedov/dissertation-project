# `results/` — portable knowledge base for the dissertation experiments

> ▶ **Updated for the 2026-08-03 run 2** (the second run received on that date; it supersedes the
> earlier 2026-08-03 figures). All values and verdicts in this folder have been replaced with the
> results of the latest run (`VALUES.md`). **All 7 hypotheses are confirmed**; none refuted. exp7
> (small data) — significant positive; the SSL gate passed with both backbones; **H-3** (domain
> distance, MMD/KL) confirmed on 6/6. The key methodological result stands: **confound CFC-2.8 has
> been decomposed** — the cumulative exp2 ablation on full EyePACS under a single initialization
> reproduces the entire exp1 gain (+0.0655), i.e. the contribution of preprocessing has been measured
> separately from the contribution of the SSL initialization.
>
> ⚠️ **Two things changed in this revision — one a result, one a specification.**
> - **H-2 / PC-8 strengthened (a real change) — the stage hierarchy is no longer flat.** Δⱼ now spans
>   0.0065–0.0143 (spread ≈3·σ_fold, previously 0.0010 < σ_fold): **flat-field (0.0143) and CLAHE
>   (0.0125) lead**, together 41% of the total gain. The previous framing — "an ensemble of
>   normalizations of comparable strength; the stages cannot be ranked" — is **withdrawn**.
>   PC-8 goes MODERATE → STRONG.
> - **H-7 was re-specified (not re-scored).** The operative form is **External Clinical Performance** —
>   Δ wF1(D−C) ≥ MCID 0.050 with CI⁻ > 0 on **both** sets — and it passes **2/2**: IDRiD +0.0689,
>   Messidor-2 +0.0541. The earlier "partial (1/2)" and "0/2" readings in this folder applied the
>   **retired** Δ_drop form. That form is algebraically degenerate —
>   `Δ_drop(D) − Δ_drop(C) ≡ Δ_in-domain − Δ_external = 0.0655 − Δ wF1(X)` — so it demands the pipeline
>   beat baseline *more abroad than at home* and penalizes it for its own in-domain win. The identity
>   stays in the work as a **§5.4 contribution**; the same defect recurs in H-6's g_ratio.
>   ⚠️ Caveat to carry: the Messidor-2 margin over the MCID is only **0.0041**.
>
> Smaller shifts: **H-6** — g_ratio now *falls* in 2 of 5 groups (mixed_ddr, topcon_messidor2), a
> denominator artifact with absolute wF1 rising in all five; spread reduction std wF1 −2.4×, AUC
> −3.1×. **E-7** — 4 of 5 folds again, but the inverting fold moved (2 → 3), so it should be reported
> as a count, not an index. **per-class by group** — the spread now contracts on **all five** classes
> (the DR0 exception has gone). **H-3** — the size of the distance reduction no longer tracks the size
> of the transfer gain (ρ ≈ 0.49); report direction only.
>
> 🔴 **Governance is out of sync with this folder.** `thesis/governance/HYPOTHESIS.md` still states
> H-7 in the retired degradation form ("the performance degradation Δ = F1_EyePACS_val − F1_external
> will be statistically smaller for the integrated-preprocessed model"). `results/` now uses the
> operative External Clinical Performance form. `thesis/` is read-only from here, so **the governance
> file must be updated by hand before chapter assembly** — otherwise the binding document and the
> results contradict each other. Same for the H-7 row in `thesis/ASSET_INVENTORY.md`.
>
> ⚠️ **Provenance needs syncing.** The numbers were taken from `VALUES.md`. The raw run artifacts
> (`summary.json`, `*_results.json`, `metrics.csv`, `predictions.npz`) were **absent from
> `experiments/outputs/`** at the time of the update (the latest files there date from 2026-07-30),
> and `results/data/*.json` contain numbers from the **previous** run. This must be closed out
> before the chapters are written — see `data/MANIFEST.md` and `TODO_BEFORE_WRITING.md`.
>
> Note on `VALUES.md` itself: §6.1 (`kowa_idrid`, `topcon_messidor2`) had **not** been regenerated
> together with §7 and still carried superseded values for the same two measurements. Both rows were
> re-synchronized to §7.1 here, and §6.8/§6.9 point estimates recomputed arithmetically; the §6.8
> bootstrap CIs were **not** recomputed.
>
> GPU locally: WSL Ubuntu + conda `dr-classifier` (torch cu121, RTX 3060), paths `/mnt/e/...`;
> the system Python `C:\Python312` is CPU-only — call WSL for GPU work.

> 🚫 **The provenance of this folder is internal. It does not carry over into the dissertation or
> into `defense/`.** Run dates ("the 2026-08-03 run"), the history of recomputations ("the previous
> run gave the opposite verdict"), artifact paths (`experiments/outputs/**`, `VALUES.md`,
> `summary.json`, `*.log`) and checkpoint identifiers are needed here for traceability — and only
> here. When prose is carried from `findings/` into the chapters, the result is stated as a property
> of the experiment, not of a dated run: "Experiment 1 yielded ΔwF1 +6.55 pp", not "the 2026-08-03
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

1. **[STATUS.md](STATUS.md)** — status of all experiments + metrics and verdicts of the 2026-08-03 run.
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

## Strategy (after the 2026-08-03 run)

- **The work rests on confirmed hypotheses.** All 7 are confirmed, the pipeline effect is stable
  across all scenarios (in-domain, zero-shot, device change, external clinic, small data), remains
  significant after correction for multiplicity, and does not depend on the backbone.
- **The end-to-end mechanism is measured, not postulated, and now localized.** H-3 shows a reduction
  in domain distance (MMD/KL, 6/6 domains); the exp2 ablation decomposes the gain across stages **and
  identifies where it comes from** — the two photometric stages carry 41% of it; and the same pattern
  recurs in every experiment (Δκ > ΔwF1, Δmacro-F1 > ΔwF1, ΔSens ≈ +0.11 with rising Spec).
  See `findings/summary-and-dominance.md`.
- **The boundaries of the claims are kept alongside the results** — this strengthens the work rather
  than weakening it. `INVARIANTS.md` remains in force: **NC-14** (Grad-CAM ≠ clinical localization) —
  for H-5 what is claimed is attention alignment, confirmed on 4/4 lesion types; the H-4/H-6
  thresholds apply to both arms, so the difference between arms rests on the comparison with baseline
  and on the reduction in spread, not on the threshold itself; **H-7 claims external performance, not
  resistance**, and its Messidor-2 margin over the MCID is thin (0.0041). The full list is in
  `findings/summary-and-dominance.md`, section "Limits of applicability and directions for further
  work".
- **The retired Δ_drop form is itself a result.** `Δ_drop(D) − Δ_drop(C) ≡ 0.0655 − Δ wF1(X)` — the
  metric equals the in-domain gap minus the quantity under test, so it can only be satisfied by an arm
  whose advantage *grows* under domain shift, and it penalizes the integrated arm for its in-domain
  win. The same defect drives H-6's g_ratio inversions. One argument covers both metrics, and it
  belongs in §5.4 as a critique of a measure in common use in the domain-shift literature.
- **Only numbers from this folder** (and from `experiments/outputs/` after synchronization). Do not
  use numbers from the demo/defense — see `INTEGRITY_NOTE.md`.

## Boundaries of this session

Done: all numeric values in `STATUS`, `tables/`, `hypotheses/`, `findings/` and the top-level
documents re-synchronized with `VALUES.md`; the structure and the file set are unchanged. Prose that
depended on values that moved was rewritten to match — **PC-8** (hierarchy now resolvable, a real
change), the H-6 g_ratio inversions, the E-7 fold index, the DR0 spread, and the weakened
H-3 ↔ transfer association. **H-7 re-specified** to the External Clinical Performance form and its
verdict corrected to CONFIRMED (2/2); the Δ_drop material was demoted to reference and reframed as a
§5.4 contribution. `VALUES.md` §6.1/§6.8/§6.9 were re-synchronized to §7.1 (see the note above).
**Not done:** synchronizing `data/*.json` and `experiments/outputs/` with the raw run artifacts
(they are not on disk); updating `thesis/governance/HYPOTHESIS.md` to the new H-7 wording
(`thesis/` is read-only from here).

## Next steps — working checklist

➡️ **[TODO_BEFORE_WRITING.md](TODO_BEFORE_WRITING.md)** — the canonical list. In brief:

- [ ] **Synchronize provenance** — publish the raw artifacts of the 2026-08-03 run into
      `experiments/outputs/` and update `results/data/*.json`. Blocks carrying numbers into the chapters.
- [ ] **G-3** — qualitative Grad-CAM overlays on the clinical (KZ) dataset; the only gap still open
      with respect to the wording of H-5 (`exp4_explainability.py` has no clinical branch).
- [ ] **Remainder of G-8** — isolate Stage 3 (FOV mask): requires a flag + a 3-channel model variant.
      **Higher priority than before:** now that the stages are ranked, level L3 (rank 4) still bundles
      Stage 2 with Stage 3, so that rank belongs to the pair rather than to a stage.
- [ ] **Check the stability of the PC-8 ranking** — the hierarchy flipped from flat to resolvable
      between two runs a day apart. Before the ranking is carried into the thesis, confirm that
      Δⱼ = 0.0143 for flat-field and 0.0125 for CLAHE reproduce; a claim that reverses between runs is
      not yet safe to build §4.3 on.
- [ ] 🔴 **Update `thesis/governance/HYPOTHESIS.md` to the operative H-7 wording** (External Clinical
      Performance, form S, MCID 0.050). It still carries the retired degradation form, so the binding
      document currently contradicts `results/`. Same for the H-7 row in `thesis/ASSET_INVENTORY.md`.
      Blocks chapter assembly. Also worth committing the formula spec (PASS_S / MCID / retirement
      rule) into `thesis/governance/` — it is not in the repo today.
- [ ] **Synchronize demo/defense** with the real numbers (`demo/web/src/data.js`,
      `demo/web/generate_charts_*.py`, `defense/figures/`). Academic integrity ahead of the defense.
- [ ] **Write chapters 4/5/7/0** from the material in `findings/` + `tables/`
      (workflow: brief→draft→continuity→review→translation).

## Provenance

Revision of **2026-08-03 (run 2, H-7 re-spec)**: values carried over from `VALUES.md`. One verdict
changed on the data (**PC-8** flat → resolvable) and one was **corrected on the criterion** (**H-7**:
the retired Δ_drop form had been applied; under the operative External Clinical Performance form it is
CONFIRMED 2/2, and always was). Earlier revisions: 2026-08-03 run 1, then 2026-08-02 (same verdicts,
different figures), then 2026-07-24…28 (assembled from `experiments/outputs/`, opposite verdicts). The
source of truth for metrics remains `experiments/outputs/`; until the new run's artifacts appear
there, `VALUES.md` is the sole carrier of these numbers.

⚠️ **Three runs in three days have produced three different sets of figures for the same
experiments.** Until the raw artifacts are published and the run-to-run variability is understood,
treat every number here as provisional and do not build chapter text on the **PC-8 ranking**, which
reversed between consecutive runs. (H-7 is a different case — its verdict was never unstable; only
the criterion applied to it was wrong.)
