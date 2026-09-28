"""Name the patient-level rule (worst eye = max of the two grades, demo/server/app/inference.py:150) on slide 06 and
in §4.2 of the volume. Run from the repo root."""
from pathlib import Path

S = "defense/presentation/slides/06-system-architecture/"
T = "thesis/chapters/04-system/"
EDITS = [
 (S + "kk.md", "| 5 | Пациент деңгейі | екі көздің нәтижесі бір пациенттік шешімге біріктіріледі |",
  "| 5 | Пациент деңгейі | пациенттің дәрежесі — нашар көздің дәрежесі: ŷ = max(ŷ_сол, ŷ_оң) |"),
 (S + "ru.md", "| 5 | Уровень пациента | результаты двух глаз объединяются в одно решение по пациенту |",
  "| 5 | Уровень пациента | степень пациента — степень худшего глаза: ŷ = max(ŷ_лев, ŷ_прав) |"),
 (S + "en.md", "| 5 | Patient level | the two eyes' results are combined into one patient decision |",
  "| 5 | Patient level | the patient's grade is the grade of the worse eye: ŷ = max(ŷ_left, ŷ_right) |"),
 (S + "kk.md", "Екі көздің нәтижесі пациент деңгейінде біріктіріледі, ал Grad-CAM назар картасын береді.",
  "Пациенттің дәрежесі — нашар көздің дәрежесі, ал Grad-CAM назар картасын береді."),
 (S + "ru.md", "Результаты двух глаз объединяются на уровне пациента, Grad-CAM строит карту внимания.",
  "Степень пациента — степень худшего глаза, Grad-CAM строит карту внимания."),
 (S + "en.md", "The two eyes are combined at patient level, and Grad-CAM gives the attention map.",
  "The patient's grade is that of the worse eye, and Grad-CAM gives the attention map."),
 (S + "kk.md", "екі көз → пациент бойынша шешім (`img/model_kk.png`)", "екі көз → нашар көздің дәрежесі (`img/model_kk.png`)"),
 (S + "ru.md", "два глаза → решение по пациенту (`img/model_ru.png`)", "два глаза → степень худшего глаза (`img/model_ru.png`)"),
 (S + "en.md", "two eyes → patient-level decision (`img/model_en.png`)", "two eyes → grade of the worse eye (`img/model_en.png`)"),
 (S + "img/make_model.py", r'"pat": "Екі көз →\nпациент бойынша\nшешім"', r'"pat": "Екі көз →\nнашар көздің\nдәрежесі (max)"'),
 (S + "img/make_model.py", r'"pat": "Два глаза →\nрешение\nпо пациенту"', r'"pat": "Два глаза →\nстепень худшего\nглаза (max)"'),
 (S + "img/make_model.py", r'"pat": "Two eyes →\npatient-level\ndecision"', r'"pat": "Two eyes →\ngrade of the\nworse eye (max)"'),
 (S + "img/make_model.py", "The rule that merges the two eyes is not named here — TODO.md §3 (check demo/server before naming it).",
  "Two eyes → the grade of the worse eye (max), as demo/server/app/inference.py:150 and §4.2 of the volume."),
 # §4.2 of the volume, three editions (+6 words EN; main-text headroom was 47)
 (T + "drafts/4.2-draft.md",
  "eyes and returns a result for the patient, which is the unit a referral decision is made about.",
  "eyes and returns the grade of the worse eye as the patient's result, which is the unit a referral\ndecision is made about."),
 (T + "translations/4.2-translation.md",
  "интерфейс екі көздің кескіндерін қабылдап, пациент бойынша\nнәтиже қайтарады,",
  "интерфейс екі көздің кескіндерін қабылдап, нашар көздің\nдәрежесін пациент бойынша нәтиже ретінде қайтарады,"),
 (T + "translations-ru/4.2-ru.md",
  "интерфейс принимает изображения обоих глаз и возвращает результат для пациента,",
  "интерфейс принимает изображения обоих глаз и возвращает степень худшего глаза как результат для пациента,"),
]
for path, old, new in EDITS:
    p = Path(path)
    t = p.read_text(encoding="utf-8")
    assert t.count(old) == 1, (path, t.count(old), old[:50])
    p.write_text(t.replace(old, new), encoding="utf-8")
print("ok", len(EDITS))
