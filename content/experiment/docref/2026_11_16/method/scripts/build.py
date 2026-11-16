# Assemble adjudicated findings + evidence text into data.json for the artifact.
import json, glob, re, os, html, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cache = {}
def load(s):
    if s not in cache:
        f = glob.glob(f'{ROOT}/data/{s}-20*-full.json')[0]
        v = re.search(r'-(\d{4}-\d{2}-\d{2}[A-Z]?)-en-full', f).group(1)
        recs = json.load(open(f))
        for r in recs: r['c'] = (r['c'] or '').replace('﻿', '')
        cache[s] = (v, recs)
    return cache[s]
TITLES = {x['slug']: x['title'] for x in json.load(open(f'{ROOT}/dl/docref.json'))['documents']}
def act_title(s):
    if s in TITLES: return TITLES[s]
    v, recs = load(s)
    t = next((r['c'] for r in recs if r['id'] == 's1-line1' or re.match(r'^(part1-)?s1-subs1$', r['id'])), '')
    m = re.search(r'(?:is|are) the (.+?)\.?$', t)
    name = m.group(1) if m else s.replace('-', ' ').title()
    name = name.replace('Act ', 'Act ').strip()
    TITLES[s] = name
    return name

def sec_label(bid):
    """human pinpoint from a block id, e.g. part7-s286-subs5-h -> s 286(5)(h)"""
    m = re.match(r'^sch(\d+[A-Z]*)', bid)
    if m and 'form' in bid: return 'Sch ' + m.group(1) + ' form ' + bid.split('form')[-1].split('-')[0]
    if m:
        cl = re.search(r'-s(\d+[A-Z]*)', bid)
        return f"Sch {m.group(1)}" + (f" cl {cl.group(1)}" if cl else '')
    m = re.search(r'(?:^|-)s(\d+[A-Z]*(?:\.\d+)?)((?:-repealed\d*)?)(.*)$', bid)
    if not m: return bid
    out = 's ' + m.group(1)
    for p in m.group(3).split('-'):
        if not p or p.startswith('repealed') or re.match(r'(line|defn|ex|exl|title|p)\d*$', p): continue
        if p.startswith('subs'): out += f'({p[4:]})'
        elif re.fullmatch(r'[a-z]{1,4}', p): out += f'({p})'
    if '.' in m.group(1): out = 'r ' + m.group(1)
    return out
_sec_label = sec_label
def sec_label(bid, slug=''):
    if re.match(r'^part\d+[A-Z]*-title$', bid): return 'Part ' + re.match(r'^part(\d+[A-Z]*)', bid).group(1)
    if re.match(r'^part\d+[A-Z]*-subpart\d+-title$', bid): return 'Part ' + re.match(r'^part(\d+[A-Z]*)', bid).group(1) + ' subpart ' + re.search(r'subpart(\d+)', bid).group(1)
    out = _sec_label(bid)
    if ('regulations' in slug) and out.startswith('s '): out = 'r ' + out[2:]
    m = re.match(r'^sch\d+[A-Z]*-mc\d+-part(\d+[A-Z]*)', bid)
    if m: out += ' Part ' + m.group(1)
    if '-ex' in bid: out += ' example ' + re.search(r'-ex(\d+)', bid).group(1)
    return out

def block(s, bid, depth=40, with_children=True):
    v, recs = load(s)
    out = []
    title = ''
    sec = re.match(r'^(.*?(?:^|-)s\d+[A-Z]*(?:\.\d+)?(?:-repealed\d*)?)(?:-|$)', bid)
    if sec:
        t = next((r['c'] for r in recs if r['id'] == sec.group(1) + '-title'), '')
        title = t
    found = False
    for r in recs:
        if r['id'] == bid or (with_children and r['id'].startswith(bid + '-')):
            found = True
            if r['c'] and (not r['id'].endswith('-title') or r['id'] == bid):
                lvl = r['id'][len(bid):].count('-')
                out.append({'id': r['id'], 'c': r['c'], 'lvl': lvl})
            if len(out) >= depth: break
    if not found:
        raise SystemExit(f'missing block {s} {bid}')
    _ = dict(act=act_title(s), slug=s, ver=v, id=bid, pin=sec_label(bid), sectitle=title,
                url=f'https://legislation.docref.nz/{s}/{v}/en/#{bid}', lines=out)
    d=dict(act=act_title(s), slug=s, ver=v, id=bid, pin=sec_label(bid, s), sectitle=title, url=f'https://legislation.docref.nz/{s}/{v}/en/#{bid}', lines=out)
    return d

