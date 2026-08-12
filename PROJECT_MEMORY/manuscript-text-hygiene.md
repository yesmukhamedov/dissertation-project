---
name: manuscript-text-hygiene
description: Internal notation that reached the reader-facing manuscript — what was removed, and the 356 undefined governance codes still open before submission
metadata:
  type: project
---

The drafts were written in the project's own notation and a lot of it reached the
page. Three classes were cleaned out of the body on 2026-08-13 (both editions,
sources edited in PART 1 only so the compliance checklists keep their references):

**Resource IDs — 40 occurrences.** `TAB-3.1`, `FIG-2.2`, `DIA-6.3a`. The mapping
was not the identity: seven tables were captioned by their asset ID and take their
document number from order of appearance, so `TAB-3.2`→Table 3.1, `TAB-3.3`→Table
3.2, `TAB-3.1`→Table 3.3 **and** Table 4.2 where §4.1.3 repeats it. Sixteen
Chapter-4/5 captions already recorded their own mapping in parentheses, which is
where those pairs came from. `TAB-5.4` was cited for figures no table in the
manuscript carries — it lives in `results/` — and its numbers are Table 4.10 and
Table 4.20 verbatim.

**Governance document names — 27 occurrences.** `RESEARCH_ARCHITECTURE` ×21,
`INVARIANTS` ×5, `CENTRAL_THESIS` ×1, always as a parenthetical provenance
citation. Three cited a literal `§X`, an unresolved cross-reference.

**Version markers in prose — 4.** The `INVARIANTS v6.0.0` citations, plus "acquired
in the **v6.1.0** corpus expansion" in §2.C/§3.C, which is process history too.
Note the scrubber in `md2gost.py` only matches V3/V4/V5, so **v6.x passes straight
through** — see [[strip-version-markers]] and [[no-process-history-in-deliverables]].

## OPEN — decide before submission

**356 governance *codes* remain in the body and none is defined for the reader**:
`SB` ×71, `OD` ×66, `SIR` ×54, `PC` ×42, `NC` ×36, `EH` ×34, `DGL` ×33, `CFC` ×13.
(The 128 `H-x` are hypotheses and are properly introduced in §0.6; `PC-x` are at
least introduced in context by §0.8.) None of the eight families appears in
`DESIGNATIONS AND ABBREVIATIONS` or in `DEFINITIONS` — and **`OD` is listed there
as "Optic Disc"**, so a reader meeting `OD-3 Stage 5` is pointed at the wrong
expansion.

Two resolutions, and they differ in how the dissertation reads to a reviewer:
declare the families in the front matter, or strip the codes from the body. This
is the candidate's call. See [[gost-export-toolchain]] for the build that renders
all of this.
