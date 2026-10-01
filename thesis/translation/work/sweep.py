"""Re-check every chunk of the KZ Qwen volume with the current checker: python work/sweep.py [glob]"""
import os, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib import THESIS, read, load_termbase
from check import check
from fix import chunks_of
pat = sys.argv[1] if len(sys.argv) > 1 else "chapters/*/translated-kk-qwen/*-kz.md"
tb = load_termbase()
ne = nw = nc = 0
for out in sorted(glob.glob(os.path.join(THESIS, pat))):
    rep, ch = chunks_of(out)
    genre = rep.get("genre", "thesis")
    t = [r for r in tb if r.get("domain", "all") in ("all", genre)]
    for n, seg, cp in ch:
        nc += 1
        e, w = check(seg, json.loads(read(cp))["out"], rep["src"], rep["tgt"], t, genre)
        ne += len(e); nw += len(w)
        for x in e: print(f"ERR  {os.path.relpath(out, THESIS)} #{n}: {x}")
        for x in w: print(f"warn {os.path.relpath(out, THESIS)} #{n}: {x}")
print(f"chunks {nc}  errors {ne}  warnings {nw}")