def section_of(s, bid):
    m = re.match(r'^(.*?(?:^|-)s\d+[A-Z]*(?:\.\d+)?(?:-repealed\d*)?)(?:-|$)', bid)
    return m.group(1) if m else bid

def ev(role, s, bid, note='', mark=None, children=True, context=True):
    b = block(s, bid, with_children=children)
    b.update(role=role, note=note, mark=mark or [])
    if context:
        sid = section_of(s, bid)
        if sid != bid:
            b['context'] = block(s, sid, depth=60)['lines']
    return b

def old_version_text(slug, ver, page, prefix):
    s = open(page).read()
    lines = []
    for m in re.finditer(r'<(\w+)[^>]*id="(' + re.escape(prefix) + r'(?:-[^"]*)?)"[^>]*>(.*?)</\1>', s, re.S):
        inner = m.group(3)
        if m.group(2) == prefix: continue
        t = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', '', inner))).strip()
        if t and not m.group(2).endswith('-title'):
            lines.append({'id': m.group(2), 'c': t, 'lvl': m.group(2)[len(prefix):].count('-')})
    return lines

P = lambda s, *ids: [(s, i) for i in ids]

findings = [
dict(key='gas-energy-commission', conf=93, cat='Phantom body',
 title='Gas Act 1992 still gives powers to an "Energy Commission" whose enabling subpart is missing',
 short='Gas Act Part 4A: "the Commission"',
 summary='Section 43D defines "Commission" as the Energy Commission "to be established under section 43ZZH". Part 4A jumps from subpart 2 (s 43ZZF) to subpart 4 (s 43ZZR), so there is no s 43ZZH and no body to establish. The term is still live: 34 provisions in Part 4A give "the Commission" roles in recommending regulations, monitoring, enforcement and appeals. Section 43M(1)(b) also applies "sections 43ZZN and 43ZZO", which do not exist either.',
 why='The defined body is unreachable and the provisions that use it are inert, but they read as if they work. This is a dangling reference, not a disagreement between two working rules.',
 s38='Probably no cure. Legislation Act 2019 s 38 deals with repealed legislation and needs replacing or corresponding legislation, and nothing here appears to replace an Energy Commission.',
 question='Was subpart 3 of Part 4A (Energy Commission) repealed or never commenced? If so, should s 43D "Commission" and the 34 references to it be removed by editorial change or revision?',
 detector='D4 unlinked internal reference + manual trace',
 evidence=[
  ev('cites', 'gas-act-1992', 'part4A-subpart1-s43D-defn2', 'Definition still in force.', ['section 43ZZH']),
  ev('cites', 'gas-act-1992', 'part4A-subpart1-s43M-subs1-b', 'Also points into the missing subpart.', ['sections 43ZZN and 43ZZO']),
  ev('uses', 'gas-act-1992', 'part4A-subpart5-s43ZZS-subs1', 'One of 34 operative uses of "the Commission".', ['the Commission']),
  ev('uses', 'gas-act-1992', 'part4A-subpart1-s43ZE-line1', 'Appeal rights for the Commission.', ['the Commission']),
  ev('target', 'gas-act-1992', 'part4A-subpart2-s43ZZF-title', 'Last section of subpart 2: s 43ZZF.', [], children=False, context=False),
  ev('target', 'gas-act-1992', 'part4A-subpart4-title', 'Next heading in the Act: subpart 4 begins at s 43ZZR. There is no subpart 3 and no s 43ZZG to 43ZZQ.', [], children=False, context=False),
 ]),
dict(key='rsa-psa-s52', conf=91, cat='Version drift',
 title='Regulatory Standards Act 2025 overrides a Public Service Act section that was repealed six months later',
 short='Regulatory Standards Act s 22(2) → PSA s 52',
 summary='Section 22(2) of the Regulatory Standards Act 2025 (version 18 Nov 2025) says chief executives act independently "despite section 52 of the Public Service Act 2020". In docref\'s Public Service Act version of 3 June 2026, s 52 (general responsibilities to the Minister) is repealed and a new s 11A (principal responsibilities of chief executives) appears. The Regulatory Standards Act was not updated, so its override now points at an empty section.',
 why='The override is the operative part of s 22. If it no longer reaches the provision that makes chief executives answerable to Ministers, whether the independence rule wins is less clear. The two Acts were in step at enactment and drifted apart later, which is the kind of error Estonia\'s tool was built to catch.',
 s38='Arguable. If s 11A "replaces or corresponds to" s 52, s 38(2) may read the reference as one to s 11A. An expert should confirm that the mapping is clean.',
 question='Did the 2026 Public Service Act amendment intend s 11A to replace s 52 for the purposes of RSA s 22(2)? Should the RSA reference be updated?',
 detector='D1 cross-Act reference → repealed provision, then version history',
 evidence=[
  ev('cites', 'regulatory-standards-act-2025', 'part2-subpart4-s22', 'Citing provision, as enacted 18 Nov 2025.', ['section 52 of the Public Service Act 2020']),
  ev('target', 'public-service-act-2020', 'part3-subpart2-s52', 'Current Public Service Act: s 52 shows only [Repealed].', [], context=False),
  dict(role='before', act='Public Service Act 2020', slug='public-service-act-2020', ver='2026-04-01', id='part3-subpart2-s52', pin='s 52', sectitle='General responsibilities of chief executives of departments and departmental agencies',
       url='https://legislation.docref.nz/public-service-act-2020/2026-04-01/en/#part3-subpart2-s52', note='The same section in the 1 Apr 2026 version, before repeal. This is what the RSA was written against.', mark=['responsible to the appropriate Minister'],
       lines=old_version_text('public-service-act-2020', '2026-04-01', f'{ROOT}/pages/psa-2026-04-01.html', 'part3-subpart2-s52')),
  ev('successor', 'public-service-act-2020', 'part1-subpart2-s11A', 'Probable successor, first appearing in the 3 Jun 2026 version.', [], context=False),
 ]),
dict(key='commerce-associate', conf=88, cat='Borrowed definition',
 title='Commerce Act borrows "associate" from a section of the Electricity Industry Act that does not define it',
 short='Commerce Act s 54C(4) → EIA s 73',
 summary='Commerce Act s 54C(4) says "associate" has "the same meaning as in section 73 of the Electricity Industry Act 2010". Section 73 is the ownership separation rule and defines only "nameplate" and "total capacity". The EIA definition of associate is in Schedule 2 clause 8, and EIA s 6A(4) also points there. The cross-reference was inserted by EIA s 150(2) in 2010.',
 why='"Associate" matters in s 54C. It decides whether conveying electricity to the supplier\'s associates, or competition with a non-associate, takes a line out of "electricity lines services" for Part 4 regulation. A reader following the reference finds no definition.',
 s38='No cure. Nothing was repealed; the reference points at the wrong place in a live Act.',
 question='Did a later EIA amendment move "associate" out of s 73 into Schedule 2? Should s 54C(4) now cite Schedule 2 clause 8?',
 detector='D3 borrowed definition',
 evidence=[
  ev('cites', 'commerce-act-1986', 'part4-subpart9-s54C-subs4-defn1', 'The borrowed definition.', ['section 73 of the Electricity Industry Act 2010']),
  ev('uses', 'commerce-act-1986', 'part4-subpart9-s54C-subs2-e', 'Where "associate" does work in s 54C.', ['associate']),
  ev('target', 'electricity-industry-act-2010', 'part3-subpart1-s73', 'Section 73 as it now reads: no "associate".', [], context=False),
  ev('successor', 'electricity-industry-act-2010', 'sch2-mc1-s8', 'Where the definition actually lives.', ['associate'], context=False),
  ev('successor', 'electricity-industry-act-2010', 'part1-subpart-s6A-subs4-defn1', 'The EIA itself points to Schedule 2.', ['clause 8'], context=False),
  ev('history', 'electricity-industry-act-2010', 'part5-subpart4-s150-subs2', 'The 2010 amendment that created the cross-reference.', ['section 73 of the Electricity Industry Act 2010'], context=False),
 ]),
dict(key='telecom-part4b', conf=86, cat='Phantom part',
 title='Telecommunications Act refers to a Part 4B and a section 156S that are not in the Act',
 short='Telecommunications Act s 240 → Part 4B / s 156S',
 summary='Section 240(1)(b) makes a consumer complaints system the dispute scheme "if Part 4B comes into force in accordance with section 156S". Section 240(3) applies ss 241 to 245 "unless Part 4B comes into force", and the s 4 overview says complaints systems "are set out in Part 4B". The Act goes from Part 4AA to Part 5 with no Part 4B, and the 156 series ends at s 156R.',
 why='These conditions can never be met as written. Section 240(3) still works in practice because Part 4B will never come into force, but s 4(gb) and s 240(1)(b) describe machinery that is not in the Act.',
 s38='Unclear. If Part 4B was repealed, s 38 has nothing to substitute, because no replacing provision is evident.',
 question='Was Part 4B (with s 156S) repealed or never enacted? Should s 4(gb) and s 240(1)(b) and (3) be tidied?',
 detector='D4 unlinked internal reference + manual trace',
 evidence=[
  ev('cites', 'telecommunications-act-2001', 'part7-s240-subs1-b', 'Conditional on Part 4B commencing under s 156S.', ['Part 4B', 'section 156S']),
  ev('cites', 'telecommunications-act-2001', 'part7-s240-subs3', '', ['Part 4B']),
  ev('cites', 'telecommunications-act-2001', 'part1-subpart1-s4-line1-gb', 'The overview of the Act also relies on Part 4B.', ['Part 4B']),
  ev('target', 'telecommunications-act-2001', 'part4A-subpart2-s156R-title', 'The last 156-series section is s 156R.', [], children=False, context=False),
  ev('target', 'telecommunications-act-2001', 'part4AA-title', 'Part 4AA is followed directly by Part 5. There is no Part 4B.', [], children=False, context=False),
 ]),
dict(key='patents-judicature', conf=80, cat='Repealed Act applied',
 title='Patents Act applies four sections of the repealed Judicature Act 1908 to the trans-Tasman disciplinary tribunal',
 short='Patents Act s 286(2) → Judicature Act ss 56M–56Q',
 summary='When the trans-Tasman patent attorneys Disciplinary Tribunal sits in New Zealand, s 286(2) applies "the following provisions of the Judicature Act 1908": ss 56M (oaths), 56N (orders not reviewable), 56O (contempt) and 56Q (privileges and immunities). The Senior Courts Act 2016 s 182(2) repealed the rest of the Judicature Act.',
 why='These provisions decide whether the tribunal can administer oaths and punish contempt, and whether participants are immune. The text applies them from an Act that no longer exists.',
 s38='Probably cured in part. Section 38(2) points to the legislation that "replaces or corresponds to" the repealed provisions, but the expert has to find those successors first.',
 question='Which provisions now correspond to Judicature Act ss 56M–56Q, and should s 286(2) name them?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'patents-act-2013', 'part6-s286', 'Applies Judicature Act provisions, with modifications.', ['Judicature Act 1908']),
  ev('target', 'senior-courts-act-2016', 'part6-s182-subs2', 'Repeal of the Judicature Act.', ['The rest of the Judicature Act 1908'], context=False),
 ]),
