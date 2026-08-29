# Licence and terms of use — OligoTox-CNS v1.0

## Short version

- Everything **we** created — the schema, the code, the documentation, the figures, and every
  computed or derived field — is released under **Creative Commons Attribution 4.0
  International (CC BY 4.0)**.
- The **row-level scientific content** is curated from published sources, and each row carries
  the terms of the source it came from in its `redistribution` column.
- **2,018 of 2,065 measurements (97.7 %) are CC BY 4.0 or US public domain** and may be reused
  for any purpose, including commercially, with attribution.
- **47 measurements (2.3 %) derive from CC BY-NC sources** and may not be used commercially.
  They are individually marked, and can be excluded with one filter.

Nothing here is behind a registration wall, a data-use agreement, or an access committee. The
files are plain CSV and XLSX.

---

## Why the licence is mixed, and how to work with it

A curated dataset cannot grant rights the underlying publications did not grant. Rather than
either over-claiming (labelling everything CC BY) or under-claiming (labelling everything
non-commercial, which would needlessly restrict 97.7 % of the data), each row states its own
terms.

| `redistribution` | source | rows | what you may do |
|---|---|---|---|
| `cc_by` | H1 — Hagedorn et al. 2022, CC BY 4.0 | 2,006 | any use, including commercial, with attribution |
| `public_domain` | C1 — FDA prescribing information, US Government work | 12 | any use |
| `cc_by_nc` | K1, L1 — CC BY-NC | 47 | non-commercial use only, with attribution |

### To obtain a fully commercially-reusable subset

```python
import csv
rows = list(csv.DictReader(open("data/measurements.csv")))
open_rows = [r for r in rows if r["redistribution"] in ("cc_by", "public_domain")]
# 2,018 of 2,065 measurements, covering 1,827 of 1,839 oligonucleotides
```

The scientific core of the release — all 1,825 sequence-resolved oligonucleotides with paired
in vitro and in vivo readouts — is entirely within the CC BY portion.

---

## Attribution

If you use this dataset, please cite **both** this dataset and the primary sources whose data
you used. `data/sources.csv` carries the full citation, DOI, PMCID and licence for each.

Suggested dataset citation:

> OligoTox-CNS: an open, sequence-resolved dataset of central-nervous-system toxicity for
> oligonucleotide therapeutics, v1.0. Assembled for the NIH/NCATS Oligonucleotide Toxicity
> Open Data Challenge, Phase 2.

The single largest contributing source, and the one any user of this dataset must cite:

> Hagedorn PH, Brown JM, Easton A, Pierdomenico M, Jones K, Olson RE, Mercer SE, Li D, Loy J,
> Høg AM, Jensen ML, Gill M, Cacace AM. Acute Neurotoxicity of Antisense Oligonucleotides After
> Intracerebroventricular Injection Into Mouse Brain Can Be Predicted from Sequence Features.
> *Nucleic Acid Therapeutics*. 2022 Jun;32(3):151–162. doi:10.1089/nat.2021.0071.
> PMID 35166597. PMC9221153. Licensed CC BY 4.0.

---

## Disclaimer

This is a research dataset assembled from published literature and regulatory documents. It is
not medical advice, not a regulatory submission, and not a substitute for reading the primary
sources. All severity grades are **provisional** and await subject-matter-expert review; see
`OPEN_ITEMS.md`. Where a value was not published, it is marked `NOT_REPORTED` rather than
estimated — users should treat those fields as genuinely unknown, not as zero.

Full CC BY 4.0 text: https://creativecommons.org/licenses/by/4.0/legalcode
Full CC BY-NC 4.0 text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
