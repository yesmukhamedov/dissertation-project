---
name: project-relocation-d-phd
description: 2026-08-30 проект переехал на D:\phd\dissertation (диска E: больше нет); карта старых и новых путей, фикс git safe.directory, что ещё осталось стухшим
metadata:
  type: project
---

**2026-08-30 проект переехал.** Диска `E:` на этой машине больше нет — всё живёт под `D:\phd\`.
Репозиторий перестал читаться Git'ом до тех пор, пока новый путь не был помечен доверенным.

## Карта путей

| Было | Стало |
|---|---|
| `E:\dissertation-project` → позже `D:\dissertation-project` | `D:\phd\dissertation` |
| `E:\datasets` | `D:\phd\datasets` |
| `E:\dissertation_council` / `D:\dissertation_council` | `D:\phd\council` |
| `/mnt/e/dissertation-project`, `/mnt/d/dissertation-project` | `/mnt/d/phd/dissertation` |
| `/mnt/e/datasets` | `/mnt/d/phd/datasets` |

Датасеты на месте и полные: `APTOS 2019`, `clinical`, `DDR`, `downloaded`, `EyePACS`, `IDRiD`,
`Messidor-2`, `ODIR-5K`, `RFMiD`. Соседи проекта под `D:\phd\`: `council`, `coursework`, `history`.

## Git после переезда

Git отказывался читать репозиторий целиком:

```
fatal: detected dubious ownership in repository at 'D:/phd/dissertation'
```

Из-за этого история выглядела пустой, а изменения — отсутствующими. Лечится один раз на машину:

```
git config --global --add safe.directory D:/phd/dissertation
```

После этого всё на месте: `origin` = `git@github.com:yesmukhamedov/dissertation-project.git`
(SSH-ключ рабочий), `main` синхронизирована, ветки `fix/experiment-run-blockers` и
`metadata-registry` целы. **Имя удалённого репозитория на GitHub осталось `dissertation-project`
— это не путь, переименовывать в текстах не нужно.** Вложенных `.git`, submodule'ов и абсолютных
путей в `.git/config` нет.

## Что НЕ пережило переезд

- `D:\удаленные` — карантин чистки 2026-08-12, лежал вне репозитория. Каталога нет,
  `restore.ps1` недоступен. См. [[quarantine-cleanup]].
- `E:\archive02\dr-classifier` — локальный клон зеркала `experiments/`. Не найден нигде
  под `D:`; при необходимости клонировать заново с `github.com/yesmukhamedov/dr-classifier`.
  См. [[config-d-cache-handoff]].

## Что ещё стухло (на 2026-08-30 не исправлено)

Документация (`CLAUDE.md`, `AGENTS.md`, `demo/CLAUDE.md`, `PROJECT_MEMORY/`) приведена в порядок,
а вот **исполняемые файлы всё ещё указывают на `E:`** и упадут при запуске:

- `experiments/configs/_run_exp1C_wsl.yaml`, `_run_exp4_wsl.yaml` — `paths.*: E:/datasets/...`
- `defense/figures/scripts/` — `fig2_lesion_overlays.py`, `fig3_dataset_contents.py`, README
- `defense/presentation/scripts/split_preprocessing_svg.py`, `defense/manuscript/figures_hires/make_figures.py`
- `demo/RUNBOOK.md`, `demo/start-demo.ps1`, `demo/start-tunnel.ps1` — комментарии и `/mnt/d/dissertation-project`
- `.claude/settings.local.json` — сотни записей allowlist со старыми путями (безвредны, просто мусор)

См. [[eyepacs-local-dataset]], [[exp4-wsl-launch]], [[master-orchestrator-all-experiments]], [[demo-stack]].
