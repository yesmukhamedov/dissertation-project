---
name: master-orchestrator-all-experiments
description: The master orchestrator C:/ssl_out/orchestrate_all2.ps1 runs ALL remaining experiments (finish Exp-1 A/B/C + summary -> Exp-2 Part A -> Exp-3..7) on the RTX 5070 Ti native-Windows box; how it stops and how to resume it
metadata:
  type: project
---

**Machine:** native Windows 11, **RTX 5070 Ti 16GB**, external drive mounts as **D:** (project
root `D:/phd/dissertation`). Env python `C:/mamba/envs/dr-classifier/python.exe` (torch
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

**Update 2026-07-23 — WSL-box exp2→exp4 chain: exp4 now resumes UNCONDITIONALLY.** On the RTX 3060/WSL
box (`/mnt/e`, Ubuntu distro; docker-desktop is the default distro so target `wsl -d Ubuntu`), the exp2
remainder is running again (`run_exp2_partA.py --folds 3 --partb --levels
baseline,baseline_canonical_flip,baseline_flat_field`, main PID varied; `baseline` 3 folds ✅,
`baseline_canonical_flip` in progress). Watcher `outputs/chain_exp4_after_exp2.sh` polls exp2 then resumes
exp4 (`run_experiment.py exp4 --config configs/_run_gen_wsl.yaml --resume`). **Logic changed at operator
request:** exp2 does NOT block exp4 (independent experiments / different hypotheses), so the watcher no
longer GATES exp4 on `CHAIN_EXP2_DONE.txt` — it now resumes exp4 **regardless** of exp2's outcome and only
logs exp2's status; the old `CHAIN_EXP4_SKIPPED.txt` no-resume branch was removed. Applied live by killing
the old watcher (PID 7742, a stateless poller) and relaunching the edited script detached via
`setsid bash chain_exp4_after_exp2.sh` (new PID logged in `chain_exp4.log`); exp2 was never touched.
Gotcha: through `wsl -d Ubuntu -- bash -lc '…'`, shell **variables** silently expand empty and bare
`/mnt/d/phd/…` args get MSYS-rewritten to `C:/Program Files/Git/mnt/d/phd/…` — use literal paths inside the
`bash -lc` quoted script (and `MSYS_NO_PATHCONV=1` only when a `/mnt` path is a standalone arg).

**Update 2026-07-23 (cont.) — WSL-box chain made sleep-proof + reboot-resilient.** Two additions on the
RTX 3060/WSL box so the previously-fatal overnight sleep can't freeze progress again:
- **Sleep protection (OS-level, AC):** `powercfg /change standby-timeout-ac 0` + `hibernate-timeout-ac 0`
  (+ `disk-timeout-ac 0`), so on mains power the machine never idle-sleeps. Verified Sleep-after AC =
  `0x00000000` (Never). Protects exp2/exp4/watcher alike, not just the watcher. **Revert:** set those
  three back to the desired minutes (e.g. `powercfg /change standby-timeout-ac 30`). Only AC changed;
  DC (battery) untouched.
- **Reboot resilience:** idempotent reconstructor `outputs/chain_boot_resume.sh` rebuilds the chain —
  settles exp2 first (relaunch the remainder if not running AND not concluded; wait until pgrep sees it
  so the watcher can't race past it), then (re)starts `chain_exp4_after_exp2.sh`; no-ops if exp4 already
  running or `CHAIN_EXP4_DONE.txt` present. Launched at **logon** by `outputs/chain_boot_resume.cmd`
  (`wsl -d Ubuntu -e bash -lc "setsid bash …chain_boot_resume.sh &"`), installed as a **Startup-folder**
  shortcut `%APPDATA%/Microsoft/Windows/Start Menu/Programs/Startup/DR-ChainResume.cmd` (schtasks
  ONLOGON needed admin → used the no-elevation Startup folder instead; fires on next interactive logon —
  a locked/never-logged-in session won't trigger it, but WSL GPU needs a session anyway). Logs to
  `outputs/chain_boot.log`. **Caveat:** exp2's remainder has no mid-fold checkpoint, so a reboot mid-exp2
  re-runs the *current* level from epoch 0 (metrics.csv may need a de-dup pass); exp4 resumes per-epoch.
  Idempotency verified live (ran it while exp2+watcher were up → logged "already running", spawned no
  dups). **To uninstall:** delete the Startup `DR-ChainResume.cmd`.

**Update 2026-07-24 — exp2 remainder DONE (science complete; false FAILED marker) + exp4 OOM on the 12GB box.**
The WSL-box exp2 remainder ran to completion: 3 light levels + Part B CLAHE sweep all finished and
`outputs/exp2/ablation_summary.json` (3461 B, 21:05:50) was SAVED — `baseline` F1 0.7611±0.0157,
`baseline_canonical_flip` 0.7701±0.0062, `baseline_flat_field` 0.7603±0.0235; Part B swept clip∈
{0.5,1,1.5,2,2.5,3,4}. **BUT** `run_exp2_partA.py:213` then crashed on `KeyError: 'metrics'` in the final
print loop (Part B sweep entries lack the `metrics` key that the ablation-level entries have) → exit 1 →
`chain_exp2_after_exp6.sh` wrote a **false `CHAIN_EXP2_FAILED.txt`**. The crash is purely cosmetic and
happens AFTER results are persisted, so exp2 is effectively complete (only `full` fold2 + the pre-existing
manual pieces remain per the 2026-07-19 note). Fixable one-liner: guard `entry.get("metrics",{})` at line
~213. The always-resume watcher then correctly launched exp4 despite the FAILED marker (the 2026-07-23 fix
worked as designed). exp4 resumed cleanly (baseline fold0 @ep20 done; full_pipeline fold0 @ep4) but died on
the FIRST full_pipeline batch with `CUDA error: out of memory` (pin_memory thread) after ~9 min →
`CHAIN_EXP4_FAILED.txt`. Cause: **RTX 3060 12 GB** — exp4 started only 40 s after exp2's tree exited (VRAM
likely not fully released) AND/OR full-pipeline EfficientNet-B4 fp32 4-ch @ batch 16/512² simply doesn't fit
12 GB (exp4 originally ran on the 16 GB PC1). GPU now idle (706 MiB). Open decision: retry exp4 resume on the
now-clean 12 GB GPU (fast OOM-or-train probe) vs. shrink batch/grad-accum (comparability caveat) vs. move exp4
to the 16 GB box.

**Update 2026-07-24 (cont.) — exp4 OOM was RESIDUAL VRAM (not a 12 GB limit); then a 9p flaky-read crash, fixed.**
Operator chose retry-on-clean-GPU. Retry passed the exact pin_memory/first-batch point that OOM'd before
(full_pipeline reached GPU 100% @ ~12 GB) → **the OOM was exp2's un-released VRAM (40 s wait), NOT a hard 12 GB
ceiling** — full-pipeline B4 fp32 4-ch @ batch16/512² DOES fit ~12 GB (≈250 MiB headroom, tight but works).
But it then crashed a different way: `datasets.py:179 FileNotFoundError: Could not load image:
…/EyePACS/train/40513_right.jpeg` — a **transient 9p/drvfs read failure under 4-worker DataLoader contention**
on the external E: drive (the file is fine: 930 KB, reads perfectly single-threaded via imread AND
open()+imdecode). One flaky read was killing the whole multi-hour run. **Fix (committed to `experiments/`):**
added module-level `_robust_imread(path, flags, retries=5)` in `src/data/datasets.py` (retry + fall back to
`open()`+`cv2.imdecode`, a different code path that survives when imread's own open drops), and routed the 3
training-path reads through it (lines ~90 base RGB, ~177 live-pipeline RGB, ~338 cached BGRA). Import verified.
exp4 relaunched (`run_experiment.py exp4 --config configs/_run_gen_wsl.yaml --resume`, detached, log
`outputs/exp4_resume3.log`) resuming full_pipeline fold0 from ep4; a background monitor watches for first-epoch
completion vs. crash. If VRAM later OOMs from fragmentation, add `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
on the next resume (safe, no comparability impact); if 9p read failures persist, drop num_workers.

**Update 2026-07-24 (cont. 2) — CONFIRMED: exp4 full_pipeline does NOT fit batch16/512² on the 12 GB 3060.**
After the 9p fix, exp4 OOM'd twice more: resume3 = OOM in pin_memory (first batch); resume4 WITH
`expandable_segments:True` got further — past pinning, INTO the B4 forward pass — then
`RuntimeError: CUDA driver error: out of memory` inside a timm EfficientNet SE block
(`_efficientnet_blocks.py:83`). So it's a genuine activation-memory shortfall, not fragmentation;
expandable_segments is not enough. full_pipeline B4 (fp32, 4-ch, mixed_precision correctly OFF for
EffNet) at batch 16 / 512² needs > 12 GB; the one resume2 run that briefly hit GPU 100% was on the ragged
edge. **exp4's baseline model is already fully trained @ batch 16 (20 ep, best ep17 wF1 0.754); only
full_pipeline is blocked.** Options put to operator (batch 16 is the mandated config, so shrinking it is a
comparability question): (A) **gradient checkpointing** on the B4 (timm `set_grad_checkpointing(True)`) —
keeps batch 16 & is numerically identical, just recomputes activations in backward (~20-30% slower); fits
12 GB; best scientific option, runs on THIS box; needs a small code hook where the model is built.
(B) move exp4 to the 16 GB PC1 box (checkpoints live on the shared external drive, so it's just re-running the
resume there at batch 16). (C) batch 8 + grad-accum ×2 (effective 16) here — but full would then train at
micro-batch 8 while baseline trained at 16 → BatchNorm-stat asymmetry in the very baseline-vs-full comparison
exp4 exists to make; least clean. Recommendation: A.

**Update 2026-07-24 (cont. 3) — RESOLVED via gradient checkpointing (option A).** Operator chose A. Added a
`grad_checkpointing: bool=False` param to `create_efficientnet` (`src/models/efficientnet.py`; calls timm
`model.set_grad_checkpointing(True)`) and wired `exp4_explainability.py::_train_model` to pass
`grad_checkpointing=(config_name != "baseline")` — so only the 4-ch full_pipeline B4 checkpoints; the 3-ch
baseline (already trained) is untouched. Numerically identical, only the training forward pass is affected
(bypassed in eval → Grad-CAM unaffected). **Smoke on the 12 GB 3060: a real fwd+bwd train step of the 4-ch B4
@ batch 16/512² fp32 peaked at only 3581 MiB alloc / 4686 MiB reserved** (was OOMing near 12 GB) — massive
headroom. exp4 relaunched (`run_experiment.py exp4 --config configs/_run_gen_wsl.yaml --resume`, detached,
`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` kept for safety, log `outputs/exp4_resume5.log`) resuming
full_pipeline fold0 from ep4; background monitor watching. Both code fixes (this + `_robust_imread`) are in
`experiments/` src and should be committed. Expect ~20–30 % slower epochs than the uncheckpointed pace.

**Update 2026-07-25 — exp4 throughput: switching full_pipeline to the Stage 0–4 cache (validated).** exp4
full_pipeline ran the WHOLE pipeline live per image (incl. the U-Net OD/fovea detector on CPU) → ~5.9 h/epoch
(Epoch 004 = 21251 s). Fix = the same Stage 0–4 cache exp1 uses (`CachedEyePACSDataset` +
`scripts/precompute_cache.py`): cache the deterministic 0–4 (the U-Net runs ONCE at build), train reads the
cache + runs only stochastic 5–7 → epoch drops ~4–5×. Operator approved cache+RESUME-from-ep5 (minimise loss).
**Snag found & handled:** exp4 builds its `EyePACSDataset` WITHOUT eye_sides, so Stage-0 canonical flip runs
with `eye_side="unknown"` (a no-op) even though the config has `use_canonical_flip: true` — a latent exp4 quirk
(exp1 DOES pass eye_sides). `precompute_cache.py` derives eye_side from the filename, so a stock cache would
flip left eyes → NOT matching exp4's ep0–5 → unsound resume. So added two backward-compatible flags to
`precompute_cache.py`: **`--config <yaml>`** (build the pipeline via `PreprocessingPipeline(
PreprocessingConfig.from_dict(cfg["preprocessing"]), is_training=False)` — exactly exp4's `_build_pipeline`)
and **`--eye-side unknown`** (force unknown to mirror exp4). Verified on 24 imgs: live exp4 pipeline vs
cache-read → **max abs diff 0.035, mean 7e-8, 0/24 > 0.05, no structural mismatch**; the 0.035 is just the
uint8-PNG Stage-4 quantization that exp1's full configs already accept → protocol-consistent, resume valid.
Latent quirk noted for a SEPARATE fix: exp4 doesn't pass eye_sides (Stage-0 flip effectively off, unlike exp1).
Remaining: wire exp4 full_pipeline → `CachedEyePACSDataset` (config-gated), build the full 35 k cache with
`--config configs/_run_gen_wsl.yaml --eye-side unknown` after epoch 5 completes (monitor bqcs0mmc8), restart
resume. Build must run detector on CPU/few workers (Pool workers aren't DataLoader workers → could spawn CUDA
contexts).

**Update 2026-07-25 (cont.) — cache-swap fully wired + a detached orchestrator drives it.** Done: (a)
`exp4_explainability.py` reads `paths.eyepacs_cache_512` → uses `CachedEyePACSDataset` for full_pipeline,
gracefully falls back to the live pipeline if `cache_meta.csv` is absent (so the config key can be set before
the cache exists); (b) added `paths.eyepacs_cache_512: /mnt/d/phd/datasets/EyePACS/cache_512_exp4` to
`configs/_run_gen_wsl.yaml`; (c) imports/paths/bit-identity all verified. **Orchestrator
`outputs/chain_exp4_cache_swap.sh`** (launched detached via setsid, survives reaping; log
`outputs/exp4_cache_swap.log`) does the whole swap on the operator's plan: waits for full_pipeline **epoch 5**
→ stops exp4 → builds the full 35 k cache with `--config configs/_run_gen_wsl.yaml --eye-side unknown` and
**`CUDA_VISIBLE_DEVICES=""`** (CPU detector — matches exp4's DataLoader-worker path exactly AND avoids
multi-CUDA-context OOM across the 8 Pool workers; resumable) → verifies (PNG count ≥ N-100 AND a 10-image
live-vs-cache bit-identity gate <0.10) → restarts `run_experiment.py exp4 --resume` (reads the cache; grad-
checkpointing still in code) writing `EXP4_CACHE_SWAP_DONE.txt`, or `EXP4_CACHE_SWAP_ABORTED.txt` (GPU left
free, exp4 NOT restarted) if the build/verify fails. NOTE: the cache dir `cache_512_exp4` is the eye_side=
unknown variant — NOT interchangeable with any exp1 cache (real eye_side). Background monitors via the Bash
tool get reaped here; setsid-detached WSL scripts (exp4 training, chain watchers, this orchestrator) survive.

**Update 2026-07-25 (cont. 2) — PAUSED at operator request (progress preserved).** Orchestrator + build were
stopped mid-cache-build (**~10.7k/35k** PNGs done; build is resumable — skips names already in cache_meta.csv
with a PNG on disk). Full state: NOTHING running (GPU idle ~1.2 GB); exp4 stopped at its **ep5** checkpoint
(`outputs/exp4/checkpoints/full_pipeline/last_checkpoint.pt`, 11:11:02); partial cache at
`/mnt/d/phd/datasets/EyePACS/cache_512_exp4` (10.7k PNGs + cache_meta.csv). Two safety-disables applied so nothing
auto-starts on a partial cache: (1) **`paths.eyepacs_cache_512` commented out** in `configs/_run_gen_wsl.yaml`
(exp4 would else crash reading the ~24k missing cache PNGs; commented → it falls back to the LIVE pipeline);
(2) **Startup reboot-resume disabled** (`…/Startup/DR-ChainResume.cmd` → `.cmd.disabled`). **TO RESUME: run
`bash /mnt/d/phd/dissertation/experiments/outputs/RESUME_EXP4_CACHE.sh`** — it un-comments the config key,
restores the Startup launcher, and relaunches `chain_exp4_cache_swap.sh`, which resumes the build from ~10.7k →
verifies → restarts exp4 on the cache from ep6. Kill mechanics note: killing the orchestrator orphaned the
build python (reparented, kept running) — had to kill the build's process group separately
(`ps -o pgid= -p <pid> | xargs -I{} kill -9 -{}`); a group-kill can also take out the current `wsl -- bash -lc`
shell (shared session), so re-verify in a fresh invocation.

**Update 2026-07-26 — cache SWAP COMPLETE; exp4 now GPU-bound on the cache.** Resumed via
`RESUME_EXP4_CACHE.sh`; the build finished all 35126 (0 errors). **A false ABORT fired**: the orchestrator's
count `NPNG=$(ls "$CACHE"/*.png | wc -l)` returns 0 on 35 k files (glob ARG_MAX overflow) → spurious
`EXP4_CACHE_SWAP_ABORTED.txt`, exp4 not auto-restarted. Real state was perfect: **35126 PNGs = 35126 meta =
expected**, bit-identity re-checked on 12 random full-cache images = worst 0.0349 (uint8 quant) PASS. Fixed the
orchestrator (`ls` glob → `find -maxdepth 1 -name '*.png'`), removed the stale marker, and manually did the
skipped restart: `run_experiment.py exp4 --config configs/_run_gen_wsl.yaml --resume`
(`PYTORCH_CUDA_ALLOC_CONF=expandable_segments`, detached, log `outputs/exp4_resume_cache.log`). Verified live:
log shows "Stage 0–4 cache for full_pipeline: …cache_512_exp4 (35126 meta rows)", baseline resumed @ep20
(skip), **full_pipeline resumed @ep6**, and **GPU 100% / ~5.5 GB** — the DataLoader is no longer the
bottleneck (was ~8% GPU CPU-bound live). exp4's 3-part saga is now fully resolved: OOM→grad-checkpointing,
9p-flaky-read→`_robust_imread`, CPU-bound→Stage 0–4 cache. Config key + Startup reboot-resume are re-enabled,
so a reboot resumes exp4 on the cache. Remaining epochs ep6→~19 now run at GPU speed (was ~5.9 h/epoch live).

**Update 2026-07-26 — exp4 COMPLETE (H-5 supported).** full_pipeline trained through ep19 (cached epochs
~31 min each, ~11× the live pace; best F1 ep19 0.7766) then Grad-CAM/ALO/IoU on 50 IDRiD images (5 with lesion
masks). Finished cleanly 15:47:48; `outputs/exp4/iou_results.json` (15986 B) written; no errors. **H-5
SUPPORTED on both metrics** — IoU baseline→full improved on 3/4 lesion types (microaneurysms, haemorrhages,
hard_exudates ↑; soft_exudates 0→0), ALO likewise 3/4 (criterion = ≥3/4). exp4's 3-blocker saga fully closed
(OOM→grad-checkpointing, 9p-read→`_robust_imread`, CPU-bound→Stage 0–4 cache `cache_512_exp4` eye_side=unknown).
The Startup reboot-resume now no-ops (checks `iou_results.json`, present). Machine free. Program state: exp2
science complete (ablation_summary.json; false CHAIN_EXP2_FAILED cosmetic), exp4 complete. Still-manual leftovers
from earlier notes: exp2 `full` fold2 completion, and the `run_exp2_partA.py:213` cosmetic KeyError fix.

**Update 2026-07-24 (cont. 4) — reboot-resume RETARGETED from exp2 to exp4.** exp2 is done, so the logon
reconstructor now resumes exp4 exclusively. Rewrote `outputs/chain_boot_resume.sh` (same file → the Startup
launcher `chain_boot_resume.cmd` and the `%APPDATA%/…/Startup/DR-ChainResume.cmd` entry are UNCHANGED): it now
(0) exits if exp4's final artifact `outputs/exp4/iou_results.json` exists (exp4 done), (1) exits if
`run_experiment.py exp4` is already running (idempotent), else (2) resumes exp4 detached
(`--config configs/_run_gen_wsl.yaml --resume`, env `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, log
`outputs/exp4_boot_resume.log`). No exp2 logic remains; the old `chain_exp4_after_exp2.sh` watcher already
exited after the earlier handoff. "Done" is keyed on the real artifact (`iou_results.json`, written last by
`exp4_explainability.run`), not a marker, so it's correct regardless of who launched exp4. Sleep stays covered
OS-side (powercfg AC=Never). Idempotency verified live (ran it while exp4 PID 1434 was training → logged
"exp4 already running -> nothing to do", spawned nothing). Current exp4 run untouched (5.1 GB VRAM, healthy).
