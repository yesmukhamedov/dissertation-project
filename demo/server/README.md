# server/ — DR-Classifier inference backend

FastAPI + PyTorch backend that serves **real** Config D (Full pipeline +
EfficientNet-B3) predictions to the React demo. It imports preprocessing and
model code directly from `../../experiments/src` (the repo-root `experiments/`
tree) — no duplication, so inference runs the *same* pipeline that was defended
in the thesis.

> This backend lives at `demo/server/` (bundled alongside the `demo/web/`
> dashboard). It is two levels below the repo root, so `app/__init__.py`
> resolves `experiments/` via `parents[3]` and the commands below run from
> `demo/`.

## Layout

```
server/
├── app/
│   ├── __init__.py        puts experiments/ on sys.path
│   ├── config.py          env-driven settings (paths, device, CORS)
│   ├── schemas.py         Pydantic request/response models
│   ├── preprocessing.py   builds the inference pipeline (+ dataset stats)
│   ├── inference.py       model load + predict (per-eye, worst-eye patient)
│   ├── gradcam.py         scaffold stub (→ 501) — see TASK-Demo §C.5
│   ├── cases.py           per-patient case store (originals, stages, verdicts)
│   ├── corrections.py     OD/fovea clinician-correction store (Phase 3/4)
│   └── main.py            FastAPI app + endpoints
├── checkpoints/           drop config_d_fold0.pt + eyepacs_norm_stats.json here
├── data/                  runtime state — case folders + corrections (gitignored)
├── tests/test_inference.py
├── requirements.txt
└── Dockerfile             HuggingFace Spaces (port 7860)
```

## Endpoints

| Method | Path | Body | Returns |
|---|---|---|---|
| GET  | `/api/health`   | — | `{status, model, checkpoint, checkpoint_loaded, device, version, git_sha, requires_password}` |
| POST | `/api/auth`     | multipart `password?` | `{ok: true}` (gate open / match) or 401 |
| POST | `/api/predict`  | multipart `left?`, `right?`, `password?`, `case_id?` | patient-level + `per_eye` |
| POST | `/api/gradcam`  | multipart `image`, `eye`, `password?`, `target_class?`, `case_id?` | `{gradcam_png_b64, attention_overlay_png_b64, target_class, rationale, cam_pixel_count, cam_area_frac, cam_region}` |
| POST | `/api/visualize`| multipart `image`, `eye`, `password?`, `case_id?` | `{fov_mask_png_b64, preview_png_b64, od_fovea}` |
| POST | `/api/od_fovea/correct` | multipart `image`, `eye`, `od_x/od_y`, `fovea_x/fovea_y`, `password?`, `case_id?` | corrected `od_fovea` + full pipeline re-run |
| POST | `/api/case/image` | multipart `image`, `eye`, `case_id?`, `is_fundus?`, `laterality?`, `source?`, `password?` | `{case_id, eye, stored, reason}` |
| POST | `/api/case/{case_id}/feedback` | multipart `verdict`, `corrected_grade`, `predicted_grade?`, `reviewer?`, `notes?`, `password?` | `{case_id, stored, index}` |
| DELETE | `/api/case/{case_id}/feedback` | query `index?`, `password?` | `{case_id, retracted, verdict, corrected_grade}` |
| GET  | `/api/cases/stats` | query `password?` | store-wide counters (patients, runs, verdicts, agreement, grades) |
| GET  | `/api/case/{case_id}` | query `password?` | the case record (`case.json`) |
| GET  | `/api/selftest` | query `password?` | per-op pass/fail report |

- **Grad-CAM** is a self-contained torch implementation on EfficientNet's
  `conv_head` (no `pytorch-grad-cam` dependency); JET overlay over the original
  image. It also emits a backend-generated **predicted-class rationale** (§D.3):
  a one-line sentence derived purely from CAM geometry (salient-pixel count +
  centroid region, no LLM), described in neutral image-space terms per NC-14.
  **/api/visualize** returns the 6-panel stage strip (via
  `pipeline.stage_breakdown`), the FOV mask, and the classical-CV OD/fovea
  payload (`od_fovea`).
- **Password gate (§C.2):** set `DEMO_PASSWORD` to require a `password` field on
  every endpoint except `/api/health`. Unset → gate **open** (local dev).
  `/api/health.requires_password` lets the frontend decide whether to show the
  access screen; `/api/auth` validates the password for that screen.