dict(key='acc-hse', conf=78, cat='Repealed Act applied',
 title='ACC Act information-sharing powers still point at the Health and Safety in Employment Act and the Machinery Act',
 short='ACC Act s 286(3), (5)(h)',
 summary='Section 286(3) lets MBIE and health and safety regulators pass ACC information to "any agency designated under section 28B of the Health and Safety in Employment Act 1992". The list of "relevant Acts" in s 286(5) includes the Machinery Act 1950. Health and Safety at Work Act 2015 s 231 repealed both. The same list was partly updated: para (a) is repealed and the HSWA 2015 appears at (e).',
 why='Who may receive ACC injury information is a privacy-significant question. Agencies are now designated under HSWA s 191, not HSE Act s 28B. The Machinery Act survives only as s 21A, kept alive for the Amusement Devices Regulations 1978.',
 s38='Likely cured for s 28B, which maps to HSWA s 191. Less clear for the Machinery Act, which has no general successor.',
 question='Does s 38(2) carry s 286(3) over to HSWA s 191 designations? Should (5)(h) be removed?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'accident-compensation-act-2001', 'part7-s286-subs3', '', ['section 28B of the Health and Safety in Employment Act 1992']),
  ev('cites', 'accident-compensation-act-2001', 'part7-s286-subs5', 'Partly updated list: (a) is repealed, (e) is HSWA, (h) is still the Machinery Act.', ['Machinery Act 1950', 'Health and Safety at Work Act 2015']),
  ev('target', 'health-and-safety-at-work-act-2015', 'part5-subpart5-s231', 'Both repealed.', ['Health and Safety in Employment Act 1992', 'Machinery Act 1950'], context=False),
  ev('successor', 'health-and-safety-at-work-act-2015', 'part5-subpart1-s191-subs1', 'Current designation power.', ['designated agency'], context=False),
  ev('history', 'health-and-safety-at-work-act-2015', 'sch1-part1-s2-subs3', 'The only surviving piece of the Machinery Act.', ['section 21A'], context=False),
 ]),
