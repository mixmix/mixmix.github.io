---
title: Loose Ends
date: 2026-11-16T15:00:00+13:00
image: loose-ends.jpg
---

In January Estonia passed a gambling tax amendment that left out one word and accidentally made online
casinos tax-free for a year. Luukas Ilves (their former government CIO) gave the amendment and the Act
it changed to a couple of LLMs, and both spotted the gap straight away. Within a day he'd built
_Apsakaleidja_ ("mistake finder"), which checks every bill going through their parliament. The step he
hadn't got to yet was checking new law against _existing_ law.

docref seemed like a good place to try that for New Zealand. Every provision has a stable address, so
"section 73 of the Electricity Industry Act 2010" can be resolved to an actual block of text and checked.

{{< embed src="statute-book-loose-ends.embed.html" title="Statute Book Loose Ends" preview="loose-ends.jpg" >}}

I asked Claude to run five simple detectors over the 70 Acts and regulations on docref. They look for
references to repealed or non-existent sections, mentions of Acts the corpus says are repealed, borrowed
definitions that point at the wrong section, and drift between versions. The detectors flagged 433
suspects. Claude then read each one and sorted it into real error, cured by the Legislation Act's
"references to repealed legislation" rule, deliberate transitional wording, or noise. 13 held up, ranked
by confidence. Each one can be walked through from the citing provision to what it actually points at,
with links to the pinpoint on docref.

My favourites:

- the Gas Act still gives powers to an "Energy Commission" that lives in a subpart that isn't there
- the Regulatory Standards Act 2025 overrides a Public Service Act section that was repealed about six
  months after it passed

Most of these are loose ends rather than true contradictions, but they're objective, and someone who
knows the area can check each one in a few minutes. That seems like the right first test of whether this
approach finds real things. The next step would be getting an expert to check them, then aiming the same
pairwise review at harder cases where two live provisions actually conflict.

The prompts, methodology, scripts and raw results are snapshotted in the
[method folder](https://github.com/mixmix/mixmix.github.io/tree/master/content/experiment/docref/2026_11_16-loose-ends/method)
if you want to check the working or run it again.
