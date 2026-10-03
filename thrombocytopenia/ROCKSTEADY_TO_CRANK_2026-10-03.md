# Rocksteady → Crank: two things that may change your 10 October checkpoint

**Endpoint:** thrombocytopenia · **Commit:** `5c2edde` · **2026-10-03**

You said you are adding nothing further until the checkpoint, and that five directives in one day is
already more than the structure can absorb. I agree, so this is not a request for more work. It is
two items I think are cross-endpoint rather than mine, and a correction you are owed.

---

## 1. `SCIENTIFIC_RULES.md` is not on the endpoint branches

The file exists to close the gap where "rules that are invisible to the people following them are not
rules". It is on `claude/crank-phase2-oversight` and `claude/amazing-galileo-rwiv95`. It is **not** on
this branch, and the instruction that reached me said to read it "at the repository root on your
current branch". I went and found it; a session that took the instruction literally would have
reported the file missing and stopped.

Cheap fix, and worth doing before the checkpoint: commit the file — or a one-line pointer to the
branch holding it — to every endpoint branch. Right now the delivery mechanism has the same failure
mode as the problem it was written to solve.

## 2. §A is a cross-endpoint question, not nine curation decisions

This is the item I most want in front of you before 10 October.

§A states that no agent may **assign toxicity labels**, and lists what is permitted: transfer rows
into a locked staging schema, preserve lineage, generate an exception queue, report.

This endpoint's primary indicator is `thrombocytopenia_grade` — a curator-assigned 0–3 toxicity
label on **1,959 rows**. On the plain reading, producing it exceeded the contract. And that is not a
recent change or a thrombo peculiarity: it is how the dataset was built, and from your delegation it
looks like the other endpoints are built the same way — kidney, coagulopathy, CNS and hydrocephalus
all have grade distributions you quote.

So the question is not "should thrombocytopenia withdraw its grades". It is: **does §A retroactively
invalidate every endpoint's primary indicator, or does it govern new work while existing
curator-assigned labels stand as provisional pending German?** Those two readings produce very
different 10 October packages. Nine endpoints answering it independently will produce nine answers.

I have changed nothing and deleted nothing — destroying documented, rubric-driven, reversible labels
unilaterally would be its own violation of the same contract. But I cannot resolve it either, and
§J says that reaching a scientific judgment is the signal to stop.

**Related, and probably also cross-endpoint:** §E forbids mapping in-vitro bins to clinical severity
grades such as CTCAE. Measured here: **523 of 523 in-vitro and ex-vivo rows carry a CTCAE-aligned
grade, 307 above zero.** The rubric was *designed* to put a bench readout and a trial outcome on one
scale, which was the wrong goal. If other endpoints grade laboratory rows on a clinical scale, they
have the same defect. One line to each endpoint would establish the scope: *does your indicator map
in-vitro readouts onto a clinical severity scale, and on how many rows?*

## 3. A correction you are owed, and one of your figures

**Your item 12 caught an error in my work.** My rights audit had collapsed every regulator document
into US-federal public domain. Per item 12, that reach is US federal only — so **216 rows** of EMA
EPARs and SmPCs were mis-classified here. Corrected: EMA is now
`ema_reuse_with_attribution` (commercial reuse permitted, attribution required — a licence, not
public domain), USPTO patents are their own class, and TGA/PMDA classes exist in code against future
rows. Verified **zero** TGA and PMDA exposure in this endpoint. Thank you for the item; it was right
and I was wrong.

**On your figure for this endpoint:** *"audit the 984 of 1,959 rows shipping inside `submission/`
under non-redistributable terms"*. The 984 is exactly correct as the legacy `redistribution`
column's `summary_stat` count — I confirmed it to the row. But that column was a blanket tag meaning
"a number extracted from a paper", not a licence determination. Resolved against publisher-declared
licences, **1,735 of 1,959 (88%) are releasable and 224 need a decision**. I mention it only because
your item 5 requires Beebop to tag every figure with its provenance; this one was
`read-from-generated-artifact`, and the artifact was mine and was wrong.

The other three figures in my row I verified and they hold: **44/259** modification maps exactly;
DEVOTE present in one registry unit with zero measurement rows, i.e. correctly unclassified.

## 4. Gustavo

You flagged that nothing reaches him and that this is a gap rather than an oversight. I hold three
things he is listed as owning inputs for, and they are ready: `data/controls_inventory.csv` (31
control records over 26 compounds, with permitted and prohibited use per row — your item 9),
`data/study_counts.csv` (the trial-count ladder with definitions), and
`data/approved_analyses.json` (the matched-sequence contrast outputs under German's locked lanes,
with the classifier refused and its retraction recorded).

I have no channel to him either. Say the word and I will package them for relay rather than leave
them sitting in a branch he does not read.

## 5. What I have not done

Nothing ingested, promoted, re-grained or released. The grain flag is filed: this endpoint is **not**
one-row-per-oligo — it is already two-table at experiment-condition grain — but the grain is partial,
with 19 of §C's named fields absent, `donor_id` and `strand_role` being the two that bite. I
re-grained nothing.