dict(key='hcr-ssa1964', conf=75, cat='Repealed Act applied',
 title='High Court Rules on attachment orders still run on the Social Security Act 1964',
 short='High Court Rules rr 17.31–17.38',
 summary='The attachment order rules define "benefit" by reference to the Social Security Act 1964 and set priority against deductions "under section 86" of that Act. Rule 17.35(4) says "Section 84 of the Social Security Act 1964 does not apply to an attachment order". Social Security Act 2018 s 455 repealed the 1964 Act.',
 why='These rules decide whose claim on a debtor\'s benefit or wages comes first. Each one now depends on finding the 2018 equivalent of a specific 1964 section.',
 s38='Probably cured. The rules are legislation, so s 38(2) reads the references as references to the corresponding SSA 2018 provisions.',
 question='Which SSA 2018 provisions correspond to SSA 1964 ss 84, 86 and 86A? Should the Rules Committee update Part 17 subpart 4?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'high-court-rules-2016', 'part17-subpart4-s17.35-subs4', '', ['Section 84 of the Social Security Act 1964']),
  ev('cites', 'high-court-rules-2016', 'part17-subpart4-s17.31-defn3-f', 'Definition of earnings includes a 1964 Act benefit.', ['Social Security Act 1964'], context=False),
  ev('cites', 'high-court-rules-2016', 'part17-subpart4-s17.35-subs1-e', 'Priority ranking.', ['section 86 of the Social Security Act 1964'], context=False),
  ev('cites', 'high-court-rules-2016', 'part17-subpart4-s17.38-subs5', '', ['Social Security Act 1964'], context=False),
  ev('target', 'social-security-act-2018', 'part8-s455-subs1', '', ['is repealed'], context=False),
 ]),
