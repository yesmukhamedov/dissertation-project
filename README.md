# Dissertation Project

**Automated Diabetic Retinopathy Diagnosis via Fundus Image Enhancement and CNN Classification**

PhD dissertation — Yesmukhamedov N.S., IITU, Almaty, Kazakhstan.

## Structure

| Directory | Description |
|-----------|-------------|
| `experiments/` | Python/PyTorch ML pipeline, training, the seven experiments |
| `results/` | Portable knowledge base — metrics, tables, hypothesis cards, findings. **Single source of truth for every number that reaches the thesis, the defense or the demo** |
| `thesis/` | Dissertation text, governance docs, literature cards |
| `council/` | Defense-council metadata registry (`METADATA.toml`) and document templates |
| `demo/` | Defense demo bundle: `web/` (React dashboard) + `server/` (FastAPI inference backend) |
| `defense/` | Slides, figures, and the built council deliverables in `defense/docs/` |

See `CLAUDE.md` for detailed project documentation.

## Current status

- **The dissertation is written, translated and exported.** 98 sections in each language,
  all approved. The council-ready pair is
  `defense/docs/FULL_DISSERTATION_{EN,KZ}_GOST_2026-08-14` (`.docx` + `.pdf`) —
  238 body pages EN / 265 KZ, 42 tables, 26 figures, 2 diagrams, 107 sources.
- **All seven experiments have been run and all seven hypotheses are supported.**
  Verdicts and numbers live in `results/` (`STATUS.md`, `tables/`, `hypotheses/`,
  `findings/`); the demo and the slides are rendered from the same source.
- **The integrated arm uses ImageNet→continual-SSL initialization** (MoCo-v2, ResNet-50 +
  EfficientNet-B3). From-scratch in-domain SSL did not clear the linear-probe gate. A
  supervised in-domain pretraining (SIP) path is implemented as a gate-selected alternative.
  Because the integrated arm varies pretraining *and* preprocessing together, it is a
  composite factor — Exp 2's cumulative ablation is what decomposes it.
- **Open before the defense: NEW-1 traceability.** The 2026-08-03 run's raw artifacts were
  never published into `experiments/outputs/`, which still holds an earlier run that
  disagrees. Every number in the text traces to `results/`, but not yet to a primary output
  file. See `PROJECT_MEMORY/new1-traceability-scope.md` and `results/INTEGRITY_NOTE.md`.

Durable decisions live in `PROJECT_MEMORY/` (indexed by `PROJECT_MEMORY.md`); binding
constraints in `thesis/governance/`.
