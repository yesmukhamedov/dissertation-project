# Council — PhD defense knowledge base (8D061, IITU/МУИТ)

*Bilingual index · Двуязычный указатель — [Русский](#ru) · [English](#en)*

---

<a name="ru"></a>
## 🇷🇺 Русский

Набор связанных шаблонов и инструкций по подготовке документов для защиты докторской
диссертации (PhD) в диссертационном совете при АО «МУИТ» по направлению
**8D061 — Информационно-коммуникационные технологии**.

**Назначение:** когда нужно подготовить любой документ защиты (отзыв, автореферат,
объявление, заключение и т. д.) — берём **точную структуру и оформление, прописанные
в этом университете**, а не международные/общие шаблоны. Это шаблоны и инструкции,
а не литературные карточки: описание структуры и содержания без привязки к авторам и темам.

Русская версия: **[`ru/`](ru/)** · English version: **[`en/`](en/)**

**Метаданные защиты — [`METADATA.toml`](METADATA.toml).** Единственное место, где
хранятся Ф.И.О., должности, e-mail, ORCID, кафедра, код и название ОП, тема на трёх
языках, объём тома и список публикаций. Шаблоны ниже обезличены и значений не содержат;
готовые документы берут их из реестра. Сверка документов с реестром:
`python .claude/skills/council-docs/scripts/check_metadata.py`.

### Нормативная база и процесс
| Файл | О чём |
|------|-------|
| [ru/00-нормативная-база/законы-и-положения.md](ru/00-нормативная-база/законы-и-положения.md) | Законы, приказы, стандарты, органы |
| [ru/00-нормативная-база/положение-о-диссовете.md](ru/00-нормативная-база/положение-о-диссовете.md) | Положение Р-39 (11 разделов + 5 форм) |
| [ru/00-нормативная-база/состав-диссовета.md](ru/00-нормативная-база/состав-диссовета.md) | Роли и нормы формирования совета |
| [ru/00-нормативная-база/требования-к-публикациям.md](ru/00-нормативная-база/требования-к-публикациям.md) | WoS/Scopus, ККСОН, порог ≥25, антиплагиат |
| [ru/00-нормативная-база/перечень-изданий-кксон.md](ru/00-нормативная-база/перечень-изданий-кксон.md) | Рекомендованные журналы (профиль 8D061) |
| [ru/01-процесс-защиты/жизненный-цикл-защиты.md](ru/01-процесс-защиты/жизненный-цикл-защиты.md) | Маршрут защиты + карта документов |
| [ru/01-процесс-защиты/предварительная-экспертиза.md](ru/01-процесс-защиты/предварительная-экспертиза.md) | Предзащита |
| [ru/01-процесс-защиты/регламент-заседания.md](ru/01-процесс-защиты/регламент-заседания.md) | Повестка защиты (§7.7) |
| [ru/01-процесс-защиты/онлайн-заседание.md](ru/01-процесс-защиты/онлайн-заседание.md) | Дистанционная защита (видеоконференция) |
| [ru/01-процесс-защиты/голосование-и-апелляция.md](ru/01-процесс-защиты/голосование-и-апелляция.md) | Голосование ≥3/4, апелляция |
| [ru/01-процесс-защиты/материалы-на-сайте.md](ru/01-процесс-защиты/материалы-на-сайте.md) | Публикуемые материалы (§6.9) |
| [ru/02-оформление/оформление-по-госту.md](ru/02-оформление/оформление-по-госту.md) | ГОСТ: поля, шрифт, объём |

### Шаблоны документов
| Документ | Файл |
|----------|------|
| Диссертация | [ru/10-диссертация/структура.md](ru/10-диссертация/структура.md) — обязательные элементы; измеренные по 16 образцам нормы объёма и числа слов, архитектуры глав, глубины заголовков, рубрик введения, длины абзаца и предложения, оформления (без §) и приложений: [нормы-по-образцам.md](ru/10-диссертация/нормы-по-образцам.md) |
| Автореферат / аннотация | [ru/11-автореферат-аннотация/структура.md](ru/11-автореферат-аннотация/структура.md) |
| Объявление о защите | [ru/12-объявление-извещение/структура.md](ru/12-объявление-извещение/структура.md) |
| Отзыв научного консультанта | [ru/13-отзыв-научного-консультанта/структура.md](ru/13-отзыв-научного-консультанта/структура.md) |
| Отзыв иностранного консультанта | [ru/14-отзыв-иностранного-консультанта/структура.md](ru/14-отзыв-иностранного-консультанта/структура.md) |
| Отзыв официального рецензента | [ru/15-отзыв-официального-рецензента/структура.md](ru/15-отзыв-официального-рецензента/структура.md) |
| Рецензия | [ru/16-рецензия/структура.md](ru/16-рецензия/структура.md) |
| Заключение этической комиссии | [ru/17-заключение-этической-комиссии/структура.md](ru/17-заключение-этической-комиссии/структура.md) |
| Список научных трудов | [ru/18-список-научных-трудов/структура.md](ru/18-список-научных-трудов/структура.md) |
| Сведения о докторанте | [ru/19-сведения-о-докторанте/структура.md](ru/19-сведения-о-докторанте/структура.md) |
| Явочный лист | [ru/20-явочный-лист/структура.md](ru/20-явочный-лист/структура.md) |
| Отчёт о работе диссовета | [ru/21-отчет-о-работе-диссовета/структура.md](ru/21-отчет-о-работе-диссовета/структура.md) |
| Протокол расширенного заседания кафедры (предзащита) | [en/22-extended-meeting-protocol/structure.md](en/22-extended-meeting-protocol/structure.md) — нормы и жанр; бланк-скелет [template.md](en/22-extended-meeting-protocol/template.md), что писать по нашей теме [content-brief.md](en/22-extended-meeting-protocol/content-brief.md), банк вопросов [qa-bank.md](en/22-extended-meeting-protocol/qa-bank.md) |

### Образовательные программы 8D061
8D06101 — Интеллектуальные системы · 8D06102 — Компьютерная и программная инженерия ·
6D070300/8D06103 — Информационные системы · 8D06105 — Наука о данных

### Принцип анонимности
Все файлы содержат **только структуру, оформление и нормативные правила**. Имена соискателей,
консультантов, рецензентов и конкретные темы намеренно **не приводятся** — вместо них `<...>`.

---

<a name="en"></a>
## 🇬🇧 English

A set of linked templates and instructions for preparing the documents required to defend
a PhD dissertation before the dissertation council of IITU («МУИТ») in the field
**8D061 — Information and Communication Technologies**.

**Purpose:** whenever a defense document is needed (review, abstract, announcement,
conclusion, etc.), use the **exact structure and formatting prescribed at this university**
rather than international/generic templates. These are templates and instructions, not
literature cards: structure and content descriptions with no reference to specific authors or topics.

Russian version: **[`ru/`](ru/)** · English version: **[`en/`](en/)**

**Defense metadata — [`METADATA.toml`](METADATA.toml).** The single place holding
names, positions, e-mail, ORCID, the department, the programme code and name, the
dissertation titles in three languages, the volume figures and the publication list.
The templates below stay anonymised; the finished documents draw their values from
the registry. Verify documents against it:
`python .claude/skills/council-docs/scripts/check_metadata.py`.

### Regulatory framework & process
| File | About |
|------|-------|
| [en/00-regulatory-framework/laws-and-regulations.md](en/00-regulatory-framework/laws-and-regulations.md) | Laws, orders, standards, bodies |
| [en/00-regulatory-framework/council-statute.md](en/00-regulatory-framework/council-statute.md) | Statute R-39 (11 sections + 5 forms) |
| [en/00-regulatory-framework/council-composition.md](en/00-regulatory-framework/council-composition.md) | Roles and formation rules |
| [en/00-regulatory-framework/publication-requirements.md](en/00-regulatory-framework/publication-requirements.md) | WoS/Scopus, KKSON, ≥25 threshold, plagiarism |
| [en/00-regulatory-framework/kkson-journal-list.md](en/00-regulatory-framework/kkson-journal-list.md) | Recommended journals (8D061 profile) |
| [en/01-defense-process/defense-lifecycle.md](en/01-defense-process/defense-lifecycle.md) | Defense roadmap + document map |
| [en/01-defense-process/preliminary-review.md](en/01-defense-process/preliminary-review.md) | Pre-defense |
| [en/01-defense-process/session-procedure.md](en/01-defense-process/session-procedure.md) | Defense agenda (§7.7) |
| [en/01-defense-process/online-session.md](en/01-defense-process/online-session.md) | Remote defense (videoconference) |
| [en/01-defense-process/voting-and-appeal.md](en/01-defense-process/voting-and-appeal.md) | Voting ≥3/4, appeal |
| [en/01-defense-process/materials-published-online.md](en/01-defense-process/materials-published-online.md) | Published materials (§6.9) |
| [en/02-formatting/gost-formatting.md](en/02-formatting/gost-formatting.md) | GOST: margins, font, length |

### Document templates
| Document | File |
|----------|------|
| Dissertation | [en/10-dissertation/structure.md](en/10-dissertation/structure.md) — mandatory elements; measured norms across the 16 samples — volume and word count, chapter architecture, heading depth, Introduction rubrics, paragraph/sentence length, typography (no §), appendices: [peer-norms.md](en/10-dissertation/peer-norms.md) |
| Abstract / annotation | [en/11-abstract-annotation/structure.md](en/11-abstract-annotation/structure.md) |
| Defense announcement | [en/12-defense-announcement/structure.md](en/12-defense-announcement/structure.md) |
| Scientific supervisor review | [en/13-supervisor-review/structure.md](en/13-supervisor-review/structure.md) |
| Foreign consultant review | [en/14-foreign-consultant-review/structure.md](en/14-foreign-consultant-review/structure.md) |
| Official reviewer report | [en/15-official-reviewer-report/structure.md](en/15-official-reviewer-report/structure.md) — norms & genre; the blank Appendix-3 form in EN/RU/KZ is [form-blank.md](en/15-official-reviewer-report/form-blank.md), what each row must say for this dissertation is [content-brief.md](en/15-official-reviewer-report/content-brief.md) |
| Review (free-form) | [en/16-review/structure.md](en/16-review/structure.md) |
| Ethics committee conclusion | [en/17-ethics-committee-conclusion/structure.md](en/17-ethics-committee-conclusion/structure.md) |
| List of scientific papers | [en/18-list-of-publications/structure.md](en/18-list-of-publications/structure.md) |
| Doctoral candidate info | [en/19-doctoral-candidate-info/structure.md](en/19-doctoral-candidate-info/structure.md) |
| Attendance sheet | [en/20-attendance-sheet/structure.md](en/20-attendance-sheet/structure.md) |
| Council annual report | [en/21-council-annual-report/structure.md](en/21-council-annual-report/structure.md) |
| Extended department meeting protocol (pre-defense) | [en/22-extended-meeting-protocol/structure.md](en/22-extended-meeting-protocol/structure.md) — norms & genre; the fill-in skeleton is [template.md](en/22-extended-meeting-protocol/template.md), what each paragraph must say for this dissertation is [content-brief.md](en/22-extended-meeting-protocol/content-brief.md), the question bank is [qa-bank.md](en/22-extended-meeting-protocol/qa-bank.md) |

### 8D061 educational programmes
8D06101 — Intelligent Systems · 8D06102 — Computer and Software Engineering ·
6D070300/8D06103 — Information Systems · 8D06105 — Data Science

### Anonymity principle
All files contain **only structure, formatting and regulatory rules**. Names of candidates,
consultants, reviewers and specific topics are intentionally **omitted** — replaced by `<...>`.
