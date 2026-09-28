import re,pathlib
D={
'ru':('# Общая архитектура модели','# Математическая постановка и архитектура модели',
 '**Центральная идея:** ŷ = CNN_θ(𝒫(I, s)) — 𝒫 неотъемлемая часть выражения',
 '''**Математическая постановка**

- 𝒫 = T₇ ∘ … ∘ T₀ : (I, s) ↦ x ∈ ℝ^(4×512×512)
- ŷ = argmax_k softmax(CNN_θ(𝒫(I, s)))_k, k ∈ {0, …, 4}; направление к врачу: ŷ ≥ 2
- θ* = argmin_θ Σᵢ FL_γ(CNN_θ(𝒫(Iᵢ, sᵢ)), yᵢ), γ = 2 — 𝒫 входит в модель, а не в данные
- ALO = |A ∩ L| / |L|, где A — область внимания Grad-CAM, L — маска поражений''',
 'Входной снимок сначала','Формально модель — композиция: сеть применяется к выходу конвейера и её параметры обучаются на этом выходе, поэтому конвейер входит в определение модели. Входной снимок сначала'),
'kk':('# Модельдің жалпы архитектурасы','# Модельдің математикалық қойылымы және архитектурасы',
 '**Орталық идея:** ŷ = CNN_θ(𝒫(I, s)) — 𝒫 өрнектің ажырамас бөлігі',
 '''**Математикалық қойылым**

- 𝒫 = T₇ ∘ … ∘ T₀ : (I, s) ↦ x ∈ ℝ^(4×512×512)
- ŷ = argmax_k softmax(CNN_θ(𝒫(I, s)))_k, k ∈ {0, …, 4}; дәрігерге жолдама: ŷ ≥ 2
- θ* = argmin_θ Σᵢ FL_γ(CNN_θ(𝒫(Iᵢ, sᵢ)), yᵢ), γ = 2 — 𝒫 деректерге емес, модельге кіреді
- ALO = |A ∩ L| / |L|, мұнда A — Grad-CAM назар аймағы, L — зақымдану маскасы''',
 'Кіріс кескін алдымен','Формалды түрде модель — композиция: желі конвейердің шығысына қолданылады және оның параметрлері сол шығыста оқытылады, сондықтан конвейер модельдің анықтамасына кіреді. Кіріс кескін алдымен'),
'en':('# Overall architecture of the model','# Mathematical formulation and architecture of the model',
 '**Central idea:** ŷ = CNN_θ(𝒫(I, s)) — 𝒫 is an integral part of the expression',
 '''**Mathematical formulation**

- 𝒫 = T₇ ∘ … ∘ T₀ : (I, s) ↦ x ∈ ℝ^(4×512×512)
- ŷ = argmax_k softmax(CNN_θ(𝒫(I, s)))_k, k ∈ {0, …, 4}; referral: ŷ ≥ 2
- θ* = argmin_θ Σᵢ FL_γ(CNN_θ(𝒫(Iᵢ, sᵢ)), yᵢ), γ = 2 — 𝒫 belongs to the model, not to the data
- ALO = |A ∩ L| / |L|, where A is the Grad-CAM attention area and L the lesion mask''',
 'The input image first','Formally the model is a composition: the network is applied to the pipeline output and its parameters are trained on that output, so the pipeline belongs to the definition of the model. The input image first'),
}
for lang,(t0,t1,c0,c1,s0,s1) in D.items():
    p=pathlib.Path(f'{lang}.md'); x=p.read_text(encoding='utf-8')
    for a,b in ((t0,t1),(c0,c1),(s0,s1)):
        assert x.count(a)==1,(lang,a); x=x.replace(a,b)
    x=x.replace('seconds: 35','seconds: 45',1)
    x=re.sub(r'^source: .*$','source: архив сл. 7 — переработан (таблица исправлена, диаграмма та же; добавлена математическая постановка)',x,count=1,flags=re.M)
    x=x.replace('terms: [preprocessing_pipeline,','terms: [preprocessing_pipeline, focal_loss,',1)
    p.write_text(x,encoding='utf-8')
print('ok')
