# Research staging — NOT validated data

Everything in this folder was acquired or derived during the **2026-10-02 research round**
(`BEEBOP_RESEARCH_REQUEST_2026-10-02.md`). It is deliberately held **outside** `../data/`.

- Nothing here has been merged into `data/measurements.csv`, `data/oligos.csv` or any register.
- No validated label, grade, eligibility class or model was changed to produce it.
- `trial_verification_2026-10-02.csv` records what a primary source **says**, alongside what the
  current row claims, and a `verification_outcome`. It is evidence for a future authorized
  reconciliation, not a replacement table.
- Proposed sequence or purity values, where any exist, are **proposals pending German's
  adjudication** — they are not promoted into `oligos.csv` by this round.

## Contents

| Path | What it is |
|---|---|
| `papers/` | Primary sources retrieved through lawful open routes. **Not committed** — see `papers/.gitignore`; the manifest carries URL + SHA-256 so any reader can re-fetch the identical bytes |
| `logs/acquisition_manifest.json` | Per-file URL, retrieval date, HTTP code, byte size, SHA-256 |
| `logs/search20_log.json` | The 20-resource coverage log, machine-readable |
| `logs/repository_targeted_hits.json` | Per-compound hit counts across GEO / SRA / BioStudies / Zenodo |
| `trial_verification_2026-10-02.csv` | Extracted trial facts vs current row claims |

## Provenance of retrieved files

All retrievals used the public REST/HTTP endpoints named in the manifest, over this
environment's standard proxy. No credentials, logins, subscriptions or purchases were used,
and no author or sponsor was contacted.
