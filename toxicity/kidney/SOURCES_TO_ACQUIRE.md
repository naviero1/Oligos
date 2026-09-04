# Sources I could not retrieve — direct download links

Ranked by what each closes. Every link is direct; nothing needs searching.

---

## A. Open access, free — blocked only by NCBI's bot detection (11 papers)

**These open normally in a browser.** I could not fetch them from this environment because
NCBI serves an anti-automation stub to scripted requests, but there is no paywall. They are
the highest-value items here: all 11 sit behind rows currently flagged `WS` (cited but not
read), and retrieving them is what converts those rows from unverified to sourced.

| # | Paper | Closes | Link |
|---|---|---|---|
| 1 | Crooke et al. 2018 — pooled 2′-MOE ASO human renal safety | `MSR058` | https://pmc.ncbi.nlm.nih.gov/articles/PMC5790433/ |
| 2 | Clin. Kidney J. — pelacarsen | `MSR063` | https://pmc.ncbi.nlm.nih.gov/articles/PMC7577764/ |
| 3 | SEQUOIA — fazirsiran | `MSR078` | https://pmc.ncbi.nlm.nih.gov/articles/PMC12369710/ |
| 4 | CJASN 2024 — cemdisiran in IgA nephropathy | `MSR066` | https://pmc.ncbi.nlm.nih.gov/articles/PMC11020434/ |
| 5 | PHYOX3 — nedosiran | `MSR046` | https://pmc.ncbi.nlm.nih.gov/articles/PMC11068990/ |
| 6 | Pegaptanib review | `MSR049` | https://pmc.ncbi.nlm.nih.gov/articles/PMC11944999/ |
| 7 | Bepirovirsen / B-Clear | `MSR068` | https://pmc.ncbi.nlm.nih.gov/articles/PMC9804925/ |
| 8 | PROMOVI — eteplirsen | `MSR040` | https://pmc.ncbi.nlm.nih.gov/articles/PMC8673535/ |
| 9 | Revusiran nonclinical safety (NAT 2019) | revusiran rows | https://pmc.ncbi.nlm.nih.gov/articles/PMC6987735/ |
| 10 | Janas et al. 2018 — GalNAc-siRNA nonclinical, Toxicol. Pathol. | `OLG030` panel, 3 rows | https://pmc.ncbi.nlm.nih.gov/articles/PMC6249674/ |
| 11 | Janas et al. 2019 — siRNA safety, NAR | `OLG030` panel | https://pmc.ncbi.nlm.nih.gov/articles/PMC6468299/ |

**Tip:** on each page use the *Download PDF* link in the sidebar. The bare
`…/PMC…/pdf/` URL returns a stub.

---

## B. Paywalled — need institutional access (10 documents)

For each of these, **the safety tables and supplementary appendix are what matter**, not the
main text. Renal lab-shift tables live in the appendix; the main text usually just says "well
tolerated", which is the sentence that created the verification problem in the first place.

| Paper | Closes | Link |
|---|---|---|
| Mongersen, NEJM 2015 | `MSR056` | https://doi.org/10.1056/NEJMoa1407250 |
| OCEAN(a)-DOSE olpasiran, NEJM 2023 | `MSR065` | https://doi.org/10.1056/NEJMoa2211023 |
| Donidalorsen, NEJM 2024 | `MSR067` | https://doi.org/10.1056/NEJMoa2402478 |
| Teprasiran, Circulation 2021 | `MSR077` | https://doi.org/10.1161/CIRCULATIONAHA.120.053029 |
| TRANSLATE-TIMI 70 vupanorsen, Circulation 2022 | `MSR079` | https://www.ahajournals.org/journal/circ |
| APOLLO patisiran, NEJM 2018 | `MSR044` | https://doi.org/10.1056/NEJMoa1716153 |
| VALOR tofersen, NEJM 2022 | `MSR042` | https://doi.org/10.1056/NEJMoa2204705 |
| Tsimikas pelacarsen Ph2, NEJM 2020 | `MSR063` | https://doi.org/10.1056/NEJMoa1905239 |
| Yu et al. 2012, *Toxicology* — ISIS 113715 monkey | `OLG025` sequence + row | https://doi.org/10.1016/j.tox.2012.06.014 |
| Alicaforsen review, ScienceDirect | `OLG027` context | search ScienceDirect for "alicaforsen review" |

**HELIOS-A (vutrisiran, `MSR047`)** and the **ATLAS trials (fitusiran, `MSR055`)** are also
needed; both were published outside the journals above — please locate whichever version your
institution can reach.

---

## C. FDA Pharmacology/Toxicology reviews — closes 39 missing doses

`accessdata.fda.gov` is blocked from this environment entirely. From **Drugs@FDA**
(https://www.accessdata.fda.gov/scripts/cder/daf/), download the **Pharmacology Review(s)**
and **Multi-disciplinary Review** PDFs for:

`210922` patisiran · `215515` vutrisiran · `215887` tofersen · `217388` eplontersen ·
`219019` fitusiran · `212154` viltolarsen · `211970` golodirsen · `213026` casimersen ·
`211172` inotersen

These are the only public source for animal NOAELs and renal lab tables. **The labels alone
will not do** — I already have those; they give findings without doses.

---

## D. One citation that is broken regardless

`MSR064` (zilebesiran) records its source as **`KARDIA_trials`**, which is not a resolvable
citation. It needs a real reference — presumably KARDIA-1 (JAMA 2024) or KARDIA-2 — before
that row can be verified by anyone.

---

## Priority, if you only chase some

1. **Section A** — free, 11 papers, closes the largest block of unverified rows.
2. **Section C** — the only route to 39 missing doses.
3. **Section B** — the remaining unverified clinical rows.
4. **Section D** — one broken citation, quick to fix.
