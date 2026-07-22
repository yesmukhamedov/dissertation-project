---
name: demo-stack
description: "How to launch the demo stack (FastAPI backend + React frontend) locally AND publicly via Cloudflare tunnels with the real model"
metadata:
  type: project
---

Human-facing runbook: `demo/RUNBOOK.md`. This is the Claude-facing fact.

**One-shot launcher (since 2026-07-19) — DEFAULT way to run the demo locally.** When the candidate asks to start/launch the demo locally, run `demo/start-demo.ps1` (or point them at `demo/start-demo.bat` for double-click) instead of composing the manual WSL/npm commands below; keep the manual commands for debugging a single component or for the tunnel recipe. `demo/start-demo.ps1` (+ `start-demo.bat` wrapper) orchestrates the whole local stack: spawns backend (WSL uvicorn) and frontend (CRA) in separate windows via self-reinvocation with `-Role backend|frontend`, waits for `/api/health` and `:3000`, opens the browser. Drive-letter agnostic ($PSScriptRoot → `/mnt/<letter>/`), idempotent (skips a component whose port already listens). Verified cold-start end-to-end 2026-07-19. Keep the .ps1 ASCII-only — PS 5.1 reads BOM-less .ps1 as ANSI and em dashes break string parsing.

Demo stack = **`demo/server/`** (FastAPI inference, CUDA) + **`demo/web/`** (React CRA dashboard). NOTE the restructure: once flat `demo/`; uvicorn module is `server.app.main:app` run **from `demo/`** (not repo root). Verified end-to-end 2026-06-07 with the real model served publicly.

**Checkpoint in place — REAL Config D since 2026-07-19.** `demo/server/checkpoints/config_d_fold0.pt` (EfficientNet-B3 4-ch, ~129 MB, gitignored) + `eyepacs_norm_stats.json` are now copies of the actual **Experiment 1 Config D** run: `experiments/outputs/exp1/checkpoints/D_fold0/best_model.pt` (fold 0, epoch 3 — best of 5 folds: val F1 0.795 / AUC 0.885 / κ 0.781; run mean 0.7702 ± 0.0159) and `experiments/data/processed/eyepacs_norm_stats.json` (EyePACS n=5000, replacing the APTOS n=3662 interim). This is the **governance-faithful** Config D — full pipeline, 4-ch, `init.source=ssl` (continual MoCo-v2 ep50), so the shipped-vs-governance divergence in [[config-d-pretraining]] is **closed for the demo**. The retired Kaggle/APTOS stand-in sits beside it as `*.APTOS_TEST.*.bak` (duplicate of `experiments/outputs/kaggle_config_d_v2/`, safe to delete). `/api/health` provenance default is now `exp1-D-fold0-eyepacs` (`MODEL_CHECKPOINT_ID`). Verified end-to-end on this box: `checkpoint_loaded=true`, `device=cuda`, strict `load_state_dict`, and 16/20 exact-match on real EyePACS images through the live demo preprocessing path (errors only on adjacent grades 1–2) — confirming the demo's live Stages 0–4 match the cache the training used. See [[preprocessing-od-fovea-polar]], [[exp1-run-mechanics-512-cache]].

**Backend** (WSL2 Ubuntu, conda `dr-classifier`; conda NOT on PATH — use absolute binary). Default WSL distro is docker-desktop (no bash) — must pass `-d Ubuntu`:
```
wsl -d Ubuntu bash -lc "cd /mnt/e/dissertation-project/demo && \
  ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier \
  uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
```
`/api/health` → `checkpoint_loaded:true, device:cuda`; `/api/selftest` → predict/gradcam/visualize all pass. CORS allowlist from env `CORS_ORIGINS` (default `http://localhost:3000`), config in `server/app/config.py`.

**Frontend** (Windows, Node, CRA): `demo/web/.env.development` sets `REACT_APP_API_URL=http://localhost:8000`. Launch from `demo/web`: `set BROWSER=none && npm start` → `http://localhost:3000`. CRA reads `REACT_APP_*` at startup — override via env instead of editing the file.

## Public demo with REAL model (Cloudflare quick tunnels)

`demo/web/start-tunnel.bat` only tunnels the frontend AND respawns npm + ends on a blocking `pause` — DON'T run as-is in a non-interactive shell. The dashboard badge shows **"simulator (backend offline)"** for remote users because the HTTPS tunnel page can't call `http://localhost:8000` (browser **mixed-content** block). cloudflared is at `C:\Program Files (x86)\cloudflared\cloudflared.exe` (on PATH). Full recipe:

1. `cloudflared tunnel --url http://localhost:3000` → FRONTEND url (e.g. `https://<a>.trycloudflare.com`)
2. `cloudflared tunnel --url http://localhost:8000` → BACKEND url (e.g. `https://<b>.trycloudflare.com`)
3. (Re)launch **backend** with `export CORS_ORIGINS='http://localhost:3000,https://<a>.trycloudflare.com'`
4. (Re)launch **frontend** with `set REACT_APP_API_URL=https://<b>.trycloudflare.com`
5. Verify: `curl -X OPTIONS <backend>/api/predict -H "Origin: <frontend>" ...` → 200 + `Access-Control-Allow-Origin` echoes the frontend url; predict returns real grade.

Quick-tunnel URLs are random per launch, so set the frontend's API target *after* the backend tunnel exists → restart frontend whenever backend tunnel changes. Free ports before relaunch: WSL `pkill -f 'uvicorn server.app.main'`; Windows kill the PID on :3000. All servers + tunnels are session-bound background processes — they die when the session/WSL ends; relaunch with the commands above.
