"""One-off: rewrite the figure line (line 15, «На слайде») of slides 06–29, R1 in kk/ru/en for the new figures,
and the titles / speech of slides 17–18. Run from defense/presentation/slides."""
from pathlib import Path

L = {
"06-system-architecture": (
 "Сурет: модель — 𝒫 + CNN композициясы, Grad-CAM → ALO, екі көз → пациент бойынша шешім (`img/model_kk.png`)",
 "Рисунок: модель как композиция 𝒫 + CNN, Grad-CAM → ALO, два глаза → решение по пациенту (`img/model_ru.png`)",
 "Figure: the model as the composition 𝒫 + CNN, Grad-CAM → ALO, two eyes → patient-level decision (`img/model_en.png`)"),
"07-factorial-design": (
 "Суретсіз: слайдтың негізгі элементі — 2 × 2 кесте (4 арналы бірінші қабат — 06-слайдтың суретінде)",
 "Без рисунка: главный элемент — таблица 2 × 2 (4-канальный первый слой — на рисунке сл. 06)",
 "No figure: the 2 × 2 table is the main element (the 4-channel first layer is on the figure of slide 06)"),
"08-datasets": (
 "Сурет: жоғарыда — ДР 0–4 дәрежелерінің мысалдары, төменде — бес дәрежелі корпустардағы дәрежелер үлесі (`img/datasets_kk.png`)",
 "Рисунок: сверху — примеры степеней ДР 0–4, снизу — доли степеней в пятистепенных корпусах (`img/datasets_ru.png`)",
 "Figure: top — examples of DR grades 0–4, bottom — grade shares in the five-grade corpora (`img/datasets_en.png`)"),
"09-cameras": (
 "Сурет: екі сақиналы диаграмма — Орталық Азия клиникаларындағы және оқыту корпустарындағы камера брендтері, астында дереккөз ескертпесі (`img/cameras_kk.png`)",
 "Рисунок: две кольцевые диаграммы — бренды камер в клиниках Центральной Азии и в обучающих корпусах, под ними примечание об источнике (`img/cameras_ru.png`)",
 "Figure: two donut charts — camera brands in Central Asian clinics and in the training corpora, with a source note below (`img/cameras_en.png`)"),
"10-datasets-experiments": (
 "Сурет: 7 эксперимент × 8 корпус матрицасы; көк — оқыту, жасыл — қайта оқытусыз тексеру (`img/matrix_kk.png`)",
 "Рисунок: матрица 7 экспериментов × 8 корпусов; синий — обучение, зелёный — проверка без дообучения (`img/matrix_ru.png`)",
 "Figure: matrix of 7 experiments × 8 corpora; blue — training, green — evaluation without fine-tuning (`img/matrix_en.png`)"),
"11-pipeline-overview": (
 "Сурет: бір көз (DR03, сол) 8 кезеңнің бәрінен өтеді — конвейер лентасы, топтар түспен белгіленген (`img/strip_kk.png`)",
 "Рисунок: один глаз (DR03, левый) проходит все 8 этапов — лента конвейера, группы выделены цветом (`img/strip_ru.png`)",
 "Figure: one eye (DR03, left) through all 8 stages — the pipeline strip, groups colour-coded (`img/strip_en.png`)"),
"12-canonical-flip": (
 "Сурет: сол көз — кіріс (диск сол жақта) және айналдырудан кейін (диск оң жақта) (`img/flip_kk.png`)",
 "Рисунок: левый глаз — вход (диск слева) и после отражения (диск справа) (`img/flip_ru.png`)",
 "Figure: the left eye — input (disc on the left) and after the flip (disc on the right) (`img/flip_en.png`)"),
"13-od-fovea-rotation": (
 "Сурет: табылған оптикалық диск пен фовеа және ось ортасы бойынша бұрылған кескін, θ = 8,2° (`img/rotation_kk.png`)",
 "Рисунок: найденные диск и фовеа и снимок, повёрнутый вокруг середины оси, θ = 8,2° (`img/rotation_ru.png`)",
 "Figure: the detected disc and fovea and the image rotated about the midpoint of the axis, θ = 8.2° (`img/rotation_en.png`)"),
"14-crop-fov-mask": (
 "Сурет: базалық созу (көз түбі — эллипс) · 2-кезең — изотропты кесу · 3-кезең — көру алаңының маскасы (`img/crop_kk.png`)",
 "Рисунок: растяжение базовой конфигурации (глазное дно — эллипс) · этап 2 — изотропная обрезка · этап 3 — маска поля зрения (`img/crop_ru.png`)",
 "Figure: the baseline stretch (the fundus becomes an ellipse) · stage 2 — isotropic crop · stage 3 — FOV mask (`img/crop_en.png`)"),
"15-clahe": (
 "Сурет: кесуден кейін → 4-кезең, жарықтандыруды түзету (σ = 0,07·D) → 5-кезең, CLAHE (`img/stages45_kk.png`)",
 "Рисунок: после обрезки → этап 4, коррекция освещённости (σ = 0,07·D) → этап 5, CLAHE (`img/stages45_ru.png`)",
 "Figure: after cropping → stage 4, flat-field correction (σ = 0.07·D) → stage 5, CLAHE (`img/stages45_en.png`)"),
"16-aug-rotation": (
 "Сурет: диск пен фовеа орнының белгісіздігі · +σ бұру мысалы · бұрыш таралуы: бейімделгіш σ = 9,1° және резервтік σ = 13°, шек ±40° (`img/aug_rotation_kk.png`)",
 "Рисунок: неопределённость положения диска и фовеа · пример поворота на +σ · распределение угла: адаптивная σ = 9,1° против резервной 13°, граница ±40° (`img/aug_rotation_ru.png`)",
 "Figure: uncertainty of the disc and fovea positions · a sample rotated by +σ · angle distribution: adaptive σ = 9.1° vs fallback 13°, clip ±40° (`img/aug_rotation_en.png`)"),
"17-aug-geometric": (
 "Сурет: масштаб 0,9 / 1,1 және қисайту ±2° — шеткі мысалдар (үзік сызық — бастапқы көру алаңы) және үлестірімдер (`img/aug_geometric_kk.png`)\n\n"
 "Параметрлер: масштаб — лог-біркелкі [0,9; 1,1], созу [1/1,05; 1,05]; қисайту — біркелкі [−2°; 2°], p = 0,3",
 "Рисунок: масштаб 0,9 / 1,1 и скос ±2° — крайние примеры (пунктир — исходное поле зрения) и распределения (`img/aug_geometric_ru.png`)\n\n"
 "Параметры: масштаб — лог-равномерно [0,9; 1,1], растяжение [1/1,05; 1,05]; скос — равномерно [−2°; 2°], p = 0,3",
 "Figure: zoom 0.9 / 1.1 and shear ±2° — extreme samples (dashed — the original field of view) and distributions (`img/aug_geometric_en.png`)\n\n"
 "Parameters: zoom — log-uniform [0.9, 1.1], stretch [1/1.05, 1.05]; shear — uniform [−2°, 2°], p = 0.3"),
"18-aug-photometric": (
 "Сурет: бастапқы · түс ауытқуы ең аз / ең көп · шу + JPEG (×4 үлкейтілген) (`img/aug_photometric_kk.png`)\n\n"
 "Параметрлер: жарықтық, контраст, қанықтық ×[0,9; 1,1], реңк ±0,02 (әрқайсысы p = 0,5); шу σ = 2–6 (p = 0,15); JPEG q = 70–100 (p = 0,2)",
 "Рисунок: исходный · цветовые искажения мин. / макс. · шум + JPEG (увеличено ×4) (`img/aug_photometric_ru.png`)\n\n"
 "Параметры: яркость, контраст, насыщенность ×[0,9; 1,1], оттенок ±0,02 (каждое с p = 0,5); шум σ = 2–6 (p = 0,15); JPEG q = 70–100 (p = 0,2)",
 "Figure: original · colour jitter min / max · noise + JPEG (4× zoom) (`img/aug_photometric_en.png`)\n\n"
 "Parameters: brightness, contrast, saturation ×[0.9, 1.1], hue ±0.02 (each p = 0.5); noise σ = 2–6 (p = 0.15); JPEG q = 70–100 (p = 0.2)"),
"19-normalization": (
 "Сурет: желі кірісі — 4 × 512 × 512 тензоры: нормаланған R, G, B және маска; x′_c = (x_c − μ_c) / σ_c (`img/normalize_kk.png`)",
 "Рисунок: вход сети — тензор 4 × 512 × 512: нормализованные R, G, B и маска; x′_c = (x_c − μ_c) / σ_c (`img/normalize_ru.png`)",
 "Figure: the network input — a 4 × 512 × 512 tensor: normalised R, G, B and the mask; x′_c = (x_c − μ_c) / σ_c (`img/normalize_en.png`)"),
"20-training-metrics": (
 "Сурет: focal loss (γ = 2 және кросс-энтропия) және пациент деңгейіндегі 5 фолд (`img/training_kk.png`)\n\n"
 "- Метрикалар: салмақталған F1 (негізгі), AUC, квадраттық κ\n- Сыртқы корпустарда: G = F1_сыртқы / F1_EyePACS (шек 0,85); назар: ALO = |A ∩ L| / |L|",
 "Рисунок: focal loss (γ = 2 против кросс-энтропии) и 5 фолдов на уровне пациента (`img/training_ru.png`)\n\n"
 "- Метрики: взвешенный F1 (основная), AUC, квадратичная κ\n- На внешних корпусах: G = F1_внеш / F1_EyePACS (порог 0,85); внимание: ALO = |A ∩ L| / |L|",
 "Figure: focal loss (γ = 2 vs cross-entropy) and 5 patient-level folds (`img/training_en.png`)\n\n"
 "- Metrics: weighted F1 (primary), AUC, quadratic κ\n- On external corpora: G = F1_ext / F1_EyePACS (threshold 0.85); attention: ALO = |A ∩ L| / |L|"),
"21-exp1": (
 "Сурет: сол жақта — төрт конфигурацияның салмақталған F1-і (A–D, 5 фолд бойынша SD); оң жақта — EfficientNet-B3, ДР дәрежелері бойынша F1 (`img/exp1_kk.png`)",
 "Рисунок: слева — взвешенный F1 четырёх конфигураций (A–D, SD по 5 фолдам); справа — EfficientNet-B3, F1 по степеням ДР (`img/exp1_ru.png`)",
 "Figure: left — weighted F1 of the four configurations (A–D, SD over 5 folds); right — EfficientNet-B3, F1 by DR grade (`img/exp1_en.png`)"),
"22-exp2": (
 "Сурет: сол жақта — кезеңдерді кезекпен қосу (каскад, Δ п.п.); оң жақта — CLAHE оптимумы (клип-фактор 2,5, шек 0,03) және жарықтандыруды түзету (σ/D = 0,07) (`img/exp2_kk.png`)",
 "Рисунок: слева — этапы добавляются по очереди (каскад, Δ п.п.); справа — оптимум CLAHE (клип-фактор 2,5, порог 0,03) и коррекции освещённости (σ/D = 0,07) (`img/exp2_ru.png`)",
 "Figure: left — stages added one at a time (waterfall, Δ pp); right — optimum of CLAHE (clip factor 2.5, threshold 0.03) and of flat-field (σ/D = 0.07) (`img/exp2_en.png`)"),
"23-domain-distance": (
 "Сурет: алты корпусқа дейінгі MMD — базалық және интеграцияланған; оң жақта Δd [95 % СА] және KL азаюы (`img/domain_kk.png`)",
 "Рисунок: MMD до шести корпусов — базовая и интегрированная; справа Δd [95 % ДИ] и снижение KL (`img/domain_ru.png`)",
 "Figure: MMD to six corpora — baseline and integrated; at the right Δd [95 % CI] and the KL reduction (`img/domain_en.png`)"),
"24-exp3": (
 "Сурет: EyePACS және APTOS 2019-дағы салмақталған F1; жалпылау қатынасы G, шек 0,85 (`img/exp3_kk.png`)",
 "Рисунок: взвешенный F1 на EyePACS и APTOS 2019; коэффициент обобщения G, порог 0,85 (`img/exp3_ru.png`)",
 "Figure: weighted F1 on EyePACS and APTOS 2019; generalisation ratio G, threshold 0.85 (`img/exp3_en.png`)"),
"25-exp4": (
 "Суреттер: сол жақта — зақымдану түрлері бойынша ALO және ALO анықтамасы (`img/exp4_kk.png`); оң жақта — Grad-CAM салыстыру (`img/a27_2.png` — ⚠ ескі прогон, Config D чекпойнтынан қайта түсіру керек)",
 "Рисунки: слева — ALO по типам поражений и определение ALO (`img/exp4_ru.png`); справа — сравнение Grad-CAM (`img/a27_2.png` — ⚠ старый прогон, снять заново с чекпойнта Config D)",
 "Figures: left — ALO by lesion type and the ALO definition (`img/exp4_en.png`); right — Grad-CAM comparison (`img/a27_2.png` — ⚠ old run, re-capture from the Config D checkpoint)"),
"26-exp5": (
 "Сурет: IDRiD және Messidor-2-дағы салмақталған F1, Δ және 95 % СА; MCID = 0,05 (`img/exp5_kk.png`)",
 "Рисунок: взвешенный F1 на IDRiD и Messidor-2, Δ и 95 % ДИ; MCID = 0,05 (`img/exp5_ru.png`)",
 "Figure: weighted F1 on IDRiD and Messidor-2, Δ and 95 % CI; MCID = 0.05 (`img/exp5_en.png`)"),
"27-exp6": (
 "Сурет: бес камера тобы бойынша салмақталған F1 және топтар арасындағы шашырау (`img/exp6_kk.png`)",
 "Рисунок: взвешенный F1 по пяти группам камер и разброс между группами (`img/exp6_ru.png`)",
 "Figure: weighted F1 by the five camera groups and the spread between groups (`img/exp6_en.png`)"),
"28-exp7": (
 "Сурет: IDRiD, 5 фолд және қазақстандық клиникалық іріктеме (n = 60): салмақталған F1, жұптасқан Δ және 95 % СА (`img/exp7_kk.png`)",
 "Рисунок: IDRiD, 5 фолдов и казахстанская клиническая выборка (n = 60): взвешенный F1, парная Δ и 95 % ДИ (`img/exp7_ru.png`)",
 "Figure: IDRiD, 5 folds and the Kazakhstani clinical hold-out (n = 60): weighted F1, paired Δ and 95 % CI (`img/exp7_en.png`)"),
"29-screening-system": (
 "Суреттер: сол жақта — жүйе сызбасы: дәрігер ↔ браузер клиенті ↔ шығару сервисі (𝒫 → CNN → Grad-CAM) (`img/system_kk.png`); оң жақта — браузер клиентінің екі скриншоты: (а) дәреже, класс ықтималдықтары және Grad-CAM; (б) алдын ала өңдеу кезеңдері (`img/ui_1_kk.png`, `img/ui_2_kk.png` — ⚠ жаңа демодан түсіру керек)",
 "Рисунки: слева — схема системы: врач ↔ браузерный клиент ↔ сервис вывода (𝒫 → CNN → Grad-CAM) (`img/system_ru.png`); справа — два скриншота браузерного клиента: (а) степень, вероятности классов и Grad-CAM; (б) этапы предобработки (`img/ui_1_ru.png`, `img/ui_2_ru.png` — ⚠ снять с актуального демо)",
 "Figures: left — system diagram: doctor ↔ browser client ↔ inference service (𝒫 → CNN → Grad-CAM) (`img/system_en.png`); right — two screenshots of the browser client: (a) grade, class probabilities and Grad-CAM; (b) preprocessing stages (`img/ui_1_en.png`, `img/ui_2_en.png` — ⚠ to be captured from the current demo)"),
"R1-limitations": (
 "Сурет: EfficientNet-B3, ДР дәрежелері бойынша F1 (`img/perclass_kk.png`); DR0 жалған позитив мысалы Grad-CAM-мен — ⚠ Config D-ден 25-слайдпен бірге түсіру керек",
 "Рисунок: EfficientNet-B3, F1 по степеням ДР (`img/perclass_ru.png`); пример ложноположительного DR0 с Grad-CAM — ⚠ снять с Config D вместе со сл. 25",
 "Figure: EfficientNet-B3, F1 by DR grade (`img/perclass_en.png`); a DR0 false-positive example with Grad-CAM — ⚠ capture from Config D together with slide 25"),
}

