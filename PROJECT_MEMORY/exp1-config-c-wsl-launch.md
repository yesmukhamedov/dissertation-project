---
name: exp1-config-c-wsl-launch
description: How Exp-1 Config C (baseline + EfficientNet-B3) is launched on the RTX 3060 / WSL box — no 512² cache needed (baseline arm), detached Start-Process launch, VRAM near-full
metadata:
  type: project
---

**Launched 2026-07-10 on the RTX 3060 / WSL2 box** (the *less* powerful machine;
Config **D** runs in parallel on the RTX 5070 Ti box — see [[exp1-run-mechanics-512-cache]]).
Config **C** = baseline arm (stretch-resize + ImageNet norm, **3-ch**) + EfficientNet-B3,
ImageNet-pretrained (`init.source=imagenet`), `mixed_precision=False` (fp16 overflow).

**Why C is much simpler than D:**
- **No 512² Stage 0–4 cache** — baseline preprocessing is live stretch-resize (no 8-stage
  pipeline, no U-Net OD/fovea detector), cheap enough to run live (~2.7 s/step @512²/batch-16).
- **No SSL checkpoint / gate** — baseline arm is ImageNet, not the gated fundus-SSL init.
- **Guardrail:** `exp1_factorial.run` **raises** if `paths.cache_dir` is set for a baseline
  config (A/C). The merged run config must therefore have **no `paths.cache_dir`** (default +
  `_wsl_local.yaml` already omit it — `_wsl_local` only sets `ssl.cache_dir`, a different key).

**Run mechanics (mirror of the D memory, but this box):**
1. `run_experiment.py` loads ONE config (`load_config`), so pre-merge into a single file:
   `load_configs("configs/default.yaml","configs/_wsl_local.yaml")` → `yaml.safe_dump` →
   **`configs/_run_exp1C_wsl.yaml`** (machine-specific, uncommitted). `_wsl_local` supplies
   `paths.eyepacs=/mnt/d/datasets/EyePACS`.
2. **Durable launch = detached `Start-Process`**, NOT harness `run_in_background` (harness
   reaping kills the WSL subtree — see [[ssl-wsl-launch-durability]]). Launcher `~/launch_expC.sh`:
   sources conda `dr-classifier`, `cd /mnt/d/phd/dissertation/experiments`,
   `PYTHONIOENCODING=utf-8`, runs `run_experiment.py exp1 --config configs/_run_exp1C_wsl.yaml
   --configs C --resume >> ~/expC.log 2>&1`, then `touch ~/EXPC_DONE.txt`.
   Launch: `Start-Process -WindowStyle Hidden -FilePath wsl.exe -ArgumentList '-d','Ubuntu','-e','bash','/home/yesmu/launch_expC.sh'`.
3. **`--resume` is safe from the first launch** (empty ckpt dir → `load_latest` raises
   FileNotFoundError → train_fold starts fresh). On relaunch-after-kill, re-run the SAME
   launcher: completed folds reload their best ckpt instantly; a killed fold continues from
   `last_checkpoint.pt`. **Delete smoke/subset outputs before a real launch** — a subset
   checkpoint in `outputs/exp1/checkpoints/C_fold0` would poison `--resume`.

**Perf / VRAM:** EffNet-B3 fp32 @512²/batch-16 pins the GPU at **100%, ~12.07 GB / 12.29 GB
(≈220 MiB headroom)** — keep Chrome/Steam/games CLOSED or it OOMs. ~2.7 s/step → ~28.1k
train imgs/fold ≈ 1756 steps/epoch ≈ ~80 min/epoch; ≤20 epochs (early-stop patience 5) × 5
folds → multi-day. Status: `~/expC.log`, `nvidia-smi`, `pgrep -f run_experiment`; done marker
`~/EXPC_DONE.txt`. Metrics land in `experiments/outputs/exp1/metrics.csv` + `summary.json`.
See [[continual-ssl-init-decision]] (H-1 caveat: C is the ImageNet pair for D).
