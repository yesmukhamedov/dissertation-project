# Output Directory

Council deliverables staged as Markdown. These are the **sources**; the GOST `.docx`/`.pdf`
renderings are built from them by the `council-docs` skill into `defense/docs/`.

| File(s) | Deliverable |
|---------|-------------|
| `abstract_{en,ru,kz}.md` | Trilingual abstract (annotation) |
| `titlepage_{en,kz}.md` | Title page (reads the metadata registry) |
| `contents_{en,kz}.md` | Table of contents |
| `normative_references_{en,kz}.md` | Normative references |
| `abbreviations_{en,kz}.md` | Designations and abbreviations |
| `definitions_{en,kz}.md` | Definitions |
| `supervisor_review_kz.md` | Supervisor's review |
| `foreign_consultant_review_en.md` | Foreign consultant's review |
| `reviewer_{1,2}_review_{en,ru,kz}.md` | Reviewers' reports (Appendix 3 form) — 1 = Bektemyssova G.U., 2 = Chinibayeva T.T. |
| `publications_list_ru.md` | List of scientific papers |
| `predefense_protocol_{ru,kz}.md` | Extended department-meeting protocol (pre-defense, §5) — two parallel editions |

The supervisor's and foreign consultant's reviews are the reviewers' own documents and are
re-exported only when revised.

The ophthalmologists' expert reviews no longer live here. They are generated, source and all,
from `defense/docs/reviews/expert/` — the signatories' data sit in `ophthalmologists.toml` and
`build_expert_reviews.py` assembles them with the shared template and the two variants of the
clinician's own text.

The protocol is **not** part of `build_all.py` — render it with `md2gost.py` directly.

Volume figures stated in the abstracts come from `council/METADATA.toml`, which is the
registry of record — do not hand-edit them here.
