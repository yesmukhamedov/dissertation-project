---
name: defense-language-kazakh
description: The defense is held in KAZAKH — the Kazakh edition is the defended volume, and every abstract cites its page count regardless of the abstract's own language
metadata:
  type: project
---

**The language of the defense is Kazakh.** The Kazakh edition of the dissertation is therefore the
**defended volume**, and the English edition is a translation of it rather than the primary artifact.

Two consequences, both already applied and neither to be "corrected" back:

1. **All three abstracts cite the Kazakh edition's volume — 113 pages since 2026-08-23** (265 before the four-chapter rewrite) — including the English one.
   An abstract describes *the dissertation submitted for defense*, not the edition it happens to be
   written in, so the English abstract citing the English edition's own page count would name a
   volume that is not the one being defended. EN/RU/KZ all read **113 pp, 19 tables, 16 figures,
   102 sources**, appendices excluded; see [[abstract-annotation-alignment]] and
   [[four-chapter-rewrite]].

   > **History: 264 → 265 on 2026-08-14 → 117 on 2026-08-20 → 118 on 2026-08-21 → 113 on
   > 2026-08-23**, the last step being the illustration-height cap, which took five pages out of
   > each edition. The registry of record is `council/METADATA.toml` (`pages_kz = 113`,
   > `pages_en = 102`, both excluding appendices; with appendices the exported volumes run
   > 143 KZ / 130 EN) — take it from there, never from an older document.

2. **The manuscript states each edition's own count — EN 102, KZ 113 — and that is correct as it
   stands**: there the document describes itself. Do not sync those to one another, nor to the
   abstract figure; the abstract and the introduction answer different questions. (Before the
   rewrite the same rule read 238 EN / 265 KZ, in §0.16.)

   Because the introduction states the count, the count and the export are a **fixed point**:
   re-measure after every re-export, write the result into the introduction and the registry, then
   re-export and confirm the figure did not move again.

Confirmed by the candidate 2026-08-13, when the page count for the Russian abstract was decided.
Related: [[people-and-identifiers]], [[council-docs-skill]].
