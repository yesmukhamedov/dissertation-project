"""Rescore finished council runs against the current gold/human references: python work/rescore.py c0 c1 ..."""
import os, sys, collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval import COUNCIL_ITEMS, chrf, body_text, GOLD
from lib import HERE, read
for tag in sys.argv[1:]:
    d = collections.defaultdict(lambda: ([], [], []))
    for item, doc, sl, tl in COUNCIL_ITEMS:
        p = os.path.join(HERE, "work", "eval", tag, "council", f"{item}.{sl}.{tl}.md")
        if not os.path.exists(p):
            continue
        h, g, r = d[f"{sl}>{tl}"]
        h.append(body_text(p)); g.append(read(os.path.join(GOLD, f"{item}.{tl}.md")))
        r.append(read(os.path.join(GOLD, "_draft", f"{item}.ref.{tl}.md")))
    allg = []
    for k, (h, g, r) in d.items():
        print(f"{tag} {k}: chrF_gold {chrf(chr(10).join(h), chr(10).join(g)):.1f}  chrF_human {chrf(chr(10).join(h), chr(10).join(r)):.1f}")
        allg.append(chrf(chr(10).join(h), chr(10).join(g)))
    print(f"{tag} mean chrF_gold {sum(allg)/len(allg):.1f}")
