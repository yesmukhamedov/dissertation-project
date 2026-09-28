import pathlib,re
L={'kk':('Жарияланған','және т.б.','ҒЖБССҚК','Төменде (курсив)'),
   'ru':('Опубликовано','и др.','КОКСНВО','Внизу (курсив)'),
   'en':('Published','et al.','KOKSNVO','Bottom (italic)')}
def ref(r,l):
    lab,etal,nat,_=L[l]
    return {'eejet':'Sapakova S., Yesmukhamedov N., Sapakov A. // Eastern-European J. of Enterprise Technologies, 2025 [Scopus Q3]',
     'procedia':f'Sapakova S., Yesmukhamedov N. {etal} // Procedia Computer Science, 2025 (DS-2025, Istanbul) [Scopus]',
     'kbtu':f'Yesmukhamedov N.S. {etal} // Herald of KBTU, 2025 [{nat}]',
     'nan':f'Yesmukhamedov N.S. {etal} // News of NAN RK, 2025 [{nat}]',
     'kazutb':f'Sapakova S.Z. {etal} // Вестник КазУТБ, 2025 [{nat}]'}[r]
MAP={'05-review':('kazutb','разд. 1.1 — лазерная модель'),
     '15-clahe':('eejet','статья — повышение качества снимка: resize, CLAHE, нормализация'),
     '16-aug-rotation':('procedia','доклад на DS-2025 (Стамбул) — аугментации и нормализация на APTOS'),
     '19-normalization':('kbtu','статья — тот же эксперимент, что Procedia: аугментации и нормализация'),
     '29-screening-system':('nan','статья — архитектура информационной системы (гл. 4)')}
FOOT=re.compile(r'^\*\*(?:Төменде|Внизу|Bottom) \((?:курсив|italic)\):\*\* \*.+\*\n\n',re.M)
SEC=re.compile(r'\n## Апробация на слайде \(2026-09-28, правило докторанта\)\n.*\Z',re.S)
for d in sorted(p for p in pathlib.Path('.').iterdir() if p.is_dir()):
    for l in L:
        p=d/f'{l}.md';x=FOOT.sub('',p.read_text(encoding='utf-8'))
        if d.name in MAP:
            x=x.replace('## Речь',f'**{L[l][3]}:** *{L[l][0]}: {ref(MAP[d.name][0],l)}*\n\n## Речь',1)
        p.write_text(x,encoding='utf-8')
    a=d/'analysis.md';y=SEC.sub('',a.read_text(encoding='utf-8')).rstrip()+'\n'
    if d.name in MAP:
        y+=('\n## Апробация на слайде (2026-09-28, правило докторанта)\n'
            f'Внизу курсивом — одна работа: **{MAP[d.name][0]}** ({MAP[d.name][1]}). Правило: каждая апробация — хотя бы на одном слайде,\n'
            'на слайде — не больше одной (2–3 — перебор). Раскладка — `TODO.md` §2; проверка — `report/build.py`.\n')
    a.write_text(y,encoding='utf-8')
print('ok')
