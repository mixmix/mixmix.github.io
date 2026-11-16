# Check 4: borrowed definitions. "==term== has the meaning given in/as in section N of the X Act" ->
# does the target section (in the corpus) still mention/define that term?
import json, glob, re, sys, os
D=sys.argv[1]
docs={}
for f in sorted(glob.glob(os.path.join(D,'*-full.json'))):
    slug=re.sub(r'-\d{4}-\d{2}-\d{2}[A-Z]?-en-full\.json$','',os.path.basename(f))
    docs[slug]=json.load(open(f))
def sl(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
pat=re.compile(r'==([^=]+)==[^.]*?(?:meaning|defined|definition)[^.]*?\bsection (\d+[A-Z]*)(?:\((\d+[A-Z]*)\))?(?:\([a-z]+\))* of the ((?:[A-Z][\w\'’()-]*|and|of|the|for|in|on|to|\s)+? Act \d{4})')
def section_text(slug,sec):
    rx=re.compile(r'^(?:.*-)?s'+re.escape(sec)+r'(?:-|$)')
    return ' '.join((r['c'] or '') for r in docs[slug] if rx.match(r['id']))
n=0
for slug,recs in docs.items():
    for r in recs:
        for m in pat.finditer(r['c'] or ''):
            term,sec,sub,title=m.groups(); t=sl(title)
            if t not in docs or t==slug: continue
            n+=1
            txt=section_text(t,sec)
            head=term.split(' and ')[0].strip().lower()
            if head not in txt.lower():
                print('MISMATCH',slug,r['id'],'->',t,'s'+sec,'| term:',term,'| target starts:',txt[:160])
print('checked',n)