dict(key='ombudsmen-ssa-committees', conf=70, cat='Defunct bodies listed',
 title='Ombudsmen Act schedule still lists welfare committees established under the repealed 1964 Act',
 short='Ombudsmen Act Sch 1 Part 3',
 summary='Schedule 1 lists the organisations the Ombudsmen can investigate. Part 3 still includes "Area welfare executive committees", "District executive committees" (both under s 7K) and "Institution management committees" (s 7M) of the Social Security Act 1964, which was repealed in 2018.',
 why='The jurisdiction list names bodies that may no longer exist. The harm is small, but anyone checking jurisdiction would be misled, and it is easy to verify.',
 s38='Partly. Any committees continued under SSA 2018 would carry over. Bodies that were not continued should come out of the list.',
 question='Do any of these committees still exist under the SSA 2018? If not, should they be removed from Schedule 1?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'ombudsmen-act-1975', 'sch1-mc1-part3-line4', '', ['section 7K of the Social Security Act 1964'], context=False),
  ev('cites', 'ombudsmen-act-1975', 'sch1-mc1-part3-line18', '', ['section 7K of the Social Security Act 1964'], context=False),
  ev('cites', 'ombudsmen-act-1975', 'sch1-mc1-part3-line28', '', ['section 7M of the Social Security Act 1964'], context=False),
  ev('target', 'social-security-act-2018', 'part8-s455-subs1', '', ['is repealed'], context=False),
 ]),
