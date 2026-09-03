---
name: exp4-wsl-launch
description: How Exp-4 (Grad-CAM explainability, H-5) is launched on the RTX 3060 / WSL box — trains 2× EfficientNet-B4 on EyePACS fold-0 then Grad-CAM on IDRiD; idrid path gotcha in the WSL overlay
metadata:
  type: project
---

**Launched 2026-07-17 on the RTX 3060 / WSL2 box** (native Win + `/mnt/d`). Exp-4
(`src/experiments/exp4_explainability.py`, H-5) is **not** a checkpoint-loader — its
`run()` **trains two EfficientNet-B4 models from scratch on EyePACS fold-0**: first the
**baseline** (3-ch, resize-only), then the **full pipeline** (4-ch, 8-stage). Only after
both train does it do Grad-CAM on ~50 sampled IDRiD images → IoU/ALO per lesion type →
H-5 test (IoU_full > IoU_baseline for ≥3/4 lesion types). Output: `outputs/exp4/iou_results.json`
+ `outputs/exp4/gradcam/*.png`. No SSL gate, no graded-testLabels dependency (uses EyePACS
`trainLabels.csv` + IDRiD's own labels/masks).

**Config gotcha (the reason a plain `_wsl_local.yaml` merge is NOT enough):** exp-4 reads
BOTH `paths.eyepacs` AND `paths.idrid`, but `configs/_wsl_local.yaml` only overrides
`eyepacs`. `default.yaml` still has `paths.idrid: D:/personal/phd/datasets/IDRiD` (prior box's Windows
path, nonexistent in WSL). So the merged run config must fix **both**: built
`configs/_run_exp4_wsl.yaml` = `load_configs(default, _wsl_local)` then set
`paths.eyepacs=/mnt/d/datasets/EyePACS` + `paths.idrid=/mnt/d/datasets/IDRiD` → `yaml.safe_dump`
(machine-specific, uncommitted). IDRiD verified present: 413 train imgs, grading CSV, 4
lesion-mask types under `A. Segmentation/2. All Segmentation Groundtruths/a. Training Set`.

**Launch mechanics (same durability rule as [[exp1-config-c-wsl-launch]] / [[ssl-wsl-launch-durability]]):**
detached `Start-Process`, NOT harness `run_in_background` (harness reap kills the WSL subtree).
Launcher `~/launch_exp4.sh`: conda `dr-classifier`, `cd /mnt/d/.../experiments`,
`PYTHONIOENCODING=utf-8`, `CUDA_VISIBLE_DEVICES=0`,
`run_experiment.py exp4 --config configs/_run_exp4_wsl.yaml --resume >> ~/exp4.log 2>&1`,
then `touch ~/EXP4_DONE.txt`. Launch:
`Start-Process -WindowStyle Hidden -FilePath wsl.exe -ArgumentList '-d','Ubuntu','-e','bash','/home/yesmu/launch_exp4.sh'`.
`--resume` safe from first launch (empty ckpt dir → fresh). **Do NOT relaunch on a harness
notification without first checking `pgrep -f 'run_experiment.py exp4'` + `nvidia-smi`.**

**Perf / VRAM:** B4 baseline fp32 @512²/batch-16 fits at **~12.07 GB / 12.29 GB (≈220 MiB
headroom)** — same knife-edge as B3 Config C; keep Chrome/Steam/games CLOSED. B3 was
~73 min/epoch; B4 two models × ≤20 epochs (early-stop patience 5) each ⇒ **multi-day**.
Status: `~/exp4.log`, `nvidia-smi`, `pgrep -f 'run_experiment.py exp4'`; done marker
`~/EXP4_DONE.txt`.

**PAUSED 2026-07-18 ~11:15** at operator request (SIGTERM, clean). State on disk in
`outputs/exp4/checkpoints/baseline/`: **baseline model, fold 0, through epoch 3** —
`last_checkpoint.pt` (epoch 3) + `best_model.pt` (epoch 2, best val F1 0.6576) +
`epoch_00..03.pt`; `metrics_baseline.csv` has all 4 epochs. Full-pipeline model NOT started;
Grad-CAM NOT run; no `iou_results.json` yet. **To resume:** re-run `~/launch_exp4.sh` (same
`--resume` launcher, detached `Start-Process`) — baseline fold 0 continues from epoch 4 via
`last_checkpoint.pt`, then the full-pipeline model trains from scratch, then Grad-CAM.
Baseline was **overfitting** (val loss 0.124→0.204 over ep0→3; F1 peaked ep2 0.658, ep3 0.655
= 1st no-improve of early-stop patience 5). **gotcha:** `pkill -f "run_experiment.py exp4"`
self-matches the killing shell (cmdline contains the pattern) → use a pattern the checker
line doesn't contain (e.g. `pkill -f "python -u run_experiment"`) or it dies mid-iterate.

**RESUME OOM (2026-07-19) — reproducible, blocks `--resume` on this box.** Restarting the
paused baseline (epoch 3 → 4) OOMs: 1st attempt died at epoch-4 **eval** (`pin_memory` thread,
"CUDA error: out of memory"); 2nd attempt (with `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
added to the launcher) died even earlier at the epoch-4 **first `model(images)` forward**
(`timm efficientnet … bn3 → F.batch_norm`, "CUDA driver error: out of memory"). Root cause:
B4 batch-16 fp32 @512² fits at only ~220 MiB headroom; a **fresh** run survives because Adam
state accrues on-GPU gradually, but `--resume` loads model **+ full Adam optimizer state**
onto the GPU at once → the first forward no longer fits. The env-var did NOT fix it (VRAM-in-forward,
not fragmentation). Operational levers exhausted (`pin_memory`/`num_workers` don't touch forward-pass
VRAM). Checkpoints stayed intact through both crashes (`last_checkpoint.pt`=ep3, `best_model.pt`=ep2).
**DECISION (2026-07-19):** operator confirmed this is NOT a code bug — pure CUDA OOM (the
allocator/driver refusing memory, no logic/shape/NaN error), so **no code change**. Plan:
**move exp4 to the RTX 5070 Ti box (16 GB)** and `--resume` there — the extra ~4 GB clears
the resume-load spike. Checkpoints (ep3 `last_checkpoint.pt`, ep2 `best_model.pt`) live under
`experiments/outputs/exp4/` on the external drive, so they travel. Caveat on the other box:
`configs/_run_exp4_wsl.yaml` has hardcoded `/mnt/d` paths — rebuild/adjust the merged config
for that machine's mount (was `/mnt/e` on a prior box). The 3060 launcher now carries a harmless
`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (added during diagnosis; did not fix the 12 GB ceiling).

**Note (2026-07-17):** Exp-1 **Config C** (`~/expC.log`) did NOT finish — its log ends
Jul 13 on **fold 3, epoch 13**, no `~/EXPC_DONE.txt` marker (died/killed). GPU was idle
when exp-4 launched. Config C still needs a resume/relaunch to complete its 5 folds.
See [[continual-ssl-init-decision]] for the H-1/H-5 preprocessing framing.
