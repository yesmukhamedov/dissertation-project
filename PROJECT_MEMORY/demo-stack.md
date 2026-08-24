---
name: demo-stack
description: "How to launch the demo stack (FastAPI backend + React frontend) locally AND publicly via Cloudflare tunnels with the real model; plus how its numbers and figures are kept in sync with results/"
metadata:
  type: project
---

Human-facing runbook: `demo/RUNBOOK.md`. Launch protocol for sessions: `demo/CLAUDE.md`
(loaded automatically when working in `demo/`). This file is the full Claude-facing detail.

## SETTLED — act, do not ask

| Candidate says | Run |
|---|---|
| **«запусти демо» / «запускаем demo» — no qualifier** | `demo\start-pages-demo.ps1` — **public is the DEFAULT** (corrected 2026-08-14: the candidate expects the Cloudflare tunnel and the agreed fixed https://dr-classification.pages.dev straight away; do not launch local and do not ask which one) |
| «запускаем demo локально» — **local said explicitly** | `demo\start-demo.ps1` |
| «запускаем demo публично» | `demo\start-pages-demo.ps1` (background; takes minutes) |
| «останови demo» | `demo\start-pages-demo.ps1 -Stop` |

**A bare «запусти демо» is already the full request: frontend + backend + Cloudflare tunnel, public
(restated by the candidate 2026-08-16).** The three components are not separable options to be
offered — one command delivers all of them. If the candidate spells them out
(«фронт+бэк+клаудфлеер тоннель»), that is the same default, not a new variant: run
`start-pages-demo.ps1` at once. The gap that made this worth restating is that `demo/CLAUDE.md` and
this file load only when work touches `demo/`, so the default now also sits in the **root
`CLAUDE.md`** Quick Commands block, which is always in context.

Decided and **not to be reopened** unless the candidate raises it: public hosting is
**Cloudflare Pages + quick tunnel at $0** (chosen 2026-08-03 over paying ~$50 to restore the
lapsed zone or ~$5-12/yr for a new domain); permanent URL **https://dr-classification.pages.dev**;
password gate always ON, value read from gitignored `demo/.demo-password` — and since 2026-08-14
that value must stay a **4-digit numeric PIN**: the gate screen (`web/src/tabs/Demo.js`,
`PasswordGate` + `PIN_LENGTH`) renders four large underscore cells that fill with digits and
auto-submits on the fourth, so a longer or non-numeric secret becomes unenterable; backend mode `auto`
= native Windows venv (no WSL on this box); wrangler already logged in, `-AccountId` unneeded.
Every public launch rebuilds the frontend on purpose — the tunnel URL is baked into the bundle.

**One-shot launcher (since 2026-07-19) — DEFAULT way to run the demo locally.** When the candidate asks to start/launch the demo locally, run `demo/start-demo.ps1` (or point them at `demo/start-demo.bat` for double-click) instead of composing the manual WSL/npm commands below; keep the manual commands for debugging a single component or for the tunnel recipe. `demo/start-demo.ps1` (+ `start-demo.bat` wrapper) orchestrates the whole local stack: spawns backend and frontend (CRA) in separate windows via self-reinvocation with `-Role backend|frontend`, waits for `/api/health` and `:3000`, opens the browser. Drive-letter agnostic ($PSScriptRoot → `/mnt/<letter>/`), idempotent (skips a component whose port already listens). Verified cold-start end-to-end 2026-07-19. Keep the .ps1 ASCII-only — PS 5.1 reads BOM-less .ps1 as ANSI and em dashes break string parsing.

**Backend runs native-Windows OR WSL — `-Backend auto|native|wsl` (added 2026-08-03).** `auto` (default) picks **native** when `demo/.venv/Scripts/python.exe` exists, else falls back to the WSL/conda path. Native mode runs `.venv\Scripts\python.exe -m uvicorn server.app.main:app` with cwd=`demo/`; no WSL, no conda. **WSL is NOT a hard requirement for the demo** — `demo/server/` is pure FastAPI + torch + cv2 + timm with no Linux-specific code, and `server/app/__init__.py` resolves `import src.*` to `experiments/` by relative path, so it runs natively on Windows. Prefer native when setting up a new box: minutes and ~6 GB vs a WSL2+Ubuntu+conda rebuild.

**Native venv recipe (Python 3.13 / Windows).** `python -m venv demo/.venv`, then torch from the CUDA index (`pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126` → torch 2.13.0+cu126, cp313 wheels exist), then `pip install -r server/requirements.txt`. **`server/requirements.txt` is INCOMPLETE — it additionally needs `pandas` + `scikit-learn`** (NOT matplotlib; verified 2026-08-03 by uninstalling it — app imports fine). Neither is genuinely used by the demo: they arrive as a **package-init side effect**. `pipeline.py.__init__` (line ~189) lazily imports the single class `UnifiedFundusAugmentation`, but Python first executes `src/data/__init__.py`, which eagerly imports `datasets.py` (→ pandas) and `splits.py` (→ sklearn). Without them the app dies at import with `ModuleNotFoundError: pandas`. **This also breaks `demo/server/Dockerfile`**, which pip-installs only `requirements.txt`. Cleaner fix than padding requirements: `pipeline.py` builds `self._augmentation` unconditionally at line 190 but uses it only under `if self.is_training:` (line 390) — guarding the import/construction with `is_training` would make inference skip `src.data` entirely. Not applied (touches the canonical training pipeline; `experiments/` is ChatGPT-implemented per CLAUDE.md). `demo/.venv` is gitignored (root `.gitignore`, added 2026-08-03).

**This D: box lost its toolchain (observed 2026-08-03).** The RTX 3060 machine that used to host WSL2+conda now has **no WSL** (`wsl --status` → exit 50, no distro packages), **no conda**, and **no Node** — only stale `demo/web/node_modules` on disk and a fresh native Python 3.13. Looks re-imaged. Recovered with: winget `OpenJS.NodeJS.LTS` (Node 24.18.1 / npm 11.16.0) + the native venv above. Verified: `checkpoint_loaded=true, device=cuda, checkpoint=exp1-D-fold0-eyepacs`, `/api/selftest` predict+gradcam+visualize all pass, CORS preflight from `:3000` → 200. See [[ssl-wsl-launch-durability]], which describes this box's older WSL state.

**A moved Python install silently kills `demo/.venv` — fix `pyvenv.cfg`, do NOT rebuild (2026-08-16).** The public launch failed with the backend window dying instantly and `/api/health` timing out at 240 s, so the dashboard deployed in simulator mode; the launcher reports only "Backend did not come up". Cause: `demo/.venv/pyvenv.cfg` still pointed at `home = C:\Python313`, but Python **3.13.14 now lives at `C:\Users\PC\AppData\Local\Programs\Python\Python313`** (per-user reinstall). The venv's `python.exe` is a shim that resolves its base interpreter through that file, so every call died with `did not find executable at 'C:\Python313\python.exe'` (exit 103) — an error visible only by invoking `.venv\Scripts\python.exe` directly. Because the **version is unchanged (3.13.14)**, the site-packages stay valid: rewrite the three paths in `pyvenv.cfg` (`home`, `executable`, `command`) and the venv works as-is — no reinstall of torch or anything else. Verified after the fix: `torch 2.13.0+cu126`, `cuda True`, `checkpoint_loaded=True`, all launcher checks green. Locate the current interpreter with `py -0p`. Only rebuild the venv if the Python **minor** version changed.

**Regenerating the result figures needs matplotlib — installed into `demo/.venv` on 2026-08-04.** `generate_charts_*.py` need numpy + scipy + cv2 + Pillow (all already in the venv for the backend) plus **matplotlib**, which was the only missing piece; `pip install matplotlib` added that package and nothing else (every dependency was already satisfied), so the inference backend is untouched. There is no other Python on this box — `python` on PATH resolves to `demo/.venv`. Charts **25/26/27 cannot be regenerated**: they render a real fundus through the pipeline and `public/fundus-examples/dr04/right_eye.jpeg` is absent; the scripts skip them by design and leave the existing PNGs, which carry no run metric.

**`demo/web/build/` is gitignored and goes stale silently.** It is NOT rebuilt by `npm start` (CRA dev-serves from `src/`), so a checked-out tree can carry a months-old bundle. On 2026-08-03 the build predated commit `2a8938c` ("rebuild demo on VALUES.md figures") by 21 source files — serving it would have shown superseded figures. The local demo is unaffected (dev server compiles current `src/`), but **rebuild before serving `build/` or tunnelling**. Note `npm run build` uses `.env.production`, where `REACT_APP_API_URL` is EMPTY → simulator-only; the real-model tunnel recipe below must set it explicitly.

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

**One-shot public launcher (since 2026-08-03) — DEFAULT way to expose the demo.** `demo/start-tunnel.ps1` (+ `start-tunnel.bat`) is the tunnel twin of `start-demo.ps1`: same `-Role` self-reinvocation and `-Backend auto|native|wsl`, plus `-Password` (→ `DEMO_PASSWORD`), `-Http2` (venue blocks QUIC/UDP 7844), `-Stop` (kill cloudflared + :3000/:8000). It creates BOTH quick tunnels first (URL scraped from `--logfile` in `$env:TEMP`), then starts the servers already carrying `CORS_ORIGINS` / `REACT_APP_API_URL`, then verifies: local health, both tunnel URLs, and the CORS preflight (`Access-Control-Allow-Origin` must echo the frontend tunnel) — it only opens the browser when all pass. It **restarts** anything already on :3000/:8000, since the random URLs must be in the environment at process start. Frontend runs the CRA **dev** server with `WDS_SOCKET_PORT=0` + `DANGEROUSLY_DISABLE_HOST_CHECK=true`, so tunnelling serves current `src/` and the stale-`build/` hazard above does not apply. Verified end-to-end 2026-08-03 through the public URL: `checkpoint_loaded=true device=cuda`, `/api/selftest` predict+gradcam+visualize all pass, wrong password → 401, `requires_password:true`.

**cloudflared was NOT installed on this box** (re-image, see above) — restored with `winget install --id Cloudflare.cloudflared -e` → 2026.7.3 at `C:\Program Files (x86)\cloudflared\cloudflared.exe`. `Find-Cloudflared` in the script checks PATH then that path.

**Stale-PATH gotcha (cost a failed run).** A shell started before node/cloudflared were installed keeps the old PATH **and hands it to every window it spawns** — the frontend window died with `npm` not found while `C:\Program Files\nodejs\` was in the machine PATH all along. Both launchers now rebuild `$env:Path` from the registry (`Sync-PathFromRegistry`, Machine+User) and resolve `npm.cmd` explicitly via `Find-Npm`.

## Permanent free URL — Cloudflare Pages + quick tunnel (CHOSEN PATH)

**Decision 2026-08-03: strictly $0, no domain.** After the zone lapsed (below) Cloudflare quoted ~$50 to restore; the candidate rejected paying and chose the free split-hosting route, so `demo/start-pages-demo.ps1` is the path to a permanent public link. Dashboard = static build on **Cloudflare Pages** at `https://<project>.pages.dev` (default project `dr-classification`), backend = quick tunnel to the local GPU box. Because the tunnel URL is random per launch, the frontend is **rebuilt with `REACT_APP_API_URL=<tunnel>` and redeployed every session** (`wrangler pages deploy`); in exchange `CORS_ORIGINS` becomes the CONSTANT pages.dev origin, so the backend no longer restarts per tunnel. Needs a one-time interactive `npx wrangler login` (browser OAuth; token lands in `%APPDATA%\xdg.config\.wrangler\config\default.toml`). Logged in 2026-08-03 as **yesmukhamedov.yeskendyr@outlook.com**, which sees exactly **one** account — `41edab150aea08647c6379508249ffb8` — so `-AccountId` is optional on this box. The older account `f729bcbe9f1803411472825d9cdd76b5` (which owned the dead zone) sits behind a **different login** and is not reachable from this token; pass `-AccountId` only if a login ever exposes several. wrangler is run via `npx --yes wrangler` (4.118.0, no repo dependency added); `WRANGLER_SEND_METRICS=false` + `CI=1` keep it from prompting — but `CI=1` is scoped to wrangler ONLY, since CRA turns build warnings into errors under `CI`.

**Correcting a plausible-sounding wrong plan:** `*.pages.dev` cannot host the demo on its own and cannot be a tunnel target. Pages serves static files only (the FastAPI+CUDA backend can't live there), and Cloudflare docs are explicit that "the `cfargotunnel.com` subdomain only proxies traffic for DNS records in the same Cloudflare account" — a named tunnel needs a zone **you own** in **your** account, which `pages.dev` never is. The Cloudflare free plan covers DNS/SSL/CDN for a domain you already have; it never included the domain name itself.

**LIVE since 2026-08-03: https://dr-classification.pages.dev** (project `dr-classification`, production branch `main`). First deploy uploaded **897 files in 99 s** after pruning. Verified independently of the launcher: index 200; the tunnel URL is baked into `static/js/main.<hash>.js`; all **30 result PNGs + 4 result JSONs** served with real content types; both referenced SVGs (`/diagrams/02_system_architecture.svg`, `04_preprocessing_pipeline_vertical.svg`); a 9.1 MB `pipeline/` PNG and a `datasets/` JPEG; `/api/selftest` through the session tunnel → predict+gradcam+visualize all pass; CORS preflight 200 echoing the pages.dev origin.

**Gotcha — HTTP 200 does NOT prove an asset exists on Pages.** Any unknown path returns the SPA fallback: `200`, `text/html`, **674 bytes** (index.html). A status-only check therefore reports every missing figure as present. Always assert `Content-Type` (or size) — that is how the pruned `images/` tree was confirmed gone and how three of my own invented filenames were caught.

**Build is 1.1 GB and mostly dead weight.** CRA copies all of `public/` into `build/`. Verified 2026-08-03 that `images/` (352 MB — a stale duplicate of `pipeline/`, and `images/results/` additionally duplicates all 30 result PNGs **and the 4 result JSONs**, i.e. it carries its own copy of the numbers; kept mirrored on 2026-08-04 rather than deleted, since deletion is the candidate's call), `fundus-examples/` (15 MB), `camera/` and `webApp/` are referenced **nowhere** in `src/` or `public/*.md` (the one "images/" hit in `RESULTS.md` is the unit "images/s"); the script prunes them before upload → ~730 MB / 1412 files, inside the Pages free limits (20,000 files, 25 MiB per file, no documented total). Still USED: `pipeline/` (338 MB, `ModelMethods.js`/`ModelPipeline.js`), `datasets/` (314 MB, `_eyepacsPairs.js` random-patient samples), `results/`, `diagrams/`, `static/`. First deploy uploads everything; later ones only the rebuilt JS bundle. Next lever if that is too slow: `pipeline/` and `datasets/` are full-resolution PNGs (up to 8.7 MB each) displayed a few hundred pixels wide — recompressing them is the obvious 10× win, not yet done.

## Permanent hostname (Cloudflare named tunnel)

`demo/start-named-tunnel.ps1` (2026-08-03) serves the demo on a stable name instead of a random quick-tunnel URL. **Single hostname, path-routed** — every backend route is under `/api/` (`server/app/main.py`) and every frontend call is `${API}/api/...` (`web/src/tabs/_apiPredict.js`), so one ingress splits them: `path: ^/api/` → :8000, else → :3000. Same-origin ⇒ **no CORS and no mixed-content problem at all**, one URL to hand out; `REACT_APP_API_URL` is set to the public origin itself (it must be non-empty — `_apiPredict.js` throws on empty, it does NOT fall back to relative). Modes: `-Setup` (create tunnel + write `~/.cloudflared/config.yml` + `tunnel route dns`), run, `-InstallService` (connector only — backend/frontend are NOT services, so a reboot needs the script again), `-Stop`. **Kept but NOT the active path** — it needs a domain, and the $0 Pages route above was chosen instead; revive it if a zone is ever acquired. Requires a one-time interactive `cloudflared tunnel login` (browser) and an **ACTIVE zone on FULL DNS setup** — a partial/CNAME zone cannot hold the `CNAME → <uuid>.cfargotunnel.com`. Universal SSL `*.<zone>` covers a single-label subdomain, so no cert work. **UNTESTED end-to-end** — see the blocker below.

**BLOCKER: the candidate's zone `yeskendyr.men` lapsed.** Registered 2025-05-29 via Cloudflare Registrar, **expired 2026-05-29**; on 2026-08-03 registry RDAP (`https://rdap.nic.men/domain/yeskendyr.men`) reports status `redemption period` + `pending delete`, and the name is NXDOMAIN on public resolvers (so the "validate to renew SSL" mail of 2026-08-01 was moot — the registration, not the certificate, is what died). Cloudflare's schedule is 40-day grace / days 41–70 redemption / days 71–75 pendingDelete, i.e. ~day 66 of 75 on 2026-08-03: restore is a **paid, irreversible, dashboard-only** action (Registrar restores only while EPP status is `redemptionPeriod`) and the window is days. Intended name once a zone exists: **`dr-classification.<zone>`**.

`demo/web/start-tunnel.bat` and `demo/web/_launch_with_tunnel.bat` are now **superseded stubs** forwarding to `demo/start-tunnel.ps1`; the old bodies tunnelled only the frontend, hardcoded `/mnt/e/`, were WSL-only and ended on a blocking `pause`. The dashboard badge shows **"simulator (backend offline)"** for remote users when only the frontend is tunnelled, because the HTTPS tunnel page can't call `http://localhost:8000` (browser **mixed-content** block). Manual recipe (for debugging one leg):

1. `cloudflared tunnel --url http://localhost:3000` → FRONTEND url (e.g. `https://<a>.trycloudflare.com`)
2. `cloudflared tunnel --url http://localhost:8000` → BACKEND url (e.g. `https://<b>.trycloudflare.com`)
3. (Re)launch **backend** with `export CORS_ORIGINS='http://localhost:3000,https://<a>.trycloudflare.com'`
4. (Re)launch **frontend** with `set REACT_APP_API_URL=https://<b>.trycloudflare.com`
5. Verify: `curl -X OPTIONS <backend>/api/predict -H "Origin: <frontend>" ...` → 200 + `Access-Control-Allow-Origin` echoes the frontend url; predict returns real grade.

Quick-tunnel URLs are random per launch, so set the frontend's API target *after* the backend tunnel exists → restart frontend whenever backend tunnel changes. Free ports before relaunch: WSL `pkill -f 'uvicorn server.app.main'`; Windows kill the PID on :3000. All servers + tunnels are session-bound background processes — they die when the session/WSL ends; relaunch with the commands above.

## Launch on the D: box — 2026-08-24 session, two blockers and their fixes

**Wrangler can be logged into the WRONG Cloudflare account, and the error hides it.** On
2026-08-24 `start-pages-demo.ps1` died at `pages project list` with
`A request to the Cloudflare API (/accounts/41edab150aea08647c6379508249ffb8/pages/projects)
failed … Authentication error [code: 10000]`. The account id in the URL is the RIGHT one — it
comes from the stale cache `node_modules/.cache/wrangler/wrangler-account.json` at the repo
root — but the OAuth token had been replaced by a login as **yesmukhamedov009@gmail.com**
(account `64cdd2ef6220914b339381bfe76440d2`), which cannot see the outlook account that owns
the Pages project. `wrangler whoami` is the diagnostic: it prints the email + the single
account the token can reach. Fix = `npx wrangler logout` then `npx wrangler login`, choosing
**yesmukhamedov.yeskendyr@outlook.com** in the browser. Do NOT "fix" it by clearing the cache
or deploying under the gmail account — that yields a different URL and orphans the permanent
link on the slide. The script's own error message ("not logged in") never fires here, since
`whoami` succeeds; only the Pages call fails.

**`demo/.venv` was broken again by a Python move — new path is `C:\Python313`.** `pyvenv.cfg`
pointed at `C:\Users\PC\AppData\Local\Programs\Python\Python313` (old Windows user `PC`);
`python.exe` in the venv then dies with `did not find executable at …`. Same minor version
(3.13), so the settled fix applies: rewrite `home`/`executable`/`command` in
`demo\.venv\pyvenv.cfg` to `C:\Python313`, do not rebuild the venv. Confirmed working after
the edit (torch 2.13.0+cu126, fastapi, uvicorn all import).

**This box has no NVIDIA GPU.** `nvidia-smi` is absent and `torch.cuda.device_count() == 0`,
so `/api/health` reports `"device":"cpu"` — expected here, not a regression; inference is just
slower. The "local GPU box" wording above describes the work PC, not this one.

**A failed health check does NOT roll the launch back.** The launcher reported
`Waiting for backend tunnel … TIMEOUT` yet exit code 0: Pages had deployed and cloudflared was
alive (tunnel answered **502** = connector up, origin dead — a useful distinction from a
connection error, which means the tunnel itself is gone). Only the backend was missing, so the
cure is to start the backend role alone and keep the session's tunnel URL, instead of rerunning
the whole script and paying for another rebuild+deploy:
`start-pages-demo.ps1 -Role backend -Backend native -CorsOrigins "http://localhost:3000,https://dr-classification.pages.dev"`
(the password is picked up from `demo\.demo-password` by the same script). Backend takes ~30 s
to answer `/api/health` while the checkpoint loads.