dict(key='ssr-nzphd', conf=64, cat='Repealed Act applied',
 title='Social Security Regulations define health "providers" by the repealed NZ Public Health and Disability Act',
 short='Social Security Regulations 2018 regs 282–291',
 summary='The community services card regulations define "provider" as "a provider of services funded under the New Zealand Public Health and Disability Act 2000" and limit card use to services funded under that Act. The Pae Ora (Healthy Futures) Act 2022 s 103 repealed it.',
 why='The regulations tie card eligibility for subsidised services to funding under an Act that has gone. Health services are now funded under Pae Ora.',
 s38='Likely cured, since the Pae Ora Act is the obvious corresponding legislation. Still a clear target for tidying.',
 question='Is Pae Ora clearly the corresponding Act for these definitions, and should regs 282, 290 and 291 be updated?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'social-security-regulations-2018', 'part8-subpart4-s282-defn5', '', ['New Zealand Public Health and Disability Act 2000'], context=False),
  ev('cites', 'social-security-regulations-2018', 'part8-subpart4-s290-subs1-e-i', '', ['New Zealand Public Health and Disability Act 2000'], context=False),
  ev('cites', 'social-security-regulations-2018', 'part8-subpart4-s291-subs7-b', '', ['New Zealand Public Health and Disability Act 2000'], context=False),
  ev('target', 'pae-ora-healthy-futures-act-2022', 'part4-subpart5-s103-subs1', '', ['is repealed'], context=False),
 ]),
dict(key='hcr-form-cl3', conf=56, cat='Repealed Act applied',
 title='High Court form CL3 is headed as a notice under the repealed Judicature Act',
 short='High Court Rules Sch 1 form CL3',
 summary='Form CL3 is titled "Notice of proceeding (being application to commercial list Judge) under section 24C(4) of Judicature Act 1908". The Judicature Act was repealed by the Senior Courts Act 2016 s 182(2).',
 why='The form is prescribed, so a stale statutory basis on its face is a small but visible error.',
 s38='Cured in substance by s 38(2). The fix is cosmetic.',
 question='Which Senior Courts Act provision now corresponds to s 24C(4), and should the form heading cite it?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'high-court-rules-2016', 'sch1-formCL3', '', ['section 24C(4) of Judicature Act 1908'], children=False, context=False),
  ev('target', 'senior-courts-act-2016', 'part6-s182-subs2', '', ['The rest of the Judicature Act 1908'], context=False),
 ]),
