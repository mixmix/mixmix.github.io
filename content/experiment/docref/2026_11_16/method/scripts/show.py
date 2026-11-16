import json,glob,re,sys
cache={}
def load(s):
    if s not in cache: cache[s]=json.load(open(glob.glob(f'data/{s}-20*-full.json')[0]))
    return cache[s]
for arg in sys.argv[1:]:
    s,pat=arg.split(':',1); n=0
    print('==',arg)
    for r in load(s):
        if re.search(pat,r['id']) and r['c']:
            print('  ',r['id'],'|',r['c'][:260].replace('\n',' ')); n+=1
            if n>=10: break
