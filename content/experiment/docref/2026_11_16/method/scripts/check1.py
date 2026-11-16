# Check 1: internal cross-references that point at a block id not present in the same version
import json, glob, re, sys, os
D=sys.argv[1]
link=re.compile(r'\]\(#([^)\s]+)\)')
tot=0; out=[]
for f in sorted(glob.glob(os.path.join(D,'*-full.json'))):
    recs=json.load(open(f)); ids={r['id'] for r in recs}
    for r in recs:
        for m in link.finditer(r['c'] or ''):
            tot+=1
            if m.group(1) not in ids:
                out.append((os.path.basename(f).split('-20')[0], r['id'], m.group(1), r['c'][:200].replace('\n',' ')))
print('links',tot,'broken',len(out))
from collections import Counter
print(Counter(o[0] for o in out).most_common(30))
for o in out[:40]: print(o)
