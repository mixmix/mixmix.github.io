# Check 2: textual cross-Act references "section N(k) of the X Act YYYY" where X is in the corpus,
# resolved against the target Act's current version: target missing, or marked repealed.
import json, glob, re, sys, os, csv
from collections import defaultdict
D=sys.argv[1]
docs={}
for f in sorted(glob.glob(os.path.join(D,'*-full.json'))):
    slug=re.sub(r'-\d{4}-\d{2}-\d{2}[A-Z]?-en-full\.json$','',os.path.basename(f))
    docs[slug]=json.load(open(f))
def title_to_slug(t):
    return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
idx={}
for slug,recs in docs.items():
    secs=defaultdict(lambda: {'live':set(),'rep':set()})
    for r in recs:
        m=re.match(r'^(?:.*-)?s(\d+[A-Z]*)(-repealed)?(?:-subs(\d+[A-Z]*)(-repealed)?)?$', r['id'])
        if not m: continue
        sec,srep,sub,subrep=m.groups()
        key=sec if sub is None else f"{sec}({sub})"
        (secs[key]['rep'] if (srep or subrep) else secs[key]['live']).add(r['id'])
        if sub is None and srep is None and r['c']=='' : pass
    # also text-level repeal: section whose only content is [Repealed]
    idx[slug]=secs
ref=re.compile(r'\bsections? (\d+[A-Z]*)((?:\(\d+[A-Z]*\))?)(?:\([a-z]+\))*(?:\([ivx]+\))* of the ((?:[A-Z][\w\'’()-]*|and|of|the|for|in|on|to|New|\s)+? Act \d{4})')
rows=[]
for slug,recs in docs.items():
    for r in recs:
        c=r['c'] or ''
        for m in ref.finditer(c):
            sec,sub,title=m.group(1),m.group(2),m.group(3).strip()
            t=title_to_slug(title)
            if t not in idx or t==slug: continue
            s=idx[t]
            key=sec+sub if sub else sec
            if key in s and s[key]['live']: status='ok'
            elif key in s and s[key]['rep']: status='REPEALED'
            elif sub and sec in s and s[sec]['live']: status='NO_SUBSECTION'
            elif sub and sec in s and s[sec]['rep']: status='REPEALED'
            else: status='MISSING'
            rows.append((status,slug,r['id'],t,key,r['url'],c[:300].replace('\n',' ')))
from collections import Counter
print(Counter(r[0] for r in rows))
with open(sys.argv[2],'w',newline='') as f:
    w=csv.writer(f); w.writerow(['status','source','block','target','target_section','url','text'])
    for r in sorted(rows):
        if r[0]!='ok': w.writerow(r)
