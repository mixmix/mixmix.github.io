# Pilot candidates: NZ legislation cross-reference defects (docref corpus, latest versions, Nov 2026)

Each row: the citing block, the target, and why it looks wrong. Confirm against legislation.govt.nz before relying on any of these.

1. **Commerce Act 1986 s54C(4), "associate"**: wrong section in a borrowed definition (strongest candidate)
   - Citing: https://legislation.docref.nz/commerce-act-1986/2026-07-01/en/#part4-subpart9-s54C-subs4-defn1
     "associate has the same meaning as in section 73 of the Electricity Industry Act 2010"
   - Target s73 (Ownership separation) does not define associate: https://legislation.docref.nz/electricity-industry-act-2010/2025-03-30/en/#part3-subpart1-s73-subs3
   - The definition is in EIA Sch 2 cl 8: https://legislation.docref.nz/electricity-industry-act-2010/2025-03-30/en/#sch2-mc1-s8-title
     (EIA s6A(4) points there too: #part1-subpart-s6A-subs4-defn1)
   - The cross-reference came from EIA s150(2) in 2010: #part5-subpart4-s150-subs2
   - Question for the expert: did a later EIA amendment move "associate" out of s73 without a matching Commerce Act update? Is the reference now inoperative or wrong?

2. **Accident Compensation Act 2001 s286**: references to repealed health and safety law, in a list that was otherwise updated
   - s286(3) refers to agencies "designated under section 28B of the Health and Safety in Employment Act 1992": https://legislation.docref.nz/accident-compensation-act-2001/2026-07-10/en/#part7-s286-subs3
   - s286(5)(h) lists the "Machinery Act 1950" as a relevant Act: #part7-s286-subs5-h
   - Both Acts were repealed by HSWA s231(1) and (2): https://legislation.docref.nz/health-and-safety-at-work-act-2015/2025-04-05/en/#part5-subpart5-s231-subs1
     (Machinery Act s21A is saved only until the Amusement Devices Regulations 1978 are revoked: #sch1-part1-s2-subs3)
   - The same list has HSWA 2015 at (e) and (a) repealed, so someone updated it partially. Designated agencies are now under HSWA s191: #part5-subpart1-s191-subs1
   - Question for the expert: does Legislation Act 2019 s38(2) cure these references, or should a revision bill or editorial change fix them?

3. **High Court Rules 2016 rr 17.31–17.38 (attachment orders)**: operative references to the Social Security Act 1964
   - https://legislation.docref.nz/high-court-rules-2016/2026-09-04/en/#part17-subpart4-s17.35-subs4 "Section 84 of the Social Security Act 1964 does not apply to an attachment order under this rule."
   - Also #part17-subpart4-s17.31-defn3-f, #part17-subpart4-s17.35-subs1-e, #part17-subpart4-s17.36-subs2-b, #part17-subpart4-s17.38-subs5
   - Repealed by SSA 2018 s455: https://legislation.docref.nz/social-security-act-2018/2026-09-26/en/#part8-s455-subs1
   - Question for the expert: which SSA 2018 provisions correspond (for s38(2) purposes), and is the mapping clear enough that the rules still work?

4. **Building Act 2004 s423(3)**: report to be presented "under section 44A of the Public Finance Act 1989"
   - https://legislation.docref.nz/building-act-2004/2026-10-08/en/#part5-subpart4-s423-subs3
   - PFA s44A is repealed: https://legislation.docref.nz/public-finance-act-1989/2026-09-04/en/#part4-s44A-repealed2-title
   - Likely a spent transitional provision from the Building Industry Authority wind-up. A candidate for tidy-up, not a live risk.

5. **Radiocommunications Act 1989 ss145–147 and 171**: references to "section 95(2) of the Broadcasting Act 1989"
   - e.g. https://legislation.docref.nz/radiocommunications-act-1989/2026-09-23/en/#part16-s146-subs1-b-ii
   - Broadcasting Act s95 is "[Repealed]": https://legislation.docref.nz/broadcasting-act-1989/2026-09-23/en/#part7-s95-p1
   - Spent transitional provisions (1989 spectrum changeover).

## False positive: why the detector needs to know commencement dates
- RMA s166, "network utility operator" (g)(i), still cites the Airport Authorities Act 1966: https://legislation.docref.nz/resource-management-act-1991/2026-10-01/en/#part8-s166-subs1-defn3-g-i
- This is deliberate. CAA 2023 s488 repeals the 1966 Act only on the fifth anniversary of s487 commencing, and (g)(ii) already covers the new regime: https://legislation.docref.nz/civil-aviation-act-2023/2026-09-23/en/#part10-subpart8-s488-line1