dict(key='fmcr-interest-example', conf=52, cat='Stale example',
 title='Worked example in the FMC Regulations uses an interest rate from the repealed Judicature Act regime',
 short='FMC Regulations 2014 Sch 20 example 2',
 summary='Example 2 in Schedule 20 calculates present values using "the Judicature (Prescribed Rate of Interest) Order 2011", which prescribes 5% "for the purposes of section 87(3) of the Judicature Act 1908". Senior Courts Act s 182(4) repealed s 87.',
 why='Examples are illustrative, but readers copy the method. This one names a rate source that no longer applies. The current regime is the Interest on Money Claims Act 2016.',
 s38='Not really applicable, because an example has no operative force. This is a tidying item.',
 question='Does the formula the example illustrates still rely on the Judicature Act rate, or should the example be redrawn?',
 detector='D2 reference to repealed Act',
 evidence=[
  ev('cites', 'financial-markets-conduct-regulations-2014', 'sch20-part2-s1-ex2', '', ['section 87(3) of the Judicature Act 1908', 'Judicature (Prescribed Rate of Interest) Order 2011'], context=False),
  ev('target', 'senior-courts-act-2016', 'part6-s182-subs4', '', ['Section 87 of the Judicature Act 1908'], context=False),
 ]),
dict(key='building-pfa44a', conf=44, cat='Spent provision',
 title='Building Act wind-up provision requires tabling under a repealed Public Finance Act section',
 short='Building Act s 423(3) → PFA s 44A',
 summary='Section 423 required the Building Industry Authority\'s final report to be tabled "under section 44A of the Public Finance Act 1989". Section 44A is repealed.',
 why='The provision is spent. It was a one-off duty in 2004–05, so this is clutter for a revision bill rather than a live risk.',
 s38='Moot, because the duty has been discharged.',
 question='Can s 423 be removed as spent in a revision programme?',
 detector='D1 cross-Act reference → repealed provision',
 evidence=[
  ev('cites', 'building-act-2004', 'part5-subpart4-s423-subs3', '', ['section 44A of the Public Finance Act 1989']),
  ev('target', 'public-finance-act-1989', 'part4-s44A-repealed2', 'Two repealed provisions numbered 44A sit here. This one is the tabling duty.', [], context=False),
 ]),
dict(key='radio-broadcasting95', conf=34, cat='Spent provision',
 title='Radiocommunications Act transitional rights still turn on a repealed Broadcasting Act section',
 short='Radiocommunications Act ss 145–147, 171',
 summary='Six provisions about 1989 transitional frequency rights refer to licences granted "pursuant to section 95(2) of the Broadcasting Act 1989". Broadcasting Act s 95 reads "[Repealed]".',
 why='These are historical changeover provisions and almost certainly spent. They are included because they are objectively stale and quick to verify.',
 s38='Moot.',
 question='Are Part 16 ss 145–147 and 171 spent and suitable for removal?',
 detector='D1 cross-Act reference → repealed provision',
 evidence=[
  ev('cites', 'radiocommunications-act-1989', 'part16-s146-subs1-b-ii', '', ['section 95(2) of the Broadcasting Act 1989']),
  ev('cites', 'radiocommunications-act-1989', 'part16-s147-subs1-b', '', ['section 95(2) of the Broadcasting Act 1989'], context=False),
  ev('target', 'broadcasting-act-1989', 'part7-s95', '', [], context=False),
 ]),
]

