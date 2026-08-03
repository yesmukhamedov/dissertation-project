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

**One-shot:** `demo/start-tunnel.ps1` (or double-click `start-tunnel.bat`). It does the whole
recipe below: creates both quick tunnels, starts backend + frontend already wired to them,
then verifies health and the CORS preflight before opening the browser.

```
powershell -ExecutionPolicy Bypass -File start-tunnel.ps1 -Password "<secret>"
powershell -ExecutionPolicy Bypass -File start-tunnel.ps1 -Stop     # tear everything down
```

Options: `-Backend auto|native|wsl` (as in `start-demo.ps1`), `-Password` → `DEMO_PASSWORD`
(**use it — a quick tunnel is world-reachable and runs on your GPU**; the dashboard then shows
an access-password screen, and `/api/health` reports `requires_password:true`), `-Http2` if the
venue network blocks QUIC/UDP 7844 and the tunnels never answer.

It restarts anything already on :3000/:8000 — the tunnel URLs are random per launch and have
to be in the servers' environment at process start. The frontend is the CRA **dev** server
(`WDS_SOCKET_PORT=0`, `DANGEROUSLY_DISABLE_HOST_CHECK=true`), so it serves current `src/` and
the stale `build/` warning above does not apply.

Requires cloudflared (`winget install --id Cloudflare.cloudflared -e`); the script finds it on
PATH or at `C:\Program Files (x86)\cloudflared\cloudflared.exe`.

**Manual equivalent**, for debugging one leg. The dashboard shows "simulator (backend offline)"
for remote users unless the backend is ALSO tunnelled (browser mixed-content blocks calling
`http://localhost:8000` from an HTTPS page).

1. `cloudflared tunnel --url http://localhost:3000` → FRONTEND url `https://<a>.trycloudflare.com`
2. `cloudflared tunnel --url http://localhost:8000` → BACKEND url `https://<b>.trycloudflare.com`
3. Relaunch **backend** with `CORS_ORIGINS='http://localhost:3000,https://<a>.trycloudflare.com'`
4. Relaunch **frontend** with `set REACT_APP_API_URL=https://<b>.trycloudflare.com`
5. Verify CORS: `curl -X OPTIONS <backend>/api/predict -H "Origin: <frontend>"` → 200.

URLs are random per launch → set the frontend API target AFTER the backend tunnel exists;
restart the frontend whenever the backend tunnel changes. Free ports: Windows kill the PID on
:3000/:8000; WSL `pkill -f 'uvicorn server.app.main'`. All servers/tunnels are session-bound —
they die with their windows; relaunch as above. The two `demo/web/*tunnel*.bat` files are
superseded stubs that forward to `start-tunnel.ps1`.

## Permanent free URL, no domain — Cloudflare Pages + quick tunnel

`demo/start-pages-demo.ps1`. Split hosting, costs nothing. **Live at
https://dr-classification.pages.dev**:

```
https://dr-classification.pages.dev  dashboard — static build on Pages (PERMANENT)
https://<random>.trycloudflare.com   API — quick tunnel to the local GPU backend
```

The dashboard URL never changes, so it can go on a slide. The backend URL is random per
launch, so the frontend is **rebuilt with it baked into `REACT_APP_API_URL` and redeployed**
each session. The payoff: `CORS_ORIGINS` becomes a **constant** (the pages.dev origin), so the
backend no longer has to be restarted whenever the tunnel changes.

```
npx wrangler login                                     # once, opens a browser
.\start-pages-demo.ps1 -Password "<secret>" -AccountId <hex>
.\start-pages-demo.ps1 -Stop                           # stops the GPU backend; Pages stays up
```

`-AccountId` (the hex string in the dashboard URL) is only needed when the login exposes more
than one Cloudflare account — the current login does not, so it can be omitted. Other flags:
`-Project` (default `dr-classification`), `-Backend`, `-Http2`, `-SkipBuild` (redeploy the
existing `build/` — only valid if the tunnel URL has not changed).

**Size.** `npm run build` produces ~1.1 GB. The script prunes `images/`,
`fundus-examples/`, `camera/` and `webApp/` — 367 MB that nothing in `src/` or `public/*.md`
references (`images/` is a stale duplicate of `pipeline/`), leaving ~730 MB in 1412 files.
That is within the Pages free limits (20,000 files, 25 MiB per file, no documented total),
but the **first** deploy uploads all of it; later ones send only the changed JS bundle. If
that upload is too slow, the next lever is recompressing `pipeline/` and `datasets/` — they
are full-resolution PNGs (up to 8.7 MB each) shown at a few hundred pixels.

**When the backend is down** the deployed dashboard stays online and falls back to
"simulator (backend offline)" — the figures, tables and pipeline pages all still work.

## Public on a permanent hostname — Cloudflare named tunnel

`demo/start-named-tunnel.ps1` serves the demo at a stable name in your own zone, and can run
as a Windows service so it survives reboots. **One hostname, path-routed** — every backend
route lives under `/api/` and every frontend call is `${API}/api/…`, so both halves fit behind
one name, same-origin: no CORS preflight, no mixed content, one URL to hand out.

```
https://<hostname>/api/*  ->  localhost:8000   (FastAPI)
https://<hostname>/*      ->  localhost:3000   (CRA)
```

Prerequisites: cloudflared installed; an **ACTIVE** zone in the Cloudflare account on **full
DNS setup** (nameservers delegated to Cloudflare — a partial/CNAME zone cannot hold the
`CNAME → <uuid>.cfargotunnel.com` that routing needs); and a one-time interactive
`cloudflared tunnel login`. Universal SSL's `*.<zone>` wildcard already covers a
single-label subdomain, so no certificate work is needed.

```
cloudflared tunnel login                                     # once, opens a browser
.\start-named-tunnel.ps1 -Hostname dr-classification.<zone> -Setup
.\start-named-tunnel.ps1 -Hostname dr-classification.<zone> -Password "<secret>"
.\start-named-tunnel.ps1 -Stop
```

`-Setup` creates the tunnel, writes `~/.cloudflared/config.yml` (a copy lands in
`demo/cloudflared/config.yml.example` so the setup travels with the drive — the credentials
JSON does not) and routes DNS. `-InstallService` registers the **connector** as a Windows
service (elevated shell); the backend and frontend are not services, so after a reboot the
hostname answers only once you rerun the script to start them.
