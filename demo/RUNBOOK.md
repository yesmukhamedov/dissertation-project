# Demo — launch runbook

> How to run the defense demo (FastAPI backend + React frontend), locally and publicly.
> Machine-readable source of truth for Claude: `PROJECT_MEMORY/demo-stack.md`.

Stack = **`demo/server/`** (FastAPI inference, CUDA) + **`demo/web/`** (React CRA dashboard).
The uvicorn module is `server.app.main:app`, run **from `demo/`** (not repo root).

**Checkpoint:** `demo/server/checkpoints/config_d_fold0.pt` (EfficientNet-B3 4-ch, ~129 MB,
gitignored) + `eyepacs_norm_stats.json`. Both are the real **Experiment 1 Config D** artifacts,
copied from `experiments/outputs/exp1/checkpoints/D_fold0/best_model.pt` and
`experiments/data/processed/eyepacs_norm_stats.json` (EyePACS, n=5000). Fold 0 is the best of
the five folds: val weighted-F1 0.795, ROC-AUC 0.885, κ 0.781 (run mean 0.7702 ± 0.0159).
The earlier Kaggle/APTOS interim stand-in is kept alongside as `*.APTOS_TEST.*.bak` and can
be deleted — an identical copy lives in `experiments/outputs/kaggle_config_d_v2/`.

To re-point at a different fold, either overwrite `config_d_fold0.pt` or set
`CHECKPOINT_PATH` (and `MODEL_CHECKPOINT_ID` for the `/api/health` provenance string).

## Local

**One-shot:** `demo/start-demo.ps1` (or double-click `start-demo.bat`) launches both:
backend + frontend in their own windows, waits for health checks, opens the browser.
Drive-letter agnostic; skips a component if its port (8000/3000) is already listening.

The backend runs one of two ways, selected by `-Backend auto|native|wsl`. **`auto` (default)
uses native Windows when `demo/.venv` exists, else WSL.** WSL is not required — `server/` is
pure FastAPI + torch + cv2 + timm with no Linux-specific code. Manual commands below.

**Backend A — native Windows** (no WSL, no conda). One-time setup:
```
python -m venv .venv
.venv\Scripts\python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
.venv\Scripts\python -m pip install -r server\requirements.txt pandas scikit-learn
```
`pandas` and `scikit-learn` are NOT in `server/requirements.txt`, but importing the app
pulls them in via `src/data/__init__.py` — without them it fails with `ModuleNotFoundError`.
Run (from `demo/`): `.venv\Scripts\python -m uvicorn server.app.main:app --host 127.0.0.1 --port 8000`

**Backend B — WSL2 Ubuntu**, conda `dr-classifier` (conda not on PATH; default WSL distro is
docker-desktop, so pass `-d Ubuntu`). The traveling drive mounts under a different letter per
machine — adjust `/mnt/<letter>/` to wherever the project sits:
```
wsl -d Ubuntu bash -lc "cd /mnt/d/dissertation-project/demo && \
  ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier \
  uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
```
Check either way: `/api/health` → `checkpoint_loaded:true, device:cuda`; `/api/selftest` → all
pass. CORS allowlist from env `CORS_ORIGINS` (default `http://localhost:3000`).

**Frontend** (Windows, Node, CRA), from `demo/web`:
```
set BROWSER=none && npm start      # → http://localhost:3000
```
`demo/web/.env.development` sets `REACT_APP_API_URL=http://localhost:8000`. CRA reads
`REACT_APP_*` at startup — override via env, don't edit the file mid-session.
Needs Node; if absent: `winget install --id OpenJS.NodeJS.LTS -e`.

> **`demo/web/build/` is gitignored and can be badly out of date.** `npm start` dev-serves
> from `src/`, so the local demo is always current — but `build/` is only refreshed by an
> explicit `npm run build`. Rebuild before serving `build/` statically or tunnelling it,
> or you may present superseded figures. Also note `npm run build` reads `.env.production`,
> where `REACT_APP_API_URL` is empty → simulator-only unless you set it.

## Public (real model) — Cloudflare quick tunnels

The dashboard shows "simulator (backend offline)" for remote users unless the backend is
ALSO tunnelled (browser mixed-content blocks calling `http://localhost:8000` from an HTTPS
page). cloudflared: `C:\Program Files (x86)\cloudflared\cloudflared.exe`.

1. `cloudflared tunnel --url http://localhost:3000` → FRONTEND url `https://<a>.trycloudflare.com`
2. `cloudflared tunnel --url http://localhost:8000` → BACKEND url `https://<b>.trycloudflare.com`
3. Relaunch **backend** with `export CORS_ORIGINS='http://localhost:3000,https://<a>.trycloudflare.com'`
4. Relaunch **frontend** with `set REACT_APP_API_URL=https://<b>.trycloudflare.com`
5. Verify CORS: `curl -X OPTIONS <backend>/api/predict -H "Origin: <frontend>"` → 200.

URLs are random per launch → set the frontend API target AFTER the backend tunnel exists;
restart the frontend whenever the backend tunnel changes. `demo/web/start-tunnel.bat` only
tunnels the frontend and ends on a blocking `pause` — don't use it in a non-interactive shell.
Free ports: WSL `pkill -f 'uvicorn server.app.main'`; Windows kill the PID on :3000.
All servers/tunnels are session-bound — they die with the session/WSL; relaunch as above.
