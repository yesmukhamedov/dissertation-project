---
name: project-relocation-d-phd
description: 2026-08-30 проект переехал на D:\personal\phd\dissertation (диска E: больше нет); карта старых и новых путей, фикс git safe.directory, что ещё осталось стухшим
metadata:
  type: project
---

**2026-10-01 — `D:` вернулся, синхронизирован с `C:\VirtualD`.** Пока диска не было, работа шла в
`C:\VirtualD\personal\phd\dissertation` (замена диска, см. `C:\VirtualD\server\README.md`). Сверка по хешам:
на `D:` ничего не правилось позже снимка, конфликтов нет. Репозиторий на `D:` перемотан fast-forward до `43607c2`,
незакоммиченные правки и новые файлы `C:\VirtualD\{personal,people,tools}` скопированы на `D:` (≈2,3 тыс. файлов
плюс `people\gulsim` целиком, без `node_modules`). Файлы, которые есть только на `D:` (видео, веса, датасеты),
не трогались. **Источник истины снова `D:`**: правим там, `C:\VirtualD` обновляется только как снимок.
Две ловушки при такой сверке: (1) клон с GitHub ставит всем файлам свежие mtime, а `update-from-d.ps1`
сравнивает по времени (robocopy `/XO`), так что сравнивать надо по содержимому; (2) клоны отличаются CRLF/LF,
а git считает файл изменённым при несовпадении размера с индексом, даже если блоб тот же. Лечится
пересборкой индекса (`del .git\index` + `git reset -q`), если в индексе нет подготовленных правок.

**2026-09-28 — внешний SSD с `D:` отвалился посреди работы** (Samsung PSSD T7 Shield, в диспетчере устройств
«Unknown»; в системе остался только `C:`). Репозиторий заново склонирован с GitHub в **`C:\personal\phd\dissertation`**
(`https://github.com/yesmukhamedov/dissertation-project`, та же структура путей, только буква `C:`). Работа продолжена
в клоне; незакоммиченные правки на `D:` (если диск вернётся) сверить с клоном, прежде чем что-то переносить — **не
держать две живые копии**. Бэкап диска `D:` лежит в Google Диске учётки yesmukhamedov.yeskendyr@gmail.com (раздел
«Компьютеры»), подключение Claude к Google Диску — на другой учётке и его не видит. Датасеты (`D:\personal\phd\datasets`)
в клоне недоступны: всё, что читает датасеты, до возврата диска не запустить. Урок: коммитить и пушить в конце каждого
этапа — сегодняшние рисунки уцелели только потому, что были в коммите `cad209b`.

**2026-08-30 проект переехал.** Диска `E:` на этой машине больше нет — всё живёт под `D:\personal\phd\`.
Репозиторий перестал читаться Git'ом до тех пор, пока новый путь не был помечен доверенным.

## Карта путей

| Было | Стало |
|---|---|
| `E:\dissertation-project` → позже `D:\dissertation-project` | `D:\personal\phd\dissertation` |
| `E:\datasets` | `D:\personal\phd\datasets` |
| `E:\dissertation_council` / `D:\dissertation_council` | `D:\personal\phd\council` |
| `/mnt/e/dissertation-project`, `/mnt/d/dissertation-project` | `/mnt/d/personal/phd/dissertation` |
| `/mnt/e/datasets` | `/mnt/d/personal/phd/datasets` |

Датасеты на месте и полные: `APTOS 2019`, `clinical`, `DDR`, `downloaded`, `EyePACS`, `IDRiD`,
`Messidor-2`, `ODIR-5K`, `RFMiD`. Соседи проекта под `D:\personal\phd\`: `council`, `coursework`, `history`.

## Git после переезда

Git отказывался читать репозиторий целиком:

```
fatal: detected dubious ownership in repository at 'D:/personal/phd/dissertation'
```

Из-за этого история выглядела пустой, а изменения — отсутствующими. Лечится один раз на машину:

```
git config --global --add safe.directory D:/personal/phd/dissertation
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
