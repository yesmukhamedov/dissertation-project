import re,glob,os,sys
sys.stdout.reconfigure(encoding='utf-8')
def nums(t):
    t=re.sub(r'\[[\d,\s–-]+\]','',t)           # refs
    t=re.sub(r'(?m)^\s*[–—\-•]?\s*\d{1,2}[\.\)]\s','',t)  # enumerators
    t=re.sub(r'\b(19|20)\d\d\b','',t)           # years
    return re.findall(r'\d+(?:[.,]\d+)?\s*%?',t)
for d in sorted(glob.glob('A*')):
    f=os.path.join(d,'Введение_по_рубрикам.txt')
    s=open(f,encoding='utf-8').read() if os.path.exists(f) else ''
    m=re.search(r'### Положени[^\n]*\n(.*?)(?=\n### |\Z)',s,re.S)
    intro=m.group(1) if m else ''
    n=nums(intro)
    sl=''
    for p in glob.glob(os.path.join(d,'Презентация','*Положени*.txt')): sl+=open(p,encoding='utf-8').read()
    ns=nums(sl)
    print(f"{d[:18]:18} intro_words={len(intro.split()):4} intro_nums={len(n):2} {' '.join(x.strip() for x in n[:8]):40} | slide={'yes' if sl else 'no '} slide_nums={len(ns)}")
