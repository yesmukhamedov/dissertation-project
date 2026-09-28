import pathlib
L={'kk':('Жарияланған','және т.б.','ҒЖБССҚК','Авторлық құқық куәлігі № 78109, 04.09.2026','Төменде (курсив)'),
   'ru':('Опубликовано','и др.','КОКСНВО','Свидетельство об авторском праве № 78109 от 04.09.2026','Внизу (курсив)'),
   'en':('Published','et al.','KOKSNVO','Copyright certificate No. 78109, 04.09.2026','Bottom (italic)')}
def P(l):
    lab,etal,nat,cert,_=L[l]
    return {
    1:f'Sapakova S., Yesmukhamedov N., Sapakov A. // Eastern-European J. of Enterprise Technologies, 2025 [Scopus Q3]',
    2:f'Sapakova S., Yesmukhamedov N. {etal} // Procedia Computer Science, 2025 [Scopus]',
    3:f'Yesmukhamedov N.S. {etal} // Herald of KBTU, 2025 [{nat}]',
    4:f'Yesmukhamedov N.S. {etal} // News of NAN RK, 2025 [{nat}]',
    5:f'Sapakova S.Z. {etal} // Вестник КазУТБ, 2025 [{nat}]',
    'cert':cert}
MAP={'05-review':[5],'06-system-architecture':[1,2,3],
     **{d:[1,2,3] for d in ['11-pipeline-overview','12-canonical-flip','13-od-fovea-rotation','14-crop-fov-mask','15-clahe','16-aug-rotation','17-aug-geometric','18-aug-photometric','19-normalization']},
     '29-screening-system':[4,'cert']}
for d,refs in MAP.items():
    for l in L:
        p=pathlib.Path(d)/f'{l}.md';x=p.read_text(encoding='utf-8')
        if '(курсив)' in x or 'Bottom (italic)' in x: continue
        lab,_,_,_,where=L[l];pp=P(l)
        pubs=[pp[r] for r in refs if r!='cert'];extra=[pp['cert']] if 'cert' in refs else []
        parts=([f'{lab}: '+'; '.join(pubs)] if pubs else [])+extra
        line=f'**{where}:** *'+'. '.join(parts)+'*\n\n'
        assert x.count('## Речь')==1,p
        x=x.replace('## Речь',line+'## Речь',1)
        p.write_text(x,encoding='utf-8')
    a=pathlib.Path(d)/'analysis.md'
    a.write_text(a.read_text(encoding='utf-8').rstrip()+'\n\n## Апробация на слайде (2026-09-28, правило докторанта)\n'
      f'Строка внизу курсивом — публикации, на которые опирается слайд (привязка по введению тома: гл. 2 → EEJET, Procedia, KBTU; '
      f'гл. 4 → NAN RK; разд. 1.1 → КазУТБ); свидетельство № 78109 — на слайде системы; патенты — после выдачи (см. `TODO.md`).\n',encoding='utf-8')
print('ok')
