---
slide: 25
id: training-metrics
lang: kk
status: final
seconds: 30
source: архив сл. 23 — без изменений
terms: [focal_loss, patient_level_cv, weighted_f1, roc_auc, kappa, generalization_ratio, alo]
---

# Оқыту параметрлері: Focal Loss, optimizer, 5-fold CV; Метрикалар: F1, AUC, Cohen's κ, Generalization gap (G), ALO

## На слайде

Суреттер: 5 фолдты бөлу сызбасы, focal loss, F1/κ, AUC, G, ALO анықтамалары (`img/a23_*.png`)

## Речь

Бағалау — пациент деңгейінде стратификацияланған бес фолдты кросс-валидация, сондықтан деректердің ағып кетуі жабылған. Кластар теңгерімсіз, шығын функциясы — кері жиілікпен салмақталған focal loss. Негізгі өлшем — салмақталған F1, одан кейін AUC және квадраттық каппа; сыртқы корпустарда — жалпылау қатынасы G, назарда — ALO.
