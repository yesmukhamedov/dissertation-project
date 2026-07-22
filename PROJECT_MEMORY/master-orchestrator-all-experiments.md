---
name: master-orchestrator-all-experiments
description: The master orchestrator C:/ssl_out/orchestrate_all2.ps1 runs ALL remaining experiments (finish Exp-1 A/B/C + summary -> Exp-2 Part A -> Exp-3..7) on the RTX 5070 Ti native-Windows box; how it stops and how to resume it
metadata:
  type: project
---

**Machine:** native Windows 11, **RTX 5070 Ti 16GB**, external drive mounts as **D:** (project
root `D:/dissertation-project`). Env python `C:/mamba/envs/dr-classifier/python.exe` (torch
2.11+cu128). NOT the RTX 3060/WSL box (that one uses `/mnt/d`; see [[ssl-wsl-launch-durability]],
[[exp1-config-c-wsl-launch]]). Machine-local scratch = `C:/ssl_out` (logs, markers, SSL artifacts)
and `C:/ssl_data/cache_512` (512² Stage 0–4 cache, ~35k PNGs, needed by the pipeline arm B/D).

**Driver script `C:/ssl_out/orchestrate_all2.ps1`** runs the whole remaining program in dependency
order. Each job = cheap SMOKE (fails on exit≠0 or "not yet implemented") then FULL run then
`save_results_to_D.ps1`, with per-job `done_<name>.txt` markers so completed jobs are SKIPPED on
relaunch, and runs are `--resume`-able. On any failure it writes `ALLEXP2_DONE.txt` (STATUS: ABORTED)
and STOPS (no cascading). Stages: **1** finish Exp-1 (`exp1_c4` C-fold4 → `exp1_a` A 5 folds →
`exp1_b` B 5 folds → `exp1_summary` factorial+H-1 via `C:/ssl_out/compute_exp1_summary.py`);
**2** `exp2` Part A (feasibility-bounded: 15% subset, 3 folds, `C:/ssl_out/run_exp2_partA.py`);
**3** exp3–7 smoke sequentially then FULL in VRAM-gated parallel waves (waveA=exp3/5/6 eval,
then exp4+exp7 sequential training). Success → `ALLEXP2_DONE.txt` (STATUS: SUCCESS).

