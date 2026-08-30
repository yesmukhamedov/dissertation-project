---
name: quarantine-cleanup
description: Хроника чистки 2026-08-12 — что вынесено в D:\удаленные (каталог утрачен при переезде 2026-08-30), что проверено безопасным и что осознанно оставлено в проекте
metadata:
  type: project
---

2026-08-12 из корня проекта (тогда `D:\dissertation-project`) вынесены (НЕ удалены) архивные, дублирующие и
пересоздаваемые файлы → **`D:\удаленные`** (1 075 файлов, ~1.06 ГБ). Путь внутри карантина
зеркалит путь в проекте; внутри лежат `_МАНИФЕСТ.md` (что и почему), `_files_index.txt`
(каждый файл + исходный путь), `_manifest.csv/.json` и `restore.ps1` (`-All` / `-Path <rel>` /
`-List` / `-WhatIf`). 628 позиций были под git — в `git status` показаны как удаления, не закоммичены.

**Вынесено:** кэши (`__pycache__` ×29, `.pytest_cache` ×3, `.wrangler` ×2, office-локи `~$*`);
`.archive/`, `.preserved_from_D/`, `.sync_manifests/`; `defense/presentation/archive/`;
`defense/presentation/assets/presentation/` (проверено хешами — 96/96 байт-в-байт дубли `assets/`);
`demo/web/public/images/` (321 МБ, зеркало `pipeline`+`results`+`diagrams`, ноль ссылок из `web/src`,
в `build/` не копируется); `demo/server/checkpoints/*.APTOS_TEST.*.bak`; `thesis/assembly/_tmp_body/`;
`defense/presentation/scripts/_tmp_preproc/`; закрытые задачники `demo/TASK.md` и
`demo/web/public/diagrams/TASK.md`.

**Проверено и осознанно ОСТАВЛЕНО** (не предлагать повторно):
`results/TODO_BEFORE_WRITING.md` — не временный мусор, **открыт** (NEW-1 / G-3 / S0);
`thesis/chapters/**/drafts/` — часть конвейера brief→draft→review, не «черновики на выброс»;
`thesis/assembly/DISSERTATION_*_2026-06-17.md` — в них проставлены цитаты, в `*_2026-08-11.md` нет;
`defense/docs/DISSERTATION_*` vs `FULL_DISSERTATION_*` — сверено хешами, это **разные** документы;
`demo/web/public/pipeline/TASKS.md` — справочник, на который ссылается `helpers/README.md`;
`ROADMAP.md` — статусы устарели относительно [[results-knowledge-base]], но файл живой (обновлять, не выносить).

**Крупные кандидаты, оставленные по решению кандидата** (проект остаётся ~110 ГБ; всё в
`experiments/outputs/`): `epoch_*.pt` — 50.3 ГБ / 302 файла (`best_model.pt` и `last_checkpoint.pt`
есть во всех 72 папках); `ssl_run_artifacts/` 10.7 ГБ (дубли весов, живые — в `outputs/ssl/`);
`last_checkpoint.pt` 10.9 ГБ; `cache_512.tar` 9.3 ГБ + `.tar.part` 5.6 ГБ; `_smoke*` 4.8 ГБ;
`ssl/ssl_cache_256.tar` 3.8 ГБ; `exp2_baseline_partial_pc1_20260716` 2.6 ГБ; `kaggle_config_d*` 0.9 ГБ.

⚠️ **2026-08-30, после переезда проекта в `D:\phd\dissertation`: каталога `D:\удаленные` на диске больше нет.** Карантин лежал вне репозитория и перенос не пережил — восстановить вынесенные файлы через `restore.ps1` уже нельзя. Всё, что было под git, восстанавливается из истории; остальное считать утраченным. Карточка сохранена как хроника решений (что осознанно оставлено и почему), а не как указатель на существующий каталог. См. [[project-relocation-d-phd]], [[eyepacs-local-dataset]].