ruled_out = [
 dict(group='Airport Authorities Act 1966 references (RMA s 166, OIA Sch 1, Public Audit Act Sch 1)', n=3, why='Deliberate dual track. Civil Aviation Act 2023 s 488 repeals the 1966 Act only on the fifth anniversary of s 487 commencing, and the new regime sits alongside it.',
      url=block('resource-management-act-1991','part8-s166-subs1-defn3-g')['url']),
 dict(group='Environmental Protection Authority Act s 22–23 → RMA s 42B', n=2, why='These provisions disestablish the old EPA, so they have to name the section that created it.', url=block('environmental-protection-authority-act-2011','part3-subpart1-s23')['url']),
 dict(group='Electricity Industry Act ss 105, 132, 140, Sch 4, Sch 6 → Electricity Act 1992', n=6, why='Transitional and continuation provisions for the Electricity Commission handover. Citing the repealed sections is intended.', url=block('electricity-industry-act-2010','part5-subpart3-s132-defn2')['url']),
 dict(group='Financial Markets Conduct Act Sch 4 → Financial Advisers Act 2008', n=29, why='Transitional schedule that preserves the effect of past prohibitions and failures under the old regime.', url=block('financial-markets-conduct-act-2013','sch4-part3-s48-subs2')['url']),
 dict(group='Social Security Regulations 2018 → Social Security Act 1964', n=21, why='Mostly grandparenting rules (transfers in 2013, payments approved in 2014, debts saved by Child Support Act s 256). They point at history on purpose.', url=block('social-security-regulations-2018','part6-subpart3-s188-subs2')['url']),
 dict(group='New Zealand Public Health and Disability Act 2000 (its own text)', n=8, why='docref still holds the Act\'s final 2022 version. The citing Act is itself repealed, so nothing here is live.', url='https://legislation.docref.nz/public-health-and-disability-act-2000/2022-07-01/en/'),
 dict(group='Minimum Wage Act s 4A, Social Security Act 2018 Sch 1, Crown Minerals Act Sch 1', n=4, why='They name both the old and new Acts, or are transitional clauses.', url=block('minimum-wage-act-1983','s4A-subs6-defn3')['url']),
 dict(group='Borrowed definitions that paraphrase the target ("involved in a default" → "involved in a breach", "Treaty", "State services")', n=20, why='The citing Act adapts the target\'s wording. The target section is correct even though the exact term does not appear in it.', url=block('minimum-wage-act-1983','s10-subs4')['url']),
 dict(group='Unlinked "section N" references in lists', n=223, why='Nearly all are list items whose lead-in names another Act (for example "the following provisions of the Customs and Excise Act 2018 apply"). They were filtered by reading each lead-in.', url=block('anti-money-laundering-act-2009','part3-subpart3-s114-subs4')['url']),
 dict(group='Version drift into changed interpretation sections', n=77, why='The cited interpretation section changed in its latest version, but none of the changed definitions was the one being cited.', url=None),
]

flags = json.load(open(f'{ROOT}/flags.json'))
st = flags['stats']
stats = dict(docs=st['docs'], blocks=st['blocks'],
  detectors=[
   dict(id='D1', name='Cross-Act section references', desc='"section N(k)(p) of the X Act" resolved against X\'s current block IDs. Flags targets that are repealed or do not exist.', examined=st['d1_refs'], flagged=st['flags']['D1']),
   dict(id='D2', name='References to repealed Acts', desc='Acts the corpus itself says are repealed ("The X Act is repealed"), still named elsewhere outside transitional wording.', examined=st['d2_refs'], flagged=st['flags']['D2']),
   dict(id='D3', name='Borrowed definitions', desc='"term has the meaning in section N of X". Checks whether section N still contains or defines the term.', examined=st['d3_refs'], flagged=st['flags']['D3']),
   dict(id='D4', name='Unlinked internal references', desc='Plain-text "section N" within an Act where no section N exists.', examined=st['d4_refs'], flagged=st['flags']['D4']),
   dict(id='D5', name='Version drift', desc='Cross-Act references into provisions changed in the target\'s latest version, after the citing Act was last consolidated.', examined=st['d5_refs'], flagged=st['flags']['D5']),
  ])
out = dict(generated='2026-11-16', stats=stats, findings=sorted(findings, key=lambda f: -f['conf']), ruled_out=ruled_out)
json.dump(out, open(f'{ROOT}/data.json', 'w'), ensure_ascii=False)
print(len(findings), 'findings', os.path.getsize(f'{ROOT}/data.json'), 'bytes')
for f in out['findings']:
    print(f['conf'], f['key'], [(e['act'][:20], e['pin'], len(e['lines'])) for e in f['evidence']])
