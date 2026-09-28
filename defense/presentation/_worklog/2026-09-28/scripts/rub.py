import re,glob,os
out=[]
for d in sorted(glob.glob('A*')):
    f=os.path.join(d,'Презентация','00_Слайды_по_порядку.txt')
    if not os.path.exists(f): continue
    t=open(f,encoding='utf-8').read()
    lang=re.search(r'Защита: [^,]*, (\S+)',t); lang=lang.group(1) if lang else '?'
    rubs=re.findall(r'=== Слайд (\d+).*?===\nРубрика: (.*)\n',t)
    seq=[];prev=None
    for n,r in rubs:
        r=r.strip()
        if seq and seq[-1][0]==r: seq[-1][1]+=1
        else: seq.append([r,1])
    s=' → '.join(f"{r}×{c}" if c>1 else r for r,c in seq)
    out.append(f"{d[:3]} {d[4:14]} ({lang}, {len(rubs)} сл.): {s}")
print('\n'.join(out))