**How to LAUNCH / RESUME (durable, detached — survives the harness):**
```
powershell -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -WindowStyle Hidden -FilePath 'powershell.exe' -ArgumentList '-NoProfile','-ExecutionPolicy','Bypass','-File','C:/ssl_out/orchestrate_all2.ps1'"
```
(Launch via the Bash tool — `Bash(powershell:*)` is allow-listed; the `Start-Process`/`PowerShell`
tool paths are denied in don't-ask mode.) NOT reboot-proof: re-launch after a restart; done-markers
+ `--resume` make it safe and idempotent. **Before relaunching, confirm nothing is live** (a 2nd
trainer writing the same `last_checkpoint.pt` corrupts it): `Get-CimInstance Win32_Process -Filter
"Name='python.exe'"` must be empty. A clean python crash would have left an ABORT marker, so an
abrupt log stop with no ABORT = the orchestrator PS process itself was killed (reboot/reap), not the
trainer.

**Progress signals:** log `C:/ssl_out/orchestrate_all2.log` (START/OK/ABORT per job); markers
`C:/ssl_out/done_*.txt`; metrics `D:/…/experiments/outputs/exp1/metrics.csv` (per-epoch rows,
cols epoch,fold,config,…); summary `outputs/exp1/summary.json`. Per-config completeness = 5 folds
present; a fold early-stops via patience-5 on val_weighted_f1 (a fold can legitimately end at ~ep6).

**State snapshot 2026-07-15:** Exp-1 **D complete** (5 folds), **C complete** (5 folds — supersedes
the older [[exp1-config-c-wsl-launch]] "C interrupted at fold 3" note; C-fold4 finished here as
`exp1_c4`), **A complete** (5 folds). **B** reached fold0/ep9 then the orchestrator was killed
(log stopped mid-`exp1_b_full`, no ABORT, no `done_exp1_b.txt`). **Relaunched orchestrate_all2.ps1**
this session → skipped c4+a, resumed B (smoke → `exp1_b_full --resume` continues `B_fold0` from
`last_checkpoint.pt` ep9 → folds 1–4), then summary → exp2 → exp3–7. Config B init =
`outputs/ssl/v4.0/ssl_mocov2_resnet50_4ch_256_ep50.pt` (continual, [[continual-ssl-init-decision]]).
Smoke configs write to a SEPARATE `outputs/_smoke/…` dir (safe — won't poison real fold ckpts).
Results auto-consolidate C:→D: after each stage via `save_results_to_D.ps1`
([[exp1-run-mechanics-512-cache]] §5).

**Update 2026-07-16 — exp2 REORDERED TO LAST + split across two machines.** exp2 turned out to be
the long pole: measured pace on the 15% subset (5268 imgs, CPU-bound, GPU idle) was ~3.5 h/fold even
for the cheapest `baseline` level, so the full 6-level Part A + Part B is multi-day. Since exp2 does
NOT block exp3–7 (they read exp1 checkpoints only), the orchestrator was edited so **exp3–7 run FIRST
and exp2 runs LAST** (new "STAGE 4" block; old STAGE 2 replaced by a pointer comment). exp2 was
stopped mid-`baseline` fold2 (killed the orchestrator PS + the `run_exp2_partA` python tree via
`taskkill /T`), and the partial `outputs/exp2/` was quarantined to
`outputs/exp2_baseline_partial_pc1_20260716/` so PC1's fresh metrics.csv holds only its owned levels.
**Two-machine exp2 split** (driver supports `--levels a,b,c`, writes metrics.csv incrementally, merge
at end): **PC1 (this 5070 Ti) owns the CPU-heavy levels** `baseline_clahe,baseline_augmentation,full`
(+ Part B IDRiD CLAHE sweep) — wired into the orchestrator's exp2_full args; **PC2 (RTX 3060/WSL)
owns** `baseline,baseline_canonical_flip,baseline_flat_field` — run there manually with
`run_exp2_partA.py --config <wsl cfg with /mnt/d paths> --subset-fraction 0.15 --folds 3 --levels
baseline,baseline_canonical_flip,baseline_flat_field` (driver rode to D: as
`outputs/ssl_run_artifacts/run_exp2_partA.py`; exp2 needs NO 512² cache — it toggles Stages 0–4 live).
The 6 ablation level names come from `src/experiments/exp2_ablation.py::_ABLATION_LEVELS` (6, not 7).
Orchestrator relaunched (skips exp1, runs exp3–7 then exp2). **At end: merge PC1+PC2 exp2 metrics.csv.**

**Update 2026-07-17 — exp3–7 unblocking (3 code fixes committed + 1 config + orchestrator reorder).**
Running exp3–7 first (before the multi-day exp2) surfaced a chain of latent blockers fast; each was a
clean fail-safe ABORT (marker + stop), never a crash. Fixes, all now on branch
**`fix/experiment-run-blockers`** (commit 96228aa) for the 3 `experiments/` source files:
- **exp4 dispatch TypeError** — `exp4_explainability.run()` lacked the `_configs_to_run` kwarg the
  dispatcher passes to every exp (only exp4 missing it). Added.
- **`_eval_utils._train_fresh`** — read a nonexistent `config["augmentation"]` (KeyError) and
  double-augmented; now `augmentation=None` (Stage-6 aug is already in the is_training pipeline).
- **`exp2_ablation._run_clahe_sweep`** — hardcoded `/mnt/d/datasets/IDRiD/...` (WSL) that crashes on
  native Windows; now reads `config["paths"]["idrid"]` (needed for exp2 Part B on PC1).
- **exp3–7 smoke path (config, NOT committed — machine-specific run-config):** `_run_gen_smoke.yaml`
  had `output_dir: outputs/_smoke/gen/`, but exp3/5/6/7 resolve exp1 checkpoints as
  `<output_dir>/exp1/checkpoints/{D,B,C,A}_fold0/best_model.pt` (`_eval_utils.load_or_train_model` /
  `load_baseline_model`). So the smoke looked in the wrong tree → exp5 fresh-trained 2.2 h then hard-
  failed, exp3 false-passed by fresh-training. Fixed to `output_dir: outputs/` (same as full
  `_run_gen.yaml`); smokes now LOAD the real exp1 checkpoints and run as fast evals. Verified: exp5
  smoke no longer creates `outputs/exp5/checkpoints/eyepacs_full_fold0` and loads the ckpt on GPU.
- **exp4 CUDA fault + reorder:** after the dispatch fix, exp4 (heavy — trains its own EfficientNet-B4
  on FULL EyePACS, ~2 h/epoch, NOT a light eval; its "smoke" is the same weight) hit a transient
  `torch.AcceleratorError: CUDA error: unknown error` in backward (~2 h in; GPU healthy after → likely
  transient, possibly systematic in the 4-ch full-pipeline B4 path / U-Net-on-GPU contention / AMP).
  So exp4 was **moved to run DEAD LAST (STAGE 5, after exp2)** and dropped from the smoke loop, so a
  re-fail can't block exp5/6/7/exp2.
  - **RESOLVED 2026-07-17 (commit 92a881a, fable subagent).** Root cause was NOT AMP (B4
    mixed_precision is correctly False). exp4's full-pipeline (4-ch) path runs the learned U-Net
    OD/fovea detector LIVE inside `Dataset.__getitem__`; on Windows each of the 4 spawned DataLoader
    workers built its OWN CUDA context and ran 512² U-Net inference concurrently with the main-process
    fp32 B4 backward on the shared 16 GB GPU → `cudaErrorUnknown`. (exp1 full never hit it because it
    reads the Stage 0–4 cache, so its workers never invoke the detector.) Fix: `od_fovea_net/infer.py`
    forces the detector to CPU when `get_worker_info()` shows it's inside a DataLoader worker (main
    process keeps CUDA); `exp4_explainability.py` moves the baseline model to CPU + `empty_cache()`
    before training the full model. **Bonus: this also de-risks exp2's own `full` ablation level**,
    which runs the same U-Net-in-workers path. Residual: if exp4 still faults last, try
    `CUDA_LAUNCH_BLOCKING=1` for the true op + batch 8/grad-accum.
- **Orchestrator now also writes per-smoke markers** `done_<exp>_smoke.txt` so a relaunch does not
  re-run an already-passed smoke (exp3's ~2.4 h smoke is skipped). Order now:
  exp5→6→7 smokes → waveA(exp3/5/6 full) → exp7 full → exp2 (PC1 heavy) → **exp4 last**.
  The `_run_*.yaml` merged run-configs stay UNCOMMITTED (machine-absolute paths, ride the drive).

**Update 2026-07-19 — exp2 stopped mid-way; exp4 resumed on PC1 from PC2; exp2 finishes AFTER exp4.**
Branch `fix/experiment-run-blockers` (2 commits) was merged + pushed to `origin/main`. The `full` ablation
level is very slow (U-Net now on CPU per the fix) and the machine slept overnight, so exp2 on PC1 was
**stopped** (killed orchestrator + `run_exp2_partA` tree). exp2 PC1 state saved on D: (`outputs/exp2`):
`baseline_clahe` (3 folds ✅), `baseline_augmentation` (3 folds ✅), `full` (fold0/1 ✅, **fold2 partial**).
**exp2 STILL MISSING:** the 3 LIGHT levels `baseline`,`baseline_canonical_flip`,`baseline_flat_field`
(**PC2 ran exp4, NOT these**), `full` fold2, Part B (IDRiD CLAHE sweep), `ablation_summary.json`.
**Plan: finish exp2 on PC1 AFTER exp4** — `run_exp2_partA.py --levels baseline,baseline_canonical_flip,baseline_flat_field`
fresh + finish `full` fold2 (resume its `last_checkpoint.pt` to keep fold0/1, OR re-run whole `full`) + `--partb`
(driver runs a level's folds as a block — no single-fold flag). **exp4 RESUMED on PC1 (free GPU) 2026-07-19**
from PC2's copied `outputs/exp4/checkpoints/baseline/` (B4 ep0–3, `last_checkpoint.pt` ep3):
`run_experiment.py exp4 --config configs/_run_gen.yaml --resume` (detached; PID in `C:/ssl_out/exp4_resume.pid`,
logs `C:/ssl_out/exp4_resume.{out,err}.log`) → continues baseline from ep4, then `full_pipeline` fresh, then
Grad-CAM. Resume verified: `trainer.train_fold` `load_latest` → `start_epoch = ckpt.epoch+1` (trainer.py:246-253).
`done_exp4.txt` keeps the orchestrator off exp4; exp2 was stopped — both remaining pieces now run MANUALLY.
**AUTO-CHAIN set up 2026-07-19:** detached watcher `C:/ssl_out/chain_exp2_after_exp4.ps1` (PID in
`chain_exp2.pid`, log `chain_exp2.log`) polls exp4's PID, and once exp4 exits AND its `exp4_resume.err.log`
shows no Traceback/CUDA error, it launches the exp2 remainder = `run_exp2_partA.py --folds 3 --partb
--levels baseline,baseline_canonical_flip,baseline_flat_field` (3 light levels + Part B) on the freed GPU
→ marker `CHAIN_EXP2_DONE.txt` (or `CHAIN_EXP2_ABORTED.txt` if exp4 crashed). It deliberately does NOT
auto-do `full` fold2 (would redo fold0/1) or the final `ablation_summary.json` — those two are finished
by hand after. NOT reboot-proof; machine must stay awake (it slept overnight once, freezing progress).
exp4 resume VERIFIED live: `metrics_baseline.csv` advanced ep3→ep4→ep5 (continued, not restarted).

**Update 2026-07-21 — exp4 PAUSED at operator request; exp2 remainder run FIRST (order swapped).** Operator
chose to run the exp2 remainder before finishing exp4. exp4 state at pause: baseline model DONE (20 epochs,
best ep17 val-wF1 0.754); **full_pipeline model paused cleanly at the epoch-3 boundary** —
`outputs/exp4/checkpoints/full_pipeline/last_checkpoint.pt` = ep3 (10:52), `epoch_00..03.pt` + `best_model.pt`
(ep2). Grad-CAM/IoU NOT run. full_pipeline pace was ~3.5 h/epoch (U-Net detector on CPU per the 92a881a fix).
Switch mechanics (native-Win 5070 Ti box): killed the **chain watcher** (`chain_exp2_after_exp4.ps1`, was PID
17124) FIRST so it couldn't race, then `taskkill /PID <exp4> /T /F` (GPU 15.8 GB → 1.15 GB), then launched
the exp2 remainder DETACHED via new **`C:/ssl_out/launch_exp2_manual.ps1`** (mirror of the watcher's step-3
cmd + a 25 s VRAM-release sleep): `run_exp2_partA.py --config configs/_run_exp2.yaml --subset-fraction 0.15
--folds 3 --partb --levels baseline,baseline_canonical_flip,baseline_flat_field`. Logs
`C:/ssl_out/exp2_remainder.{log,out.log}`; done marker `EXP2_REMAINDER_DONE.txt`. exp2 confirmed live
(loading EyePACS index; CPU-bound so GPU ~0% in this phase — expected). **To resume exp4 later:**
`run_experiment.py exp4 --config configs/_run_gen.yaml --resume` → baseline instant (already at max_epochs),
full_pipeline continues from ep4 (watch for a resume-load VRAM spike, but 16 GB cleared it for baseline).
**exp2 STILL MISSING after this remainder:** `full` fold2 completion + `ablation_summary.json` (both manual,
see [[master-orchestrator-all-experiments]] 2026-07-19 note). exp2 done-so-far on D: `outputs/exp2`:
baseline_clahe (3 folds ✅), baseline_augmentation (3 folds ✅), full (fold0 ✅, fold1 ✅, fold2 partial ep1).

**Update 2026-07-21 (later) — BOTH experiments STOPPED at operator request; nothing training now.** After
confirming exp4 and exp2 cannot run in parallel on the single 16 GB GPU (each needs ~15.8 GB at the mandatory
batch 16; shrinking batch would invalidate exp2's ablation + exp4's baseline-vs-full comparison; both are also
CPU-bound so no wall-clock win), the operator stopped everything. exp2 python tree (was PID 11348) killed;
GPU freed to ~0.95 GB. **NOTHING is training as of this note.** State on D: unchanged from the pause snapshots:
exp4 = baseline done + full_pipeline `last_checkpoint.pt` ep3; exp2 = baseline_clahe/baseline_augmentation
(3 folds each) + full fold0/1 done, full fold2 partial, and the 3 light levels NOT started (their run had only
just begun, no durable rows). Resume commands: exp4 → `run_experiment.py exp4 --config configs/_run_gen.yaml
--resume`; exp2 remainder → `C:/ssl_out/launch_exp2_manual.ps1` (or the `run_exp2_partA.py … --levels
baseline,baseline_canonical_flip,baseline_flat_field` cmd inside it).