TITLE = {
 "17-aug-geometric": ("Аугментация: масштабтау (scale) және ығыстыру (shear)", "Аугментация: масштаб и скос", "Augmentation: scale and shear"),
 "18-aug-photometric": ("Аугментация: түс, жарықтық, контраст, шу", "Аугментация: цвет, яркость, контраст, шум", "Augmentation: colour, brightness, contrast, noise"),
}
SPEECH = {
 "17-aug-geometric": (
  ("Оқыту кезінде кескін кездейсоқ жылжытылады, масштабталады және ығыстырылады.", "Оқыту кезінде кескін кездейсоқ масштабталады, сәл созылады және ығыстырылады."),
  ("При обучении снимок случайно сдвигается, масштабируется и скашивается.", "При обучении снимок случайно масштабируется, слегка растягивается и скашивается."),
  ("In training the image is randomly translated, scaled and sheared.", "In training the image is randomly scaled, slightly stretched and sheared.")),
 "18-aug-photometric": (
  ("торқабықтың құрылымдық белгілеріне сүйенуге үйренеді.", "торқабықтың құрылымдық белгілеріне сүйенуге үйренеді. Сонымен қатар аз ықтималдықпен шу мен JPEG сығу қосылады — арзан камерамен түсіргендегі және кескінді желі арқылы бергендегідей."),
  ("опираться не на цвет, а на структурные признаки сетчатки.", "опираться не на цвет, а на структурные признаки сетчатки. Кроме того, с небольшой вероятностью добавляются шум и сжатие JPEG — как при съёмке недорогой камерой и передаче снимка по сети."),
  ("rely not on colour but on the structural features of the retina.", "rely not on colour but on the structural features of the retina. In addition, noise and JPEG compression are added with a small probability — as with an inexpensive camera and an image sent over a network.")),
}

for d, lines in L.items():
    for lang, new in zip(("kk", "ru", "en"), lines):
        p = Path(d) / f"{lang}.md"
        rows = p.read_text(encoding="utf-8").split("\n")
        assert rows[14].startswith(("Сурет", "Рисун", "Figure", "Figures")), (p, rows[14])
        rows[14] = new
        text = "\n".join(rows)
        if d in TITLE:
            old_t = next(r for r in rows if r.startswith("# "))
            text = text.replace(old_t, "# " + TITLE[d][("kk", "ru", "en").index(lang)], 1)
        if d in SPEECH:
            a, b = SPEECH[d][("kk", "ru", "en").index(lang)]
            assert a in text, (p, a)
            text = text.replace(a, b, 1)
        p.write_text(text, encoding="utf-8")
print("ok", len(L))
