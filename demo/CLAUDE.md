# demo/ — defense demo bundle

FastAPI inference backend (`server/`, CUDA) + React CRA dashboard (`web/`).
Human-facing runbook: `RUNBOOK.md`. Claude-facing detail: `PROJECT_MEMORY/demo-stack.md`.

## Launch protocol — ACT, DO NOT ASK

These decisions are settled. When the candidate says "запускаем demo" (or "launch the
demo"), run the matching command **immediately** — no clarifying questions, no proposing
alternatives, no re-deriving the architecture.

| The candidate says | Run |
|---|---|
| «запускаем demo **локально**» / "run the demo locally" | `powershell -ExecutionPolicy Bypass -File D:\dissertation-project\demo\start-demo.ps1` |
| «запускаем demo **публично**» / "publish the demo" / "share the demo" | `powershell -ExecutionPolicy Bypass -File D:\dissertation-project\demo\start-pages-demo.ps1` |
| «останови demo» / "stop the demo" | `.\start-pages-demo.ps1 -Stop` (public) or close the two windows (local) |

Public launches take several minutes (model load + CRA build + Pages deploy) — run them with
`run_in_background: true` and report the result when the notification arrives.

**Settled parameters — do not ask about these:**

- **Password.** Always on. Read automatically from `demo/.demo-password` (gitignored); pass
  `-Password` only if the candidate names a different one in the same breath.
- **Public hosting = Cloudflare Pages + quick tunnel, $0.** Decided 2026-08-03 after the zone
  `yeskendyr.men` lapsed and Cloudflare quoted ~$50 to restore. Do not re-propose buying a
  domain, restoring that one, or a named tunnel unless the candidate raises it.
- **Permanent URL: https://dr-classification.pages.dev.** Stable across launches; the backend
  tunnel URL is random per launch and is rebuilt into the bundle every time. This is why a
  public launch always rebuilds — never skip the build to save time.
- **Backend mode `auto`.** Native Windows venv (`demo/.venv`) on this box; WSL is not
  installed here. Do not offer to set up WSL.
- **Account.** `npx wrangler login` is already done (one account,
  `41edab150aea08647c6379508249ffb8`); `-AccountId` is unnecessary. If the token ever expires,
  the candidate must rerun the login interactively — in Git Bash Node is not on PATH, so the
  command is `export PATH="/c/Program Files/nodejs:$PATH" && npx wrangler login`.

## Verifying a public launch

The launcher already checks health, both URLs and the CORS preflight, and only opens the
browser when all pass. If verifying assets by hand: **Cloudflare Pages returns `200 text/html`
(674 bytes, index.html) for ANY unknown path** — a status-only check reports missing files as
present. Assert `Content-Type`.

## Landmines (all already handled in the scripts — do not "fix" them again)

- **Stale PATH.** A shell started before Node/cloudflared were installed hands its old PATH to
  every window it spawns, so `npm` vanishes in the child. The launchers rebuild `$env:Path`
  from the registry and resolve `npm.cmd` explicitly.
- **`CI=1` is scoped to wrangler only.** CRA turns build warnings into errors under `CI`.
- **`web/build/` is gitignored and goes stale silently** — `npm start` never refreshes it.
  Only the public launcher rebuilds it. Never deploy or tunnel a build you did not just make.
- **`server/requirements.txt` is incomplete** — it also needs `pandas` + `scikit-learn`
  (package-init side effect of `src/data/__init__.py`), which also breaks `server/Dockerfile`.
- **PS 5.1 reads BOM-less `.ps1` as ANSI** — keep the launchers ASCII-only.

## Scripts

| File | Purpose |
|---|---|
| `start-demo.ps1` / `.bat` | local only (backend :8000 + CRA :3000) |
| `start-pages-demo.ps1` | **public, active path** — Pages + quick tunnel |
| `start-tunnel.ps1` / `.bat` | public via two quick tunnels; both URLs random. Superseded by the Pages route, kept for a quick one-off share |
| `start-named-tunnel.ps1` | public on a permanent hostname; **needs a domain**, currently unusable, untested |
| `web/*tunnel*.bat` | superseded stubs forwarding to `start-tunnel.ps1` |
