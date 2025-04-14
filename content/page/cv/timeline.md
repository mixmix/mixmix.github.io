# Timeline

This is the raw mermaid code used to generate SVGs

Process:
1. edit in hackmd.io/new
2. copy raw rendered SVG from DOM
3. format pretty with https://codebeautify.org/svg-formatter-beautifier
4. save as SVG
5. tweak any inline styles


```mermaid 
gantt
  title 2000s
  dateFormat YYYY-MM-DD
  axisFormat %Y
  tickInterval 12month
  
  start                    :milestone, 2000-01-01, 0d
  Section University
    Neuroscience             :done, 2002-01-01, 18M
    Maths                    :done, maths, 2002-01-01, 4y
    Physics                  :done, 2003-07-01, 30M
    BSc Hons. Maths          :milestone, after maths, 0D

    Research                 :done, 2006-01-01, 1y

    TCol                     :done, tcol, 2007-01-01, 1y
    Post Grad. Dip. Teaching :milestone, after tcol, 0d

  Section Teaching
    Unlimited Paenga Tawhiti :done, 2008-01-01, 2y
```

```mermaid
gantt
  title 2010s
  dateFormat YYYY-MM-DD
  axisFormat %Y
  tickInterval 12month
  
  Section Teaching
    Unlimited Paenga Tawhiti :done, 2010-01-01, 2y
    Ensipiral Dev Academy    :done, after ae, 2017-04-30
  
  Section University
    Fine Arts                :done, 2012-01-01, 1y
  
  Section Social Ent.
    Loomio                   :done, 2013-01-01, 2015-07-01
    Cobudget                 :done, 2014-05-01, 9M

    POC21                    :done, 2015-09-01, 2M
    Scuttlebutt              :active, 2015-10-01, 2020-01-01
    
  
    Protozoa                 :active, 2017-05-01, 2020-01-01
    Dark Crystal             :done, 2018-07-01, 6M
    ScuttleCamp              :done, 2018-12-05, 2019-03-10
    Ahau                     :active, 2019-01-01, 1y

    Dweb DEI                 :done, 2019-04-11, 2019-08-20
  
  Section Contracting
    Spanner Planner          :done, 2014-06-01, 8M
    WebPunch                 :done, 2015-01-01, 8M
    Accredited Employer      :done, ae, 2015-10-01, 8w
    Civic Dinners            :done, 2017-05-01, 2017-07-30
```

```mermaid 
gantt
  title 2020s
  dateFormat YYYY-MM-DD
  axisFormat %Y
  tickInterval 12month
  
  Section Social Ent.
    Scuttlebutt              :active, 2020-01-01, until last_updated
    Protozoa                 :active, 2020-01-01, until last_updated
    Ahau                     :active, ahau, 2020-01-01, 2024-06-01
    Ahau -> Matou            :milestone, after ahau, 0d
    Matou                    :active, after ahau, until last_updated    
    
    Manyverse, NGI          :done, 2022-05-01, 2023-10-06
    Dweb Scholarships        :done, 2022-06-10, 2022-09-16
    Planetary                :done, 2022-06-23, 6M

    Decent Social            :done, 2024-01-01, 2M
    Dweb Weaving             :done, 2024-06-01, 3M
    Beautiful Signals        :done, 2024-11-01, 2M

  Section Contracting
    Open Measures            :done, 2020-01-01, 6M
    Open Measures            :done, 2022-03-14, 2023-01-10
    
    Entropy                  :done, 2024-05-01, 2025-02-01
    
    
    last updated             :milestone, last_updated, 2025-04-11, 0d
    .                        :milestone done, 2030-01-01, 0d
  ```
