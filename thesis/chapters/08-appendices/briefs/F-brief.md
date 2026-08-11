# SECTION BRIEF
## Appendix F — Device Domain-Shift Supplementary Tables

**Chapter:** Appendices (back matter)
**Section Function:** put the full per-group evidence behind §4.8 on the record, including the per-class decomposition the main text only summarises
**Word Count Target:** prose 700–1,000 words; the tables carry the appendix

> **Gate check:** PASSED, bounded. The per-group and per-class data exist. **Per-group confusion matrices
> were not recorded** — only per-class F1 by group — so the error *composition* within a group cannot be
> shown, and the appendix says so rather than substituting something else.

---

### GOVERNANCE BINDINGS

**Primary claims:** PC-9 — STRONG, with three travelling qualifications.
**Non-claims:** **NC-16** (no device certification, no device-agnostic readiness), NC-17.
**Forbidden claims:** CFC-2.1, CFC-2.2, CFC-2.4, CFC-2.5, CFC-2.8.
**Scope boundaries:** SB-1.8, SB-2.3 (taxonomy and equipment heterogeneity), SB-3.1.
**Evidence thresholds:** EH-1, EH-2.
**Source rules:** SIR-1, SIR-3.

---

### CONTENT SPECIFICATION

**Section objective:** Give the group-level detail at the resolution the record supports, and mark clearly
where that resolution stops.

**Structure:**
- **Opening.** What the appendix contains, and the three conditions that govern every table in it, stated
  before the first one: two of the five groupings **are** the external clinical corpora of Experiment 5
  and coincide with them by construction rather than replicating them; three groupings aggregate more
  than one camera model and therefore identify a device family rather than a device; and the evaluation
  uses the models of a single fold, so the dispersion reported is **between groups**, not between folds.
- **F.1 Group composition** — group sizes and per-group class sizes.
- **F.2 Weighted F1 and retention ratio by group** — both arms, the paired difference and its interval,
  and the ratio for each arm with the floor.
- **F.3 ROC-AUC and κ by group** — both arms, with the AUC difference and its interval.
- **F.4 Referable-DR AUC by group** — both arms.
- **F.5 Per-class F1 by group** — one table per arm, with macro-F1.
- **F.6 Between-class dispersion** — the span of each class across the five groups, both arms.
- **F.7 Between-group dispersion** — the standard deviations and their reduction, with the interval.
- **F.8 The retention-ratio artefact.** The ratio divides by each arm's own in-domain figure, so the
  integrated arm's denominator is larger and a group must gain proportionally just to hold its ratio.
  Report the two groups where the ratio falls while absolute performance rises, and connect it to the
  same structural defect identified in §5.4 — **descriptive, rehabilitating nothing**.
- **F.9 What is not included** — per-group confusion matrices were not recorded; the consequence is that
  within-group error composition is an open question, exactly as §4.8 and §5.4 state.

---

### SOURCE MAPPING

| Source | Role | Content |
|---|---|---|
| `results/tables/TAB-4.9_exp6_device.md` | data | group sizes, wF1, g_ratio, AUC, κ, referable AUC, between-group dispersion |
| `results/tables/per_class_and_confusion.md` | data | per-class F1 by group, per-group class sizes, per-class spans |
| §4.8 | binding | the established reading and its three qualifications |
| §5.4 | binding | the normalisation defect, as a descriptive contribution |

**⚠️ Every figure is transcribed, not recomputed.**

---

### BOUNDARY WARNINGS

1. **NC-16 in the opening and again at the close.** A per-device table invites a compatibility reading.
2. **The two coinciding groups must be flagged before the tables**, not after — otherwise the five rows
   read as five independent observations.
3. **No new number**; in particular no dispersion statistic is recomputed.
4. **The retention-ratio artefact is descriptive.** It explains a table; it rescues nothing.
5. **CFC-2.8** — all comparison is between configurations.
6. **Rule 16** — the source tables carry run dates, source-file pointers and revision narrative;
   **none may cross over.**

---

### ACCEPTANCE CRITERIA

- [ ] Three governing conditions stated before the first table.
- [ ] F.1–F.7 present with both arms throughout.
- [ ] Retention-ratio artefact explained and bounded as descriptive.
- [ ] F.9 present: per-group confusion matrices unrecorded, with the consequence.
- [ ] NC-16 at the opening and the close.
- [ ] No run date, no artifact path, no revision narrative.

---

### WRITING DIRECTIVES

- **Tense:** past for what was measured; present for what a table shows.
- **Register:** documentary; the appendix records, it does not argue.
