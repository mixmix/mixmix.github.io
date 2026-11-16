# Check 3: Acts declared repealed somewhere in the corpus ("The X Act YYYY (YYYY No N) is repealed")
# that are still referenced by other instruments. Flags references not in obviously transitional/savings text.
import json, glob, re, sys, os, csv
from collections import defaultdict
D=sys.argv[1]
docs={}
for f in sorted(glob.glob(os.path.join(D,'*-full.json'))):
    slug=re.sub(r'-\d{4}-\d{2}-\d{2}[A-Z]?-en-full\.json$','',os.path.basename(f))
    docs[slug]=json.load(open(f))
rep=re.compile(r'\b(?:The |the )?((?:[A-Z][\w\'’()-]*|and|of|the|for|in|on|to|\s)+? (?:Act|Regulations) \d{4})\s*(?:\(\d{4} No \d+\)\s*)?(?:is|are) (?:consequentially )?repealed')
repealed={}
for slug,recs in docs.items():
    for r in recs:
        for m in rep.finditer(r['c'] or ''):
            t=re.sub(r'^(The|the)\s+','',m.group(1).strip())
            if len(t.split())<3: continue
            repealed.setdefault(t,(slug,r['url']))
print('repealed acts declared:',len(repealed))
trans=re.compile(r'former|repealed|transitional|saving|before the commencement|continues? to apply|as if|immediately before|under the repealed|in force before|(?:came|comes) into force|despite the repeal',re.I)
rows=[]
for slug,recs in docs.items():
    for r in recs:
        c=r['c'] or ''
        if 'Schedule' in r['id'] or r['id'].startswith('sch'): sched=True
        else: sched=False
        for t,(rs,ru) in repealed.items():
            if t in c and rs!=slug:
                rows.append(('transitional?' if trans.search(c) else 'LIVE-LOOKING', 'schedule' if sched else 'body', t, slug, r['url'], rs, ru, c[:300].replace('\n',' ')))
from collections import Counter
print(Counter((r[0],r[1]) for r in rows))
with open(sys.argv[2],'w',newline='') as f:
    w=csv.writer(f); w.writerow(['flag','where','repealed_act','citing_doc','citing_url','repealed_by','repeal_url','text'])
    for r in sorted(rows): w.writerow(r)
c=Counter((r[2]) for r in rows if r[0]=='LIVE-LOOKING' and r[1]=='body')
print(c.most_common(40))
