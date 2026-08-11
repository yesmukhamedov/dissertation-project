# SECTION BRIEF
## Appendix C — System Architecture UML Diagrams

**Chapter:** Appendices (back matter)
**Section Function:** discharge DIA-6.3 — give the formal structural views that Chapter 6 specifies in prose
**Word Count Target:** prose 600–900 words; the diagrams carry the appendix

> **Gate check:** PASSED. This is the one blocked appendix that was never experiment-gated: DIA-6.3 is an
> **asset task**, and the asset is authorable from Chapter 6 without any new measurement. The diagrams are
> supplied as **diagram source** (Mermaid), which is the definition of the diagram rather than a rendering
> of it, and is therefore content rather than a placeholder. Rendering is a conversion-time step.

---

### GOVERNANCE BINDINGS

**Primary claims:** PC-5 (modular screening-system architecture) — **DESIGN/THEORETICAL**; SC-5.1.
**Scope boundaries:** **SB-4.1** (design specification; no prototype, no field test), **SB-4.2** (GDPR/HIPAA-*aligned*, not certified), SB-1.3 (decision support, physician-in-the-loop), SB-4.3.
**Non-claims:** NC-9, NC-14 (the overlay is an interpretability artefact, not a localisation output), NC-3.
**Operational definitions:** OD-3 (the pipeline the Preprocessing Engine realises), OD-6 (the envelope that prunes the topology).
**Forbidden claims:** CFC-2.4, CFC-2.3.

---

### CONTENT SPECIFICATION

**Section objective:** Make the Chapter-6 decomposition inspectable — a reader should be able to check the
module set, its interfaces, its deployment topology and its persisted entities against Tables 6.1–6.3.

**Structure:**
- **Opening.** What these diagrams are and, immediately, what they are not: a design specification, not a
  built system. No prototype was implemented and no deployment was tested (SB-4.1). Note the notation and
  that the diagrams are given as source, to be rendered at conversion.
- **C.1 Component view** — the seven modules of Table 6.3 with their provided/required interfaces, the
  external systems they meet, and the module → FR → NFR mapping restated as a table so the diagram is
  traceable to the requirements rather than merely illustrative.
- **C.2 Deployment view** — the store-and-forward topology: peripheral capture site, reading-centre
  processing node, hospital information systems. This is the view where OD-6 does its pruning, and the
  reason for the asynchronous boundary belongs here (NFR-4).
- **C.3 Sequence view** — one screening episode end to end, from capture to persisted clinician
  disposition. Two things must be visible in the ordering: the clinician's disposition is the terminal
  step (SB-1.3), and the overlay accompanies the grade as decision support (FR-4, NC-14).
- **C.4 Data view** — the persisted entity model, with the entities that carry patient identity marked,
  since that is where NFR-7 concentrates. The audit record is an entity, not an afterthought.
- **Close.** The status of the whole: each diagram is a specification satisfying Chapter 6's requirement
  tables, and none is evidence that the system works.

---

### SOURCE MAPPING

| Source | Role | Content |
|---|---|---|
| §6.1.1 (Tables 6.1, 6.2) | binding | FR-1…FR-7, NFR-1…NFR-8 |
| §6.1.2 (Table 6.3) | binding | the seven modules and their FR/NFR mapping; the asynchronous PACS/EHR boundary |
| §6.2.1, §6.2.2 | binding | Preprocessing Engine configurability; inference and model selection |
| §6.3.1, §6.3.2 | binding | telemedicine topology; the physician-in-the-loop interface and override channel |
| §6.4.1 | binding | security concentration at the data-management boundary |

**⚠️ Nothing is invented.** Every module, interface, node and entity must be traceable to a Chapter-6
statement. Where the diagram needs a detail Chapter 6 does not fix, the detail is omitted rather than chosen.

---

### BOUNDARY WARNINGS

1. **SB-4.1 in the opening and again in the close.** A diagram invites being read as a built system.
2. **SB-4.2 / NC-9** wherever security appears: aligned by design, never certified.
3. **NC-14** at the overlay: an interpretability artefact accompanying a grade, not a localisation output.
4. **SB-1.3** in the sequence: the clinician is the terminal decision-maker, not a notified party.
5. **No performance figure, no latency claim, no throughput number.** The envelope is qualitative here;
   the measured computational cost belongs to §5.3.2 and is not restated.
6. **Rule 16** — no process history.

---

### ACCEPTANCE CRITERIA

- [ ] Four views present: component, deployment, sequence, data.
- [ ] Module → FR → NFR traceability table present.
- [ ] Every element traceable to Chapter 6; nothing invented.
- [ ] SB-4.1 at the opening and the close; SB-4.2 at security; NC-14 at the overlay; SB-1.3 in the sequence.
- [ ] No metric value of any kind.

---

### WRITING DIRECTIVES

- **Tense:** present — a specification is stated, not narrated.
- **Notation:** Mermaid, given as fenced source blocks with a caption above each; one short reading note
  per diagram saying what to look at, not what to conclude.
