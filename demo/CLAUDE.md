# demo/ — defense demo bundle

FastAPI inference backend (`server/`, CUDA) + React CRA dashboard (`web/`).
Human-facing runbook: `RUNBOOK.md`. Claude-facing detail: `PROJECT_MEMORY/demo-stack.md`.

## Launch protocol — ACT, DO NOT ASK

These decisions are settled. When the candidate says "запускаем demo" (or "launch the
demo"), run the matching command **immediately** — no clarifying questions, no proposing
alternatives, no re-deriving the architecture.

**A bare «запусти демо» already means all three parts — frontend AND backend AND the
Cloudflare tunnel, public.** The candidate should never have to spell that out; if they do
(«фронт+бэк+тоннель»), it is the same default request, not a new variant. One command
(`start-pages-demo.ps1`) delivers all three, so never launch the parts separately or ask
which of them is wanted.

| The candidate says | Run |
|---|---|
| «запусти демо» / «запускаем demo» / "launch the demo" — **no qualifier: PUBLIC is the default** | `powershell -ExecutionPolicy Bypass -File D:\phd\dissertation\demo\start-pages-demo.ps1` (background) — the candidate expects the Cloudflare tunnel and the agreed fixed https://dr-classification.pages.dev immediately. Do not fall back to the local launcher and do not ask which one (settled 2026-08-14). |
| «запускаем demo **локально**» / "run the demo locally" — local said **explicitly** | `powershell -ExecutionPolicy Bypass -File D:\phd\dissertation\demo\start-demo.ps1` |
| «запускаем demo **публично**» / "publish the demo" / "share the demo" | `powershell -ExecutionPolicy Bypass -File D:\phd\dissertation\demo\start-pages-demo.ps1` |
| «останови demo» / "stop the demo" | `.\start-pages-demo.ps1 -Stop` (public) or close the two windows (local) |

Public launches take several minutes (model load + CRA build + Pages deploy) — run them with
`run_in_background: true` and report the result when the notification arrives.

**Settled parameters — do not ask about these:**

- **Password.** Always on. Read automatically from `demo/.demo-password` (gitignored); pass
  `-Password` only if the candidate names a different one in the same breath. It must be a
  **4-digit numeric PIN** — the gate screen is a four-cell PIN entry (`web/src/tabs/Demo.js`,
  `PIN_LENGTH`), so any other secret cannot be typed in.
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

## Patient cases — the demo's only persistent state

The demo opens a **patient case** on the backend as soon as the first image that
passes the client-side fundus check lands in a slot, and everything computed for
that patient is filed into one directory (`server/app/cases.py`, default
`server/data/cases/<case_id>/`, gitignored):

| In the case | Written by |
|---|---|
| `original/{left,right}.<ext>` — the uploads, byte-for-byte | `POST /api/case/image` |
| `preprocessing/<eye>/` — one PNG per stage + `input_channels/` (the 4-channel CNN input) | `POST /api/visualize` |
| `preprocessing/<eye>_corrected_<n>/` — the re-run driven by a clinician OD/fovea correction | `POST /api/od_fovea/correct` |
| `attention/<eye>_{gradcam,attention_overlay}.png` | `POST /api/gradcam` |
| `case.json` — the record; `case.txt` — the same, rendered for a human | every write |
| the ophthalmologist's confirm/reject verdict + corrected grade | `POST /api/case/{id}/feedback` |

The verdict is the point: the confirm/reject control used to live only in browser
memory, so a disagreement died with the tab.

**One verdict per prediction.** Once given, the confirm/reject buttons are
replaced by the standing verdict and an undo, so a result cannot be confirmed
twice or confirmed and rejected at once. Undo (`DELETE /api/case/{id}/feedback`)
**removes** the verdict rather than flagging it — one left in place would keep
being counted and exported. Both writes go through one promise chain in
`Demo.js`, so an undo clicked before the save lands retracts what that save wrote.

**Both panels come from disk, not the tab.** `GET /api/cases/stats` walks the case
directories for the *Study totals* counters (patients, verdicts, agreement, reviewed
patients per grade); `GET /api/cases/verdicts` rebuilds the *relabeling buffer* itself
from every verdict in the store, newest first, in the exact row shape the JSONL export
writes. Neither survives on browser state, so a reload — or a different machine on the
same backend — shows the same rows and the same totals.

Consequences, all deliberate: the buffer has **no "clear" button** (the rows are the
study's verdict log; a local wipe would only hide rows that return on the next reload —
withdraw one at a time with *Undo verdict*), and both fetches are gated on `authed`
rather than on mount, because a fetch fired before the PIN is accepted comes back 401
and would leave both panels empty for the rest of the session. A verdict the store never
received (its writes are best-effort) stays in the buffer as a local row until it can be
filed.

Two rules when touching this: the store is **best-effort** (a write failure must
never fail a prediction — see `_case_write` in `main.py`), and `case_id` comes
from the client, so it is validated against the minted format before it is ever
turned into a path. The store grows with use and is never pruned — clear old
cases by hand.

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
