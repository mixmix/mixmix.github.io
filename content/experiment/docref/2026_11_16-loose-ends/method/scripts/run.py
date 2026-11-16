# Full run: detectors D1-D5 over the docref corpus -> flags.json (with citing + target context)
import json, glob, re, sys, os
from collections import defaultdict, Counter
D, CL, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
docs, ver, url = {}, {}, {}
for f in sorted(glob.glob(os.path.join(D,'*-full.json'))):
    m=re.match(r'(.*)-(\d{4}-\d{2}-\d{2}[A-Z]?)-en-full\.json$',os.path.basename(f))
    slug,v=m.groups(); recs=json.load(open(f))
    for r in recs: r['c']=(r['c'] or '').replace('\ufeff','')
    docs[slug]=recs; ver[slug]=v; url[slug]=f'https://legislation.docref.nz/{slug}/{v}/en/'
title={}
for slug,recs in docs.items():
    t=next((r['c'] for r in recs if r['id']=='s1-line1' or r['id'].endswith('s1-subs1')), '')
    title[slug]=slug.replace('-',' ').title()
def sl(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
REP=re.compile(r'^_\[Repealed\]_$|^\[Repealed\]$')
# ---- index: section/subsection/paragraph keys -> (ids, repealed?)
IDRX=re.compile(r'^(?:.*?-)?s(\d+[A-Z]*)((?:-repealed\d*)?)((?:-(?:subs\d+[A-Z]*|line\d+|[a-z]{1,4})(?:-repealed\d*)?)*)$')
idx={}; byid={}
for slug,recs in docs.items():
    I=defaultdict(lambda:{'live':[], 'rep':[]}); B={}
    kids=defaultdict(list)
    for r in recs:
        B[r['id']]=r
        m=IDRX.match(r['id'])
        if not m: continue
        sec,srep,rest=m.groups()
        parts=[p for p in rest.split('-') if p] if rest else []
        key=[sec]; rep=bool(srep)
        for p in parts:
            if p.startswith('repealed'): rep=True; continue
            if re.fullmatch(r'line\d+',p): continue
            if p.startswith('subs'): key.append('('+p[4:]+')')
            elif re.fullmatch(r'[a-z]{1,4}',p) and p not in ('line','defn'): key.append('('+p+')')
            else: key=None; break
        if key is None: continue
        k=''.join(key)
        I[k]['rep' if rep else 'live'].append(r['id'])
    # a live section whose only text child is [Repealed] counts as repealed
    for k,v in list(I.items()):
        live=[]
        for i in v['live']:
            ch=[r for r in recs if r['id'].startswith(i+'-') and r['c'] and not r['id'].endswith('-title')]
            if B[i]['c'] and REP.match(B[i]['c'].strip()): v['rep'].append(i)
            elif not B[i]['c'] and ch and all(REP.match(c['c'].strip()) for c in ch[:1]) and len(ch)==1: v['rep'].append(i)
            else: live.append(i)
        v['live']=live
    idx[slug]=I; byid[slug]=B
def ctx(slug, bid, n=14):
    """text of a block and its descendants (for display)"""
    out=[]
    for r in docs[slug]:
        if (r['id']==bid or r['id'].startswith(bid+'-')) and r['c']:
            out.append({'id':r['id'],'c':r['c']})
            if len(out)>=n: break
    return out
def parent_section(bid):
    m=re.match(r'^(.*?-?s\d+[A-Z]*(?:-repealed\d*)?)(?:-|$)',bid)
    return m.group(1) if m else bid
flags=[]
def add(**k): flags.append(k)
ACT=r'((?:[A-Z][\w\'’()-]*|and|of|the|for|in|on|to|New|\s)+? Act \d{4})'
REF=re.compile(r'\b(section|sections|regulation|clause) (\d+[A-Z]*)((?:\(\d+[A-Z]*\))?)((?:\([a-z]{1,4}\))?)((?:\([ivx]+\))?)(?:[^.;:]{0,40}?)? of the '+ACT)
REF=re.compile(r'\bsections? (\d+[A-Z]*)((?:\(\d+[A-Z]*\))?)((?:\([a-z]{1,4}\))?)((?:\([ivx]+\))?) of the '+ACT)
TRANS=re.compile(r'former|repealed|transitional|saving|before the commencement|continues? to apply|as if|immediately before|in force before|despite the repeal|as saved|as that section|was entitled|is or was|before \d|on \d+ \w+ (19|20)\d\d',re.I)
def in_schedule_amend(bid,c):
    return bool(re.match(r'^sch\d+[A-Z]*-part\d+-sg',bid)) or bool(re.search(r'\b(replace|insert|repeal|omit|substitut)\w*\b',c,re.I)) and bool(re.match(r'^sch',bid))
# ---- D1 cross-Act refs
n1=0
for slug,recs in docs.items():
    for r in recs:
        c=r['c']
        for m in REF.finditer(c):
            sec,sub,par,sp,act=m.groups(); t=sl(act.strip())
            if t not in idx or t==slug: continue
            n1+=1
            I=idx[t]
            keys=[sec, sec+sub, sec+sub+par] if sub else [sec, sec+par]
            keys=[k for i,k in enumerate(keys) if k and (i==0 or k!=keys[i-1])]
            status='ok'; deepest=None
            for k in keys:
                if k in I and I[k]['live']: deepest=I[k]['live'][0]; continue
                if k in I and I[k]['rep']: status='REPEALED'; deepest=I[k]['rep'][0]; break
                status='MISSING'; break
            if status=='ok': continue
            sched=in_schedule_amend(r['id'],c)
            add(det='D1', kind='Reference to '+('a repealed provision' if status=='REPEALED' else 'a provision that does not exist'),
                src=slug, src_id=r['id'], src_text=c, ref=m.group(0), tgt=t, tgt_key=''.join(keys[-1:]),
                tgt_id=deepest or (I[sec]['live'] or I[sec]['rep'] or [None])[0] if sec in I else deepest,
                transitional=bool(TRANS.search(c)), schedule=sched)
# ---- D2 references to Acts declared repealed in corpus
RPL=re.compile(r'\b(?:The |the )?'+ACT.replace(' Act \\d{4})',' (?:Act|Regulations) \\d{4})')+r'\s*(?:\(\d{4} No \d+\)\s*)?(?:is|are) (?:consequentially )?repealed([^.;]{0,120})')
repealed={}
for slug,recs in docs.items():
    for r in recs:
        for m in RPL.finditer(r['c']):
            a=re.sub(r'^(The|the|of the)\s+','',m.group(1).strip()); a=re.sub(r'^.*?\bof the ','',a) if a.startswith('of ') else a
            if len(a.split())<3 or re.match(r'^(Section|Sections|Part|Schedule)',a): continue
            cond=bool(re.match(r'\s*on (the|a)\b',m.group(2)))
            if a not in repealed or not cond: repealed[a]=dict(by=slug,by_id=r['id'],text=r['c'],conditional=cond)
n2=0
for slug,recs in docs.items():
    for r in recs:
        c=r['c']
        for a,info in repealed.items():
            if info['by']==slug or a not in c: continue
            if re.search(r'(?:Act|Regulations) \d{4}', a) is None: continue
            if a.startswith('Social Security Act 1964') and 'Social Security Act 2018' in c: pass
            n2+=1
            sched=in_schedule_amend(r['id'],c)
            trans=bool(TRANS.search(c))
            if r['id'].endswith('-title') or re.search(r'-h\d+$',r['id']): continue
            add(det='D2', kind='Reference to an Act the corpus records as repealed', src=slug, src_id=r['id'], src_text=c, ref=a,
                tgt=info['by'], tgt_id=info['by_id'], tgt_note=info['text'], conditional=info['conditional'], transitional=trans, schedule=sched,
                mentions_successor=False)
# ---- D3 borrowed definitions
DEF=re.compile(r'==([^=]+)==[^.]*?(?:meaning|defined|definition)[^.]*?\bsection (\d+[A-Z]*)((?:\(\d+[A-Z]*\))?)(?:\([a-z]+\))* of the '+ACT)
n3=0
deflocs={}
for slug,recs in docs.items():
    d=defaultdict(list)
    for r in recs:
        for t in re.findall(r'==([^=]+)==',r['c']): d[t.strip().lower()].append(r['id'])
        for t in re.findall(r'\*\*([^*]+)\*\*',r['c']): d[t.strip().lower()].append(r['id'])
    deflocs[slug]=d
for slug,recs in docs.items():
    for r in recs:
        for m in DEF.finditer(r['c']):
            term,sec,sub,act=m.groups(); t=sl(act.strip())
            if t not in idx or t==slug: continue
            n3+=1
            secids=(idx[t].get(sec) or {}).get('live',[])+((idx[t].get(sec) or {}).get('rep',[]))
            if not secids: continue
            sid=secids[0]
            sectext=' '.join(x['c'] for x in docs[t] if x['id']==sid or x['id'].startswith(sid+'-')).lower()
            terms=[x.strip().lower() for x in re.split(r'\band\b|,',term) if x.strip()]
            head=terms[0]
            if head in sectext: continue
            elsewhere=[i for i in deflocs[t].get(head,[]) if not i.startswith(sid)]
            add(det='D3', kind='Borrowed definition points at a section that does not define the term', src=slug, src_id=r['id'], src_text=r['c'],
                ref=m.group(0)[m.group(0).find('section'):], term=term, tgt=t, tgt_id=sid, defined_elsewhere=elsewhere[:3])
# ---- D4 unlinked internal "section N" refs to a section that doesn't exist in the same Act
n4=0
LINKS=re.compile(r'\[[^\]]*\]\(#[^)]*\)')
INT=re.compile(r'\b(section|sections) (\d+[A-Z]*)\b(?!\s*(?:\(\d+[A-Z]*\))*\s*(?:\([a-z]+\))*\s*(?:of|to|or|and)\b\s*(?:the|that|this|any|an|a)?\s*[A-Z]?)')
for slug,recs in docs.items():
    secs={k for k in idx[slug] if re.fullmatch(r'\d+[A-Z]*',k)}
    if not secs: continue
    for r in recs:
        if r['id'].startswith('sch'): continue
        c=LINKS.sub(' ',r['c'])
        for m in re.finditer(r'\bsection (\d+[A-Z]*)((?:\(\d+[A-Z]*\))*)((?:\([a-z]+\))*)([^.;]{0,60})',c):
            sec,tail=m.group(1),m.group(4)
            if re.match(r'\s*(of|in|to|under)\b',tail) and not re.match(r'\s*of this (Act|Part|subpart)',tail): continue
            if re.search(r'\bAct\b|\bregulations?\b|\bRules?\b|\bCode\b',tail[:40]): continue
            n4+=1
            if sec in secs: continue
            add(det='D4', kind='Unlinked internal reference to a section number that does not exist', src=slug, src_id=r['id'], src_text=r['c'], ref=m.group(0)[:80], tgt=slug, tgt_key=sec, tgt_id=None)
# ---- D5 drift: inbound cross-Act refs into blocks changed in target's latest version
chg={}
for f in glob.glob(os.path.join(CL,'*.json')):
    try: d=json.load(open(f))['changelog']
    except Exception: continue
    s=re.sub(r'-\d{4}-\d{2}-\d{2}[A-Z]?\.json$','',os.path.basename(f))
    chg[s]=dict(version=d['version'],prev=d['prev_version'],touched=set(d['diffs'])|set(d['deletions'])|{x if isinstance(x,str) else str(x) for x in d['renamed']})
n5=0
for slug,recs in docs.items():
    for r in recs:
        for m in REF.finditer(r['c']):
            sec,sub,par,sp,act=m.groups(); t=sl(act.strip())
            if t not in chg or t==slug: continue
            I=idx[t]; k=sec+sub if sub else sec
            ids=(I.get(k) or {}).get('live',[])
            if not ids: continue
            tid=ids[0]
            hit=[x for x in chg[t]['touched'] if x==tid or x.startswith(tid+'-')]
            if hit and ver[slug] < chg[t]['version']:
                n5+=1
                add(det='D5', kind='Cited provision changed in its latest version, after the citing Act was last consolidated', src=slug, src_id=r['id'], src_text=r['c'], ref=m.group(0), tgt=t, tgt_id=tid, changed=hit[:6], tgt_change=f"{chg[t]['prev']} → {chg[t]['version']}")
# ---- attach context + urls
for i,f in enumerate(flags):
    f['n']=i
    f['src_url']=url[f['src']]+'#'+f['src_id']; f['src_ver']=ver[f['src']]
    f['src_section']=ctx(f['src'],parent_section(f['src_id']),30)
    if f.get('tgt_id'):
        f['tgt_url']=url[f['tgt']]+'#'+f['tgt_id']; f['tgt_ctx']=ctx(f['tgt'],f['tgt_id'],14)
    else:
        f['tgt_url']=url[f['tgt']]; f['tgt_ctx']=[]
    f['tgt_ver']=ver[f['tgt']]
    for e in f.get('defined_elsewhere',[]): f.setdefault('alt',[]).append({'url':url[f['tgt']]+'#'+e,'ctx':ctx(f['tgt'],e,4)})
stats=dict(docs=len(docs), blocks=sum(len(v) for v in docs.values()), d1_refs=n1, d2_refs=n2, d3_refs=n3, d4_refs=n4, d5_refs=n5, repealed_acts=sorted(repealed), flags=Counter(f['det'] for f in flags))
json.dump(dict(stats=stats,flags=flags,versions=ver),open(OUT,'w'),indent=1)
print(json.dumps(stats,indent=1,default=str))