- **Patient cases (`app/cases.py`).** The demo opens a case as soon as the first
  image that passes the client-side fundus check lands in a slot, and passes its
  `case_id` back on every later call. Everything computed for that patient is
  then filed under `data/cases/<case_id>/`: the originals byte-for-byte, one PNG
  per preprocessing stage (plus the final stage's channel split — the 4-channel
  CNN input), the Grad-CAM heatmap and attention overlay, the prediction, any
  OD/fovea correction with its own pipeline re-run, and the ophthalmologist's
  confirm/reject verdict with the corrected grade. `case.json` is the record and
  `case.txt` is the same thing rendered for a human to read.
  Every write is best-effort: a failed or absent case never fails a prediction,
  and an unknown `case_id` is ignored rather than rejected. A case with two eyes
  is a few MB of PNGs — the store grows with use and is never pruned
  automatically.
  A verdict can be **withdrawn** (`DELETE …/feedback`), which drops it from the
  record entirely rather than flagging it — a retracted verdict left in place
  would keep being counted in `/api/cases/stats` and exported as a label.
  `/api/cases/stats` aggregates every case directory, which is what lets the
  demo show study-wide totals that survive a cleared browser buffer.
- **Safety limits (§C.4):** ≤ 8 MB/image, MIME ∈ {jpeg,png,webp} (else 415),
  decoded ≤ 4096×4096. Inference itself decodes in memory only; the case store
  is the one component that writes to disk (`data/`, gitignored).

## Why two files in `checkpoints/`

Config D trained with **dataset-specific** Stage 7 normalize (D-2), not ImageNet.
To avoid train/inference preprocessing drift, the server injects the *same*
EyePACS mean/std the checkpoint trained with:

- `config_d_fold0.pt`  ← `experiments/outputs/exp1/checkpoints/D_fold{N}/best_model.pt`
- `eyepacs_norm_stats.json` ← `experiments/data/processed/eyepacs_norm_stats.json`
  (produced by `scripts/compute_dataset_stats.py`)

If `eyepacs_norm_stats.json` is missing, the server still boots but logs a
warning and falls back to ImageNet — **don't** demo Config D that way.

## Local dev

```bash
cd demo          # the demo/ dir; `server` resolves as a package from here
# 1. Put the trained artifacts in place (experiments/ is at the repo root):
cp ../experiments/outputs/exp1/checkpoints/D_fold0/best_model.pt server/checkpoints/config_d_fold0.pt
cp ../experiments/data/processed/eyepacs_norm_stats.json         server/checkpoints/

# 2. Install + run (use the dr-classifier env, or a fresh venv):
pip install -r server/requirements.txt
uvicorn server.app.main:app --reload --port 8000
# → http://localhost:8000/api/health
```

Smoke test:
```bash
curl -F "left=@<some_fundus>.jpg" -F "right=@<some_fundus>.jpg" \
     http://localhost:8000/api/predict
```

## Configuration (env vars)

| Var | Default | Purpose |
|---|---|---|
| `CHECKPOINT_PATH` | `server/checkpoints/config_d_fold0.pt` | Model weights. |
| `NORM_STATS_PATH` | `server/checkpoints/eyepacs_norm_stats.json` | Stage 7 stats. |
| `MODEL_CHECKPOINT_ID` | `config-d-fold0` | Provenance shown in `/api/health`. |
| `DEVICE` | `auto` | `cuda` / `cpu` / `auto`. |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins. |
| `PORT` | `8000` (Docker: `7860`) | Bind port. |

## Tests

```bash
pytest server/tests/test_inference.py
```
They boot the app and assert response *shape/behaviour*; they pass even without
a checkpoint (random-init weights still give a valid softmax).

## Configuration (added env vars)

| Var | Default | Purpose |
|---|---|---|
| `DEMO_PASSWORD` | (unset) | Shared access password; unset = gate open. |
| `DEMO_VERSION` | `__version__` | Version string in `/api/health`. |
| `GIT_SHA` | `git rev-parse` | Provenance SHA (best-effort). |
| `CASES_DIR` | `server/data/cases` | Patient case store (originals, cached stages, attention maps, verdicts). |
| `OD_FOVEA_CORRECTIONS_DIR` | `server/data/od_fovea_corrections` | OD/fovea correction store feeding the Phase-4 fine-tune. |

## Status / next

- [x] Bootable API, real preprocessing + model wiring, worst-eye aggregation.
- [x] Dataset-specific normalize injection (no preprocessing drift).
- [x] Grad-CAM (live, self-contained) + predicted-class rationale, `/api/visualize`
      (preview strip + FOV mask + OD/fovea), `/api/selftest`, password gate + `/api/auth`,
      safety limits, health provenance (incl. `requires_password`).
- [x] Frontend wiring of the new endpoints (per-image widget, live Grad-CAM +
      rationale, provenance footer, password screen) — TASK-Demo Part D.
- [x] Bundle real checkpoint (Part A) — Experiment 1 Config D, fold 0
      (`outputs/exp1/checkpoints/D_fold0/best_model.pt`), replacing the earlier
      Kaggle/APTOS interim artifact.
