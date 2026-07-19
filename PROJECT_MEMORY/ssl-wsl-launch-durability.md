---
name: ssl-wsl-launch-durability
description: "On the native-Windows+WSL RTX 3060 box, harness background tasks get reaped AND that kills the whole WSL process subtree — launch long GPU jobs DETACHED via PowerShell Start-Process, not run_in_background"
metadata:
  type: project
---

**Machine:** native Windows 11 + WSL2 Ubuntu, RTX 3060 12 GB, external drive mounts as **D:** (`/mnt/d`, NOT `/mnt/e` — that box was a prior machine). conda `dr-classifier` (torch 2.5.1+cu121, timm 1.0.25) at `~/miniconda3`. SSL Stage 0–4 cache at `/home/yesmu/ssl_cache_256` (53,576 imgs).

**Finding (2026-07-08, launching EfficientNet-B3 SSL v1.1):** TASK.md §4's "KEY FINDING" claim — that python survives a harness *killed/stopped* notification by reparenting to init — **did NOT hold here**. Three launches all died the instant the harness reaped the background task; each time GPU went idle and `pgrep run_ssl_pretrain` = empty (genuine death, not just the relay). The harness *stop* propagates into the WSL2 VM and kills the whole subtree (`wsl.exe → bash → python`), not only the Windows-side relay. Also `exec python` makes it worse (python becomes the relay's direct child); and `nohup … & disown` inside a `bash -lc` that then *returns* dies too (returning wsl.exe tears down the session — §4's other trap). Lost ~66% of epoch 0 (~75 min) on the worst restart.

**Working launch (durable):** write a launcher script in WSL, then start it as a **detached, hidden, independent Windows process** so it is in NO harness-tracked tree:
```
# /home/yesmu/launch_eff_ssl.sh : source conda; conda activate dr-classifier; cd /mnt/d/.../experiments; exec python -u scripts/run_ssl_pretrain.py <configs> --backbone efficientnet_b3 --device cuda >> ~/ssl_eff_b3.log 2>&1
Start-Process -WindowStyle Hidden -FilePath 'wsl.exe' -ArgumentList '-d','Ubuntu','-e','bash','/home/yesmu/launch_eff_ssl.sh'
```
Verified: python (PID/PPID inside WSL) keeps running with GPU at 100% after the launching PowerShell tool returns and across turns. **Do NOT re-launch on any harness notification without first checking `pgrep -f run_ssl_pretrain` + `nvidia-smi`** — a 2nd `--resume` while the 1st is alive corrupts `train_state`.

**Perf reality on this GPU:** EfficientNet-B3 BYOL, batch 32, **fp32** (AMP off — fp16 overflow), 256², 4-ch two-view → **~0.24 steps/s ≈ 8 img/s ≈ 4.1 s/step**; 1,674 steps/epoch → **~1.9 h/epoch, ep50 ≈ 4 days, ep300 ≈ 24 days**. Candidate chose to leave fp32 as-is for now (declined bf16 experiment). Faster lever if revisited: **bf16 autocast** (3060 is Ampere → bf16 has fp32 exponent range, so the fp16-overflow reason for AMP-off does NOT apply) — needs a trainer code path; ~1.5–2× + frees VRAM (currently only ~30 MiB headroom at batch 32, so keep cs2/Steam/games CLOSED or it OOMs).

**Config gotcha on this box:** `configs/_wsl_local.yaml` rides the drive with the *previous* machine's values. Fixed here: `paths.eyepacs /mnt/e→/mnt/d`; added `ssl.corpus.test_labels_csv: sampleSubmission.csv` because the graded `testLabels15.csv` is MISSING from `D:/datasets/EyePACS/` (only `sampleSubmission.csv` + `trainLabels.csv` present). sampleSubmission is a valid *stem* source for the disjointness audit (INV-SSL-2 passed: SSL 53,576/26,788pt vs train 35,126/17,563pt), but the **linear-probe GATE needs the real graded file** (true grades + Usage slice) — obtain Kaggle `retinopathy_solution.csv`, place as `testLabels15.csv`, revert that key before gating. See [[config-d-pretraining]], [[v5-cache-throughput]], [[eyepacs-local-dataset]].
