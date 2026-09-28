import csv, io
from pathlib import Path
BS = chr(92)
M = {'01':'01','02':'02','03':'03','04':'03','05':'04','06':'04','07':'05','09':'06','10':'07','12':'08','13':'09','14':'10','15':'11','16':'12','17':'13','18':'14','19':'15','20':'16','21':'17','22':'18','23':'19','25':'20','26':'21','27':'22','28':'23','29':'24','30':'25','31':'26','32':'27','33':'28','35':'29','36':'30','37':'31','38':'32','39':'33','40':'34','41':'35','42':'36'}
p = Path('usage.csv'); raw = p.read_text(encoding='utf-8-sig')
rows = list(csv.reader(io.StringIO(raw), delimiter=';'))
hdr, body = rows[0], rows[1:]
out, dropped = [], []
for r in body:
    if r[2] == 'A17':
        new = M[r[5]]
        fname = r[8].split(BS)[-1]
        cand = [d for d in Path('../slides').iterdir() if d.name.startswith(new + '-')][0]
        f = cand / fname
        r[5] = new
        r[8] = BS.join(['defense', 'presentation', 'slides', cand.name, fname])
        if r[0] in ('object_subject', 'methods'):
            dropped.append((r[0], new, r[7][:70])); continue
    out.append(r)
buf = io.StringIO(); w = csv.writer(buf, delimiter=';', lineterminator='\n'); w.writerow(hdr); w.writerows(out)
p.write_text('﻿' + buf.getvalue(), encoding='utf-8')
print(len(body), '->', len(out))
for d in dropped: print(d)
