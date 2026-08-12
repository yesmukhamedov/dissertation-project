---
name: manuscript-text-hygiene
description: Internal notation that reached the reader-facing manuscript — resource IDs, governance doc names and version markers removed; the 356 governance codes DECLARED in the abbreviations (2026-08-13)
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

## Governance codes — DECLARED, not stripped (2026-08-13)

The fourth class was the 356 codes themselves — `SB` ×71, `OD` ×66, `SIR` ×54,
`PC` ×42, `NC` ×36, `EH` ×34, `DGL` ×33, `CFC` ×13 — and the resolution chosen was
**declaration**. All eight families now have a row in `DESIGNATIONS AND
ABBREVIATIONS`, EN and KZ, in `thesis/output/abbreviations_{en,kz}.md`.

**Write the family as `SB-n`, not `SB`.** The numbered form is how the codes always
appear in the text, and it is what makes them read as a system rather than as
ordinary abbreviations. It is also what resolves the **`OD` collision**: `OD`
(Optic Disc) keeps its own row and `OD-n` (Operational Definition) sits directly
after it, closing with the rule that separates them — the optic disc is never
written with a number.

Each row says what the family **is** for a reader with no access to the governance
documents (a scope boundary; a rule on what may be attributed to a source), never
where it is recorded — naming the documents is what the 27-occurrence cleanup above
removed.

**Three further families were removed instead of declared — 9 occurrences per
edition.** `IT-1` ×4, `SC-1.4` ×3, `AOQ-2` ×2, all bare provenance parentheticals
whose sentences already carried the content; `(AOQ-2 simplified)` was process
history as well. One needed rewording, not deletion: §3.3.1's "the five-class
taxonomy of IT-1" → "the dissertation's five-class taxonomy". Declaring three more
families for nine markers would have bought the reader nothing.

**`FR-n`/`NFR-n` (118 occurrences) are deliberately left undeclared** — §6.1.1
defines each in its own table on the page where it first appears.

**Verify in the built `.docx`, not the Markdown** — the front matter is prepended
at assembly and the abbreviations table is rendered as a Word table, so a grep over
`thesis/assembly/*.md` alone does not prove what the reader sees. The rebuild after
this change moved nothing: front matter stayed 10 pages EN / 11 KZ and §0.16's
239 / 266 still match (appendices begin p. 240 EN, p. 267 KZ). See
[[gost-export-toolchain]] for the build that renders all of this.
