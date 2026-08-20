# SECTION BRIEF
## Appendix B — Supplementary Experimental Results and Confusion Matrices

**Chapter:** Appendices (back matter)
**Section Function:** put the per-class and error-structure evidence behind Chapters 4–5 on the record, in full, so a reader can audit the aggregate figures
**Word Count Target:** prose 700–1,000 words; the tables carry the appendix

> **Gate check:** PASSED **with a bounded scope.** The data exist in `results/`. What does **not** exist
> is equally binding: per-epoch training trajectories and per-class curves were not retained, and
> ROC/PR curves require per-sample prediction dumps that are not available. The appendix reports what
> was recorded and **states what was not, and why**, rather than silently omitting it.

---

### GOVERNANCE BINDINGS

**Evidence thresholds:** EH-1 (metric hierarchy), EH-2 (per-class figures are supplementary and cannot establish a hypothesis).
**Forbidden claims:** CFC-2.1, CFC-2.2, CFC-2.4, CFC-2.5, **CFC-2.8**.
**Non-claims:** NC-17.
**Scope boundaries:** SB-2.1 (imbalance conditions every per-class figure), SB-1.10 (calibration is not clinical reliability), SB-3.1.
**Source rules:** SIR-1 — no reading stronger than the section that established it.

---

### CONTENT SPECIFICATION

**Section objective:** Supply the decomposition the main text summarises, at the level of the class and the
confusion cell, without re-adjudicating anything.

**Structure:**
- **Opening (short).** What the appendix is for, and the standing condition: the grade distribution is
  severely imbalanced, so every per-class figure must be read against its class size, and the class sizes
  are given first. **EH-2:** these figures are supplementary and establish no hypothesis on their own.
- **B.1 Per-class metrics on the training corpus**, all four configurations — F1, precision, recall, plus
  macro-F1. One table per configuration or one combined table.
- **B.2 Confusion matrices on the training corpus**, all four configurations, rows = truth.
- **B.3 Confusion matrices on the external public corpus**, both arms.
- **B.4 Calibration** — ECE and Brier for all four configurations. **SB-1.10 attached.**
- **B.5 Convergence and overfitting** — per-fold best epoch, train and validation loss at best epoch, and
  the loss gap, for all four configurations. This is the *only* convergence evidence retained.
- **B.6 Interval estimates** — the between-fold cross-validation intervals and the per-instance bootstrap
  intervals, side by side, with the distinction between what each quantifies stated.
- **B.7 Referable-DR screening metrics in-domain** — sensitivity, specificity, PPV, NPV, referable AUC.
- **B.8 What this appendix does not contain**, with the reason for each absence: per-epoch training
  curves (not retained); per-class ROC and precision–recall curves (require per-sample prediction dumps
  that were not saved); per-camera-group confusion matrices (not recorded — see Appendix F).

**Interpretive notes:** one or two sentences per table at most, and never above the strength the
originating section established. The appendix does not argue.

---

### SOURCE MAPPING

| Source | Role | Content |
|---|---|---|
| `results/tables/exp1_per_class.md` | data | per-class F1/P/R and the four confusion matrices |
| `results/tables/per_class_and_confusion.md` | data | external-corpus confusion matrices |
| `results/tables/TAB-4.3_exp1_calibration.md` | data | ECE, Brier |
| `results/tables/exp1_convergence_ci.md` | data | per-fold best epoch, losses, CV and bootstrap intervals |
| `results/tables/TAB-5.4_clinical_referable.md` | data | in-domain referable metrics |

**⚠️ Every figure is transcribed, not recomputed.** No derived quantity may be introduced that the source
tables do not carry.

---

### BOUNDARY WARNINGS

1. **No new number.** Transcription only; nothing computed, averaged or rounded differently.
2. **Rule 16 is the live risk here.** The source tables carry run dates, `VALUES.md` section pointers and
   revision narrative. **None of that may cross into the appendix.** Report a result as a property of the
   experiment, never of a dated execution of it.
3. **CFC-2.8** — any comparative remark concerns configurations, never preprocessing alone.
4. **SB-2.1 first**, before any per-class figure is shown.
5. **SB-1.10** with the calibration table.
6. **The absences are content**, not an apology. Each gets its reason.

---

### ACCEPTANCE CRITERIA

- [ ] Class sizes given before the first per-class table.
- [ ] All four configurations present in B.1, B.2, B.4, B.5, B.6, B.7.
- [ ] Both arms present in B.3.
- [ ] SB-1.10 attached to calibration; SB-2.1 attached to the per-class framing.
- [ ] B.8 present, with a reason for each of the three absences.
- [ ] No run date, no artifact path, no revision narrative.

---

### WRITING DIRECTIVES

- **Tense:** past for what was measured; present for what a table shows.
- **Register:** documentary. The appendix is a record, not an argument.
