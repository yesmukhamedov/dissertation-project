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
| `expert_review_ophthalmologist_{1,2}_ru.md` | Expert reviews by practising ophthalmologists on the demonstration of the application (genre `council/en/16-review`) |

The supervisor's and foreign consultant's reviews are the reviewers' own documents and are
re-exported only when revised. The same holds for the ophthalmologists' expert reviews: they are
drafts handed to the signatory, who edits them to their own voice and signs on the letterhead of
their medical organisation. Their `<...>` fields (name, position, organisation, date, length of
service) are filled by the signatory, not from the registry.

The protocol and the expert reviews are **not** part of `build_all.py` — render them one by one
with `md2gost.py`.

Volume figures stated in the abstracts come from `council/METADATA.toml`, which is the
registry of record — do not hand-edit them here.
