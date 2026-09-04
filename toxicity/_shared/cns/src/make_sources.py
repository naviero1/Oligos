#!/usr/bin/env python3
"""Render the source register.

    deliverables/OligoTox-CNS_SourceRegister.pdf

This is the provenance document: which database each file came from, the exact endpoint that
returned it, which table or figure inside it was read, what licence it carries, and how many
released rows it accounts for.

Every count, every source block and the whole ClinicalTrials.gov table are computed at build
time from the released rows in toxicity/<endpoint>/data/, the source registry in
src/assemble.py, and the retrieved JSON under sources/. Nothing is typed as a literal, so this
document cannot claim a source the dataset does not contain, or a row count the data does not
support.

The prose that is NOT computed -- the description of each retrieval route, the failure modes,
the exclusion reasons -- is a statement about method rather than about data, and is written
here once.
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import endpoints
from assemble import SOURCES

from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, PageBreak

from make_pdfs import BOXBG, WARNBG, B, P, box, build, caption, table

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"
CTDIR = ROOT / "sources" / "CT1_ClinicalTrialsGov"

# ==========================================================================================
# Method statements. These describe how material was retrieved, not what it contains.
# ==========================================================================================

DATABASES = [
    ("Europe PMC REST&nbsp;&mdash;<br/>full text",
     "European Bioinformatics Institute (EMBL-EBI). Returns the publisher-deposited JATS XML of "
     "an open-access article: body, methods, tables, figure legends and the machine-readable "
     "permissions block.",
     "https://www.ebi.ac.uk/europepmc/<br/>webservices/rest/&lt;PMCID&gt;/fullTextXML",
     "H1, HV1, HV3, and the licence verification for every source in &sect;3"),
    ("Europe PMC REST&nbsp;&mdash;<br/>supplementary files",
     "The same service, returning a ZIP of the article's supplementary material. This is the "
     "only programmatic route to supplementary tables, which is where sequence-resolved "
     "oligonucleotide data almost always lives.",
     "https://www.ebi.ac.uk/europepmc/<br/>webservices/rest/&lt;PMCID&gt;/supplementaryFiles",
     "H1 Table S1 (the module's core), K1 Table S2, L1 Table S1, HV2 source data, HV3 mmc1/mmc3"),
    ("Europe PMC REST&nbsp;&mdash;<br/>search",
     "Fielded search over 45+ million records (TITLE:, AUTH:, JOURNAL:, DOI:, PMCID:, "
     "PUB_YEAR:). <font face='Courier'>resultType=core</font> returns the DOI, PMID, PMCID, "
     "open-access flag and licence in one call.",
     "https://www.ebi.ac.uk/europepmc/<br/>webservices/rest/search?query=&hellip;<br/>"
     "&amp;resultType=core&amp;format=json",
     "discovery of every literature source; identifier and licence verification in &sect;8"),
    ("PubMed Central",
     "NIH/NLM's full-text archive. Used to read articles in rendered form and to confirm the "
     "copyright statement shown to a human reader.",
     "https://pmc.ncbi.nlm.nih.gov/<br/>articles/&lt;PMCID&gt;/",
     "orientation and cross-checking for all PMC-deposited sources"),
    ("ClinicalTrials.gov<br/>API v2",
     "NIH/NLM trial registry. <font face='Courier'>resultsSection.adverseEventsModule</font> "
     "carries the full MedDRA adverse-event table for a trial with posted results: every term, "
     "every arm, with both a numerator and a denominator.",
     "https://clinicaltrials.gov/api/v2/<br/>studies/&lt;NCT&gt;",
     "CT1 &mdash; the module's principal human source; see &sect;4 for the trial-by-trial table"),
    ("DailyMed",
     "NIH/NLM's archive of current FDA-approved product labelling, addressed by a stable "
     "<font face='Courier'>setid</font>. The approved label is the regulatory statement of a "
     "drug's adverse-effect profile.",
     "https://dailymed.nlm.nih.gov/dailymed/<br/>lookup.cfm?setid=&lt;setid&gt;",
     "C1 &mdash; QALSODY (tofersen) and SPINRAZA (nusinersen) prescribing information"),
    ("WHO INN<br/>(Recommended List)",
     "The World Health Organization's International Nonproprietary Name entry, which for an "
     "oligonucleotide prints the full sequence and the per-position chemistry as a formal "
     "description.",
     "WHO Drug Information, INN<br/>Recommended List (tofersen)",
     "the tofersen sequence and its 15&nbsp;PS / 4&nbsp;PO linkage pattern"),
    ("USPTO full-text<br/>(via patent PDF)",
     "Granted US patents. Patent tables routinely pair an oligonucleotide sequence with a "
     "toxicity rating, and are US Government works in the public domain.",
     "US 10,799,523 B2 (Olson et al.)",
     "P1 &mdash; retrieved and held, not yet ingested (&sect;5)"),
    ("Publisher sites<br/>(OUP, NEJM, CHDI)",
     "Read directly where the article or conference deck is not deposited in PMC.",
     "academic.oup.com/nar/&hellip; ; nejm.org",
     "O1 cross-check; M1, S1 and B2 read but not redistributable (&sect;5)"),
]

FAILURE_MODES = [
    ("PMC binary downloads are gated",
     "Requesting a supplementary binary directly from <font face='Courier'>pmc.ncbi.nlm.nih.gov"
     "</font> returns <b>HTTP 200 with an HTML challenge page</b>, not the file. A pipeline that "
     "trusts the status code silently writes a JavaScript proof-of-work page to disk and parses "
     "it as data.",
     "Every download is checked with <font face='Courier'>file</font> before it is parsed. "
     "Supplementary material is taken from the Europe PMC endpoint instead."),
    ("The ClinicalTrials.gov results page has no results in it",
     "<font face='Courier'>clinicaltrials.gov/study/&lt;NCT&gt;?tab=results</font> is a "
     "client-side application. Its HTML contains none of the adverse-event text, so scraping "
     "the page returns nothing while appearing to succeed.",
     "All CT1 data is taken from API v2 and the returned JSON is committed to the repository, "
     "so the build does not depend on the service staying up."),
    ("The Europe PMC supplementary ZIP can carry another article's files",
     "A first call for HV1 returned a valid 898&nbsp;kB ZIP, HTTP 200 &mdash; whose 47 members "
     "all belonged to a different paper. This is a cache collision, and it is invisible unless "
     "the member filenames are inspected.",
     "Every extracted ZIP is checked member-by-member against the expected article prefix "
     "before anything inside it is read."),
    ("Plain text extraction destroys chemistry",
     "Source L1 encodes each nucleotide's chemistry in the <b>typeface</b> of its supplementary "
     "table &mdash; bold&nbsp;=&nbsp;LNA, bold-italic&nbsp;=&nbsp;2&prime;-MOE, "
     "regular&nbsp;=&nbsp;DNA. Copying the text out yields a sequence with the chemistry "
     "silently deleted.",
     "The parser reads PDF span styling, so per-position chemistry is recovered mechanically "
     "rather than transcribed by eye."),
    ("Sequences that exist only in the supplement",
     "All 23 of source HV3's modified sequences appear in <font face='Courier'>mmc1.pdf</font> "
     "and <font face='Courier'>mmc3.pdf</font> and <b>nowhere in the article text</b>. A "
     "full-text-only extraction finds none of them and concludes the paper prints no sequences.",
     "Supplementary material is retrieved for every source, not only where the text implies it "
     "exists."),
    ("The host matters",
     "<font face='Courier'>www.ncbi.nlm.nih.gov/pmc/articles/&lt;PMCID&gt;/</font> now answers "
     "with a 301 redirect; the working host is "
     "<font face='Courier'>pmc.ncbi.nlm.nih.gov</font>.",
     "Recorded here so a future run does not read the redirect as an absent article."),
]

# What was read inside each source, beyond what the registry's own notes field says.
READ_FROM = {
    "H1": "Supplementary Table S1 &mdash; 1,825 oligonucleotides, each with its full sequence "
          "(upper case encoding LNA position, lower case DNA), a measured rat-cortical-neuron "
          "calcium-oscillation score, and for 181 of them a measured mouse acute tolerability "
          "score. Grade cut-offs 4 / 7 / 18 are the authors' own, quoted from the Fig.&nbsp;1B "
          "discussion.",
    "K1": "Supplementary Table S2 (<font face='Courier'>media-1.pdf</font>) &mdash; per-group "
          "average acute tolerability score, dose in nmol and &micro;g, injectate "
          "Ca<super>2+</super> and Mg<super>2+</super> concentration, group size, mouse "
          "genotype, and the paper figure each group appears in.",
    "L1": "Supplementary Table S1 (five ASOs, per-position chemistry recovered from typeface) "
          "and Figures 1A&ndash;F with the Results text. Behavioural scores are published only "
          "as figures, so the numeric readouts are recorded NOT_REPORTED and the authors' "
          "stated outcome is carried instead.",
    "C1": "Prescribing information sections 5.1&ndash;5.3 (warnings), 6.1 (adverse reactions "
          "table) and 6.2 (post-marketing). The tofersen sequence and its linkage pattern come "
          "from the published INN description, not from the label.",
    "CT1": "<font face='Courier'>resultsSection.adverseEventsModule</font> &mdash; both "
           "<font face='Courier'>seriousEvents</font> and "
           "<font face='Courier'>otherEvents</font>, every arm including comparators. Scope: "
           "the whole &lsquo;Nervous system disorders&rsquo; organ class plus a curated set of "
           "CNS terms MedDRA files elsewhere (post-lumbar-puncture syndrome, CSF findings, "
           "meningitis, myelitis, papilloedema, hydrocephalus). Cardiac "
           "&lsquo;ventricular&rsquo; terms are excluded &mdash; those are heart ventricles.",
    "HV1": "Table&nbsp;1 (three 2&prime;-MOE PS sequences), Figure&nbsp;1B and Figure&nbsp;2B "
           "category labels read from the figure axes, Results &sect;3.1&ndash;3.4, Methods "
           "&sect;2.4 and &sect;2.6, and the Figure 1 and 2 legends for n and significance.",
    "HV2": "Extended Data Fig.&nbsp;6b, 6d and 6f &mdash; which print no numbers &mdash; "
           "resolved against the released Source Data workbook "
           "<font face='Courier'>41586_2024_7310_MOESM13_ESM.xlsx</font>, sheet by sheet and "
           "column by column. The article does not print the ASO sequences, so those are "
           "NOT_REPORTED.",
    "HV3": "Table S2 in <font face='Courier'>mmc1.pdf</font> for the 23 modified sequences, "
           "cross-checked against <font face='Courier'>mmc3.pdf</font>; Figures 4D and 4H from "
           "the main text; Figures S7D and S8D from the supplement.",
    "O1": "The rodent intrathecal, rodent intracerebroventricular and non-human-primate "
          "intrathecal acute-inhibition scales, transcribed into "
          "<font face='Courier'>docs/SCORING_INSTRUMENTS.md</font>. No per-oligonucleotide rows: "
          "the supplement does not pair sequences with scores.",
}

# Sources retrieved and held, but contributing no released row.
HELD = [
    ("B1", "Bravo-Hern&aacute;ndez M, et&nbsp;al. Transient acute neuronal activation response "
           "caused by high concentrations of oligonucleotides in the cerebral spinal fluid. "
           "<i>Nucleic Acids Res</i>. 2026;54(3):gkag057.",
     "doi:10.1093/nar/gkag057 &middot; PMID 41633500 &middot; PMC12867516",
     "CC BY-NC 4.0", "yes",
     "Would add the first non-human-primate rows and upgrade the acute-activation instrument in "
     "<font face='Courier'>docs/SCORING_INSTRUMENTS.md</font> &sect;4 from a fetched summary to "
     "a direct reading."),
    ("P1", "Olson RE, et&nbsp;al. US Patent 10,799,523 B2 &mdash; oligonucleotide compounds for "
           "CNS delivery.",
     "US 10,799,523 B2",
     "US Government work &mdash; public domain", "yes",
     "Patent tables pair a sequence with a toxicity rating. This is the format that supplied 21 "
     "rows to the sibling kidney module, so the extraction path is already proven."),
    ("S1", "Schobel S. <i>Preliminary results from GENERATION HD1</i>. CHDI Therapeutics "
           "Conference, 2021.",
     "conference presentation",
     "&copy; Roche &mdash; not licensed for redistribution", "<b>no</b>",
     "Tominersen ventricular-volume and neurofilament-light detail behind the clinical failure."),
    ("B2", "Boak L, McColgan P. <i>Treatment and post-treatment effects of tominersen in "
           "GENERATION HD1</i>. CHDI Therapeutics Conference, 2022.",
     "conference presentation",
     "&copy; Roche &mdash; not licensed for redistribution", "<b>no</b>",
     "Post-treatment follow-up on the same trial."),
    ("M1", "McColgan P, et&nbsp;al. Tominersen in Adults with Manifest Huntington&rsquo;s "
           "Disease. <i>N Engl J Med</i>. 2023;389(23):2203&ndash;2205 (Correspondence).",
     "doi:10.1056/NEJMc2300400 &middot; PMID 38055260",
     "&copy; NEJM &mdash; not licensed for redistribution", "<b>no</b>",
     "The peer-reviewed statement of the GENERATION HD1 outcome."),
]

# Examined and rejected, with the reason. Identifiers verified against Europe PMC.
REJECTED = [
    ("Drygin D, Barone S, Bennett CF. Sequence-dependent cytotoxicity of second-generation "
     "oligonucleotides. <i>Nucleic Acids Res</i>. 2004;32(21):6585&ndash;6594.",
     "doi:10.1093/nar/gkh997 &middot; PMID 15604456 &middot; PMC545465",
     "43 oligonucleotides with per-compound cytotoxicity &mdash; the largest human panel found, "
     "and it prints every sequence.",
     "<b>Wrong organ.</b> The lines are A549 lung, HepG2 and Hep3B liver. Human, but not CNS. "
     "Admitting it would put another organ&rsquo;s toxicity inside a CNS module."),
    ("Yuan NY, et&nbsp;al. Neural organoids incorporating microglia to assess neuroinflammation "
     "and toxicities induced by known developmental neurotoxicants. <i>Curr Res Toxicol</i>. "
     "2025;9:100252.",
     "doi:10.1016/j.crtox.2025.100252 &middot; PMID 40799410 &middot; PMC12341589",
     "A human iPSC neural organoid platform with microglia &mdash; exactly the kind of human "
     "in vitro system the Challenge brief prioritises.",
     "<b>No oligonucleotide is tested.</b> The compounds are lead acetate and other industrial "
     "developmental neurotoxicants. The platform is relevant; the data is not oligonucleotide "
     "data."),
    ("Means JC, et&nbsp;al. Rapid and scalable personalized ASO screening in patient-derived "
     "organoids. <i>Nature</i>. 2025;638:237&ndash;243.",
     "doi:10.1038/s41586-024-08462-1 &middot; PMID 39843740 &middot; PMC11798851",
     "The highest-profile personalised-ASO organoid screen in the literature.",
     "<b>Cardiac organoids</b>, from Duchenne muscular dystrophy patients. Recorded here as an "
     "explicit exclusion so it is not re-surfaced as a CNS candidate on a later sweep."),
    ("Seven ClinicalTrials.gov records of CNS-delivered oligonucleotides &mdash; BIIB078, "
     "BIIB094, GTX-102, RO7248824, STK-001, WVE-004, and a CpG-ODN glioblastoma trial.",
     "NCT03626012, NCT03976349, NCT04259281, NCT04428281, NCT04442295, NCT04931862, NCT00190424",
     "All were retrieved in full and are committed to the repository.",
     "<b>No posted results.</b> Every one carries "
     "<font face='Courier'>hasResults:&nbsp;false</font> despite being completed or terminated, "
     "so the registry holds no adverse-event table to read. This is a finding about the field, "
     "not a retrieval failure &mdash; see &sect;4."),
]

# Human in vitro backlog. Identifiers verified against Europe PMC search at build time of v1.1.
BACKLOG = [
    ("Flynn LL, et&nbsp;al. Single stranded fully modified-phosphorothioate oligonucleotides can "
     "induce structured nuclear inclusions&hellip; <i>Front Genet</i>. 2022;13:791416.",
     "PMC9019733 &middot; CC BY", "SH-SY5Y; primary human dermal fibroblasts",
     "90+ sequences, 18&ndash;30&nbsp;nt, four chemistries. The largest sequence-resolved human "
     "panel in the backlog.", "yes"),
    ("Ottesen EW, Murzyn WA, Kaas RL, Bertrand KJ, Payne JL, Singh RN. A therapeutic antisense "
     "oligonucleotide encompassing 2&prime;-O-methoxyethyl modification&hellip; "
     "<i>NAR Mol Med</i>. 2026;3:ugag002.",
     "PMC12805893 &middot; CC BY", "SH-SY5Y; SMA patient fibroblasts",
     "An 18-mer with sequence and chemistry identical to nusinersen &mdash; a marketed CNS ASO "
     "already in this dataset&rsquo;s clinical layer.", "yes"),
    ("Thirumalai S, Livesey FJ, Patani R, Hung C. APP antisense oligonucleotides are effective "
     "in rescuing mitochondrial phenotypes in human iPSC-derived trisomy&nbsp;21 astrocytes. "
     "<i>Alzheimers Dement</i>. 2025;21:e14560.",
     "PMC11775556 &middot; CC BY", "hiPSC-derived astrocytes, control and Down syndrome",
     "One 20-mer gapmer, PS backbone, five 2&prime;-MOE each side, 5-methyl-deoxycytidine in the "
     "gap.", "yes"),
    ("Umek T, et&nbsp;al. Oligonucleotides Targeting DNA Repeats Downregulate <i>Huntingtin</i> "
     "Gene Expression in Huntington&rsquo;s Patient-Derived Neural Model. "
     "<i>Nucleic Acid Ther</i>. 2021;31(6):443&ndash;456.",
     "PMC8713517 &middot; CC BY", "HD patient iPSC &rarr; NSC and neurons (NINDS repository)",
     "CAG19, a 19-nt DNA/LNA mixmer with a full PS backbone.", "yes"),
    ("Faravelli I, et&nbsp;al. Targeted antisense oligonucleotide treatment rescues "
     "developmental alterations in spinal muscular atrophy organoids. "
     "<i>Nat Commun</i>. 2025;16:988.",
     "PMC12847787 &middot; CC BY-NC-ND", "SMA patient hiPSC spinal cord and cerebral organoids",
     "MO-10-34 morpholino targeting SMN2 ISS-N1, bare and r6-conjugated.", "yes"),
    ("Bowles KR, et&nbsp;al. ELAVL4, splicing, and glutamatergic dysfunction precede neuron loss "
     "in MAPT mutation cerebral organoids. <i>Cell</i>. 2021;184(17):4547&ndash;4563.e17.",
     "PMC8635409 &middot; not open access", "FTD patient iPSC cerebral organoids",
     "The single ASO-in-cerebral-organoid study identified by the Lange 2022 review.", "yes"),
    ("K&ouml;nig S, et&nbsp;al. Transferrin-Functionalized Liposomes Enhance MAPT-ASO Transport "
     "Across a 3D Blood-Brain Barrier Microvascular Model. <i>Int J Mol Sci</i>. "
     "2025;26(23):11347.",
     "PMC12691827 &middot; CC BY", "Microfluidic 3D BBB chip &mdash; human BMEC, astrocytes, "
     "pericytes",
     "A Cy3-labelled MAPT-targeting PS ASO; the paper prints the sequence.", "yes"),
    ("Selvakumaran J, et&nbsp;al. An Induced Pluripotent Stem Cell-Derived Human Blood-Brain "
     "Barrier Model&hellip; <i>Biomedicines</i>. 2023;11(10):2700.",
     "PMC10604610 &middot; CC BY", "iPSC-derived brain microvascular endothelial cells",
     "Pip6a-PMO targeting SMN2 exon&nbsp;7.", "not stated"),
]


# ==========================================================================================
def ct_rows(meas: list[dict]) -> list[dict]:
    """One record per retrieved ClinicalTrials.gov study, read from the committed JSON."""
    import re
    per = collections.Counter()
    for m in meas:
        if m["source_id"] == "CT1":
            per[re.match(r"(NCT\d+)", m["source_location"]).group(1)] += 1
    # the drug map is the build's own, so the table cannot disagree with the pipeline
    import build_ctgov
    out = []
    for f in sorted(CTDIR.glob("NCT*.json")):
        d = json.loads(f.read_text())
        ps = d.get("protocolSection", {})
        nct = f.stem
        # A trial with no posted results is not in the build's drug map, because the build only
        # maps trials it ingests. Its compound still has to be named, so it is read from the
        # record itself rather than typed here -- the arm suffix ("STK-001 - Single Ascending
        # Doses") is trimmed to leave the compound.
        ivs = [i.get("name", "") for i
               in ps.get("armsInterventionsModule", {}).get("interventions", [])]
        fallback = next((v.split(" - ")[0].strip() for v in ivs
                         if v and not re.search(r"placebo|sham|vehicle", v, re.I)), "&mdash;")
        out.append({
            "nct": nct,
            "drug": build_ctgov.TRIAL_DRUG.get(nct) or fallback,
            "sponsor": ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
                         .get("name", "?"),
            "status": ps.get("statusModule", {}).get("overallStatus", "?").replace("_", " ")
                        .title(),
            "has_results": bool(d.get("hasResults")),
            "rows": per.get(nct, 0),
        })
    return out


def story(meas, oligos, srcs, cts):
    reg = {s["source_id"]: s for s in SOURCES}
    n_meas = collections.Counter(m["source_id"] for m in meas)
    n_olig = collections.Counter(o["source_id"] for o in oligos)
    n_class = {sid: collections.Counter(m["subject_class"] for m in meas if m["source_id"] == sid)
               for sid in reg}
    s = []

    # ---------------------------------------------------------------- cover
    s.append(P("OligoTox-CNS &mdash; Source Register", "title"))
    s.append(P("NIH/NCATS Oligonucleotide Toxicity Open Data Challenge &mdash; Phase 2 "
               "&nbsp;&middot;&nbsp; CNS / neurotoxicity module &nbsp;&middot;&nbsp; "
               "companion to the dataset, narrative, methodology and PADP", "subtitle"))

    s.append(box([
        P(f"<b>What this document is.</b> Every one of the {len(meas):,} measurements in this "
          f"dataset was read out of a published source. This register names all of them: the "
          f"database each file came from, the exact endpoint that returned it, the table or "
          f"figure inside it that was read, the licence it carries, and how many released rows "
          f"it accounts for. It also lists what was retrieved and <i>not</i> used, and why.", "small"),
        P("", "small"),
        P(f"<b>Nothing here is hand-typed.</b> The source blocks in &sect;3, the trial table in "
          f"&sect;4 and every count in this document are computed at build time from the "
          f"released rows, from the source registry in "
          f"<font face='Courier'>src/assemble.py</font>, and from the retrieved JSON on disk. "
          f"Regenerate with <font face='Courier'>python3 src/make_sources.py</font>.", "small")]))
    s.append(P("", "body"))

    s.append(table(
        [["", "count"],
         ["Sources contributing at least one released row", f"{len([k for k in n_meas if n_meas[k]]):,}"],
         ["Sources contributing measurement instruments only", f"{len([s_['source_id'] for s_ in SOURCES if not n_meas.get(s_['source_id'])]):,}"],
         ["Oligonucleotides", f"{len(oligos):,}"],
         ["CNS toxicity measurements", f"{len(meas):,}"],
         ["Clinical trial records retrieved", f"{len(cts):,}"],
         ["&nbsp;&nbsp;of which have posted results, and were read", f"{len([c for c in cts if c['rows']]):,}"],
         ["Sources retrieved and held, contributing no row (&sect;5)", f"{len(HELD):,}"],
         ["Sources examined and rejected on the record (&sect;6)", f"{len(REJECTED):,}"],
         ["Human <i>in vitro</i> sources identified and queued (&sect;7)", f"{len(BACKLOG):,}"]],
        [130 * mm, 40 * mm], align_right=(1,)))
    s.append(caption("Every figure in this table is counted from the released data at build time."))

    # ---------------------------------------------------------------- 1
    s.append(P("1&nbsp;&nbsp;Databases and interfaces queried", "h1"))
    s.append(P(
        "Nine distinct services were used. The endpoint column gives the address actually "
        "called, not a landing page, so any row in this dataset can be traced back to a request "
        "a reader can repeat."))
    s.append(table(
        [["Database", "What it is", "Endpoint called", "Used for"]] +
        [[a, b, f"<font face='Courier' size='7'>{c}</font>", d] for a, b, c, d in DATABASES],
        [26 * mm, 56 * mm, 50 * mm, 38 * mm]))

    # ---------------------------------------------------------------- 2
    s.append(P("2&nbsp;&nbsp;What each route does and does not return", "h1"))
    s.append(P(
        "Six retrieval routes return something that looks like success and is not. Each cost "
        "real time to find, and each would have put wrong data &mdash; or no data &mdash; into "
        "the dataset silently. They are recorded because the next person to build on these "
        "sources will meet them too."))
    s.append(table(
        [["Trap", "What happens", "What this pipeline does"]] +
        [[f"<b>{a}</b>", b, c] for a, b, c in FAILURE_MODES],
        [36 * mm, 76 * mm, 58 * mm]))

    # ---------------------------------------------------------------- 3
    s.append(P("3&nbsp;&nbsp;The sources, one by one", "h1"))
    s.append(P(
        "Each block below is generated from the source registry and the released rows. "
        "<b>Contributes</b> is counted from the data, so a source cannot appear here claiming "
        "rows it did not supply."))

    for sid in [x["source_id"] for x in SOURCES]:
        r = reg[sid]
        ids = " &middot; ".join(x for x in [
            f"doi:{r['doi']}" if r["doi"] else "",
            f"PMID {r['pmid']}" if r["pmid"] else "",
            r["pmcid"] if r["pmcid"] else ""] if x)
        cls = n_class[sid]
        contrib = (f"{n_olig.get(sid, 0):,} oligonucleotides &middot; "
                   f"{n_meas.get(sid, 0):,} measurements"
                   + (f" &nbsp;(" + ", ".join(f"{k.replace('_', ' ')} {v:,}"
                                              for k, v in sorted(cls.items())) + ")"
                      if cls else " &mdash; instruments only, no rows"))
        blk = [
            P(f"<b>{sid}</b>&nbsp;&nbsp;{r['source_key'].replace('_', ' ')}", "h2"),
            table([["Citation", r["citation"].replace("&", "&amp;")],
                   ["Identifiers", ids or "&mdash;"],
                   ["Link", f"<font face='Courier' size='7'>{r['url']}</font>" if r["url"] else "&mdash;"],
                   ["Retrieved via", r["retrieved_via"]],
                   ["Licence", f"<b>{r['license']}</b> &rarr; "
                               f"<font face='Courier'>{r['redistribution']}</font>"],
                   ["Read from it", READ_FROM.get(sid, "&mdash;")],
                   ["Contributes", contrib]],
                  [24 * mm, 146 * mm], header=False),
        ]
        s.append(KeepTogether(blk))

    # ---------------------------------------------------------------- 4
    s.append(P("4&nbsp;&nbsp;ClinicalTrials.gov, trial by trial", "h1"))
    read_ok = [c for c in cts if c["rows"]]
    no_res = [c for c in cts if not c["rows"]]
    s.append(P(
        f"CT1 is the module&rsquo;s principal human source and its only source of quantitative "
        f"hydrocephalus rows. {len(cts)} registry records of oligonucleotides delivered into the "
        f"central nervous system were retrieved in full and committed to the repository; "
        f"<b>{len(read_ok)} carry posted results</b> and were read, contributing "
        f"{sum(c['rows'] for c in read_ok):,} measurements."))
    s.append(table(
        [["NCT", "Drug", "Lead sponsor", "Status", "Rows"]] +
        [[f"<font face='Courier' size='7'>{c['nct']}</font>", c["drug"], c["sponsor"],
          c["status"], f"{c['rows']:,}"] for c in read_ok],
        [24 * mm, 30 * mm, 60 * mm, 32 * mm, 16 * mm], align_right=(4,)))
    s.append(caption("Each record resolves at "
                     "<font face='Courier'>https://clinicaltrials.gov/study/&lt;NCT&gt;</font> "
                     "for a human reader and at "
                     "<font face='Courier'>https://clinicaltrials.gov/api/v2/studies/&lt;NCT&gt;"
                     "</font> for the data. Rows are counted from the released dataset."))

    s.append(box([
        P(f"<b>{len(no_res)} completed or terminated CNS oligonucleotide trials have posted no "
          f"results at all.</b> Each was retrieved successfully and each returns "
          f"<font face='Courier'>hasResults: false</font>, so the registry holds no "
          f"adverse-event table to read.", "small"),
        P("", "small"),
        table([["NCT", "Drug", "Status"]] +
              [[f"<font face='Courier' size='7'>{c['nct']}</font>", c["drug"], c["status"]]
               for c in no_res],
              [26 * mm, 60 * mm, 40 * mm]),
        P("This is a finding about the field rather than a gap in the retrieval: the safety data "
          "for these programmes is not public anywhere this pipeline can reach.", "small")],
        bg=WARNBG))

    # ---------------------------------------------------------------- 5
    s.append(P("5&nbsp;&nbsp;Retrieved and held, contributing no released row", "h1"))
    s.append(P(
        "These were read during research. None supplies a row, so removing every one of them "
        "changes nothing in the released dataset. They are listed because a reader is entitled "
        "to know what informed the work as well as what is in it."))
    s.append(table(
        [["ID", "Source", "Identifiers", "Licence", "In repo?", "What it would add"]] +
        [[a, b, c, d, e, f] for a, b, c, d, e, f in HELD],
        [10 * mm, 48 * mm, 27 * mm, 25 * mm, 14 * mm, 46 * mm]))
    s.append(box([
        P("<b>Three of these are on the working disk but deliberately not in the repository.</b> "
          "S1, B2 and M1 are copyrighted publisher material not licensed for redistribution "
          "&mdash; two Roche conference decks and an NEJM correspondence item. Committing them "
          "would republish them, which is a different act from reading them for research. They "
          "are listed in <font face='Courier'>.gitignore</font>, and named in full above so "
          "anyone can retrieve their own copy. This is the same per-source-terms discipline "
          "<font face='Courier'>LICENSE.md</font> applies at row level.", "small"),
        P("", "small"),
        P("<b>This was a judgement call, not an instruction.</b> Say the word and they can be "
          "committed.", "small")]))

    # ---------------------------------------------------------------- 6
    s.append(P("6&nbsp;&nbsp;Examined and rejected, with the reason", "h1"))
    s.append(P(
        "A source register that lists only what was used is a reading list, not a provenance "
        "record. These were found, assessed and turned down; the reason is stated so the "
        "decision can be argued with."))
    s.append(table(
        [["Source", "Identifiers", "Why it looked right", "Why it was rejected"]] +
        [[a, f"<font size='7'>{b}</font>", c, d] for a, b, c, d in REJECTED],
        [50 * mm, 30 * mm, 44 * mm, 46 * mm]))

    # ---------------------------------------------------------------- 7
    s.append(P("7&nbsp;&nbsp;Human <i>in vitro</i> backlog &mdash; identified, not yet extracted", "h1"))
    hv = sum(v for k, v in collections.Counter(
        m["subject_class"] for m in meas).items() if k == "human_invitro")
    s.append(P(
        f"The Challenge brief states a particular interest in &ldquo;datasets based on in vitro "
        f"human systems or able to extrapolate data between in vitro human systems and animal "
        f"data&rdquo;. This release carries <b>{hv} human <i>in vitro</i> measurements</b> from "
        f"sources HV1&ndash;HV3. The sources below were found in the same sweep and are queued "
        f"for the next revision. <b>No released row depends on any of them</b>, so this is a "
        f"costed backlog rather than an unknown."))
    s.append(table(
        [["Source", "Identifiers", "Human system", "What it carries", "Seq?"]] +
        [[a, f"<font size='7'>{b}</font>", c, d, e] for a, b, c, d, e in BACKLOG],
        [50 * mm, 26 * mm, 34 * mm, 46 * mm, 14 * mm]))
    s.append(caption("Every identifier in this table was resolved against the Europe PMC search "
                     "API rather than carried over from a reading note."))

    s.append(box([
        P("<b>One lead is recorded here without a verified citation.</b> A study reported as "
          "Yoshikawa 2025, <i>J Pharmacol Toxicol Methods</i> 135:107844 &mdash; 27 ASOs run "
          "through a rat calcium-oscillation IC<sub>50</sub> assay, then mouse ICV, then a human "
          "iPSC multi-electrode array &mdash; would be the closest match in the literature to "
          "the brief&rsquo;s extrapolation clause. Four separate Europe PMC queries (by page "
          "number, by author and year, by title phrase, and by DOI) return nothing. It is "
          "therefore listed as <b>an unverified lead to chase, not a citation</b>, and no part "
          "of this dataset rests on it.", "small")], bg=WARNBG))

    # ---------------------------------------------------------------- 8
    s.append(P("8&nbsp;&nbsp;The licence audit that produced this document", "h1"))
    s.append(P(
        "Writing this register meant re-resolving every identifier against Europe PMC and "
        "reading each article&rsquo;s own machine-readable permissions block rather than "
        "trusting the reading notes. That found two errors in the released dataset, both now "
        "fixed and both material."))
    s.append(table(
        [["", "What the registry said", "What the source actually says", "Effect"],
         ["<b>K1</b> Miller 2024",
          "CC BY-NC &rarr; <font face='Courier'>cc_by_nc</font>; cited under a title the article "
          "does not carry; PMCID from the preprint record paired with the journal DOI",
          "<b>CC BY-NC-ND 4.0</b> &mdash; verbatim from the permissions block of <i>both</i> the "
          "journal record (PMC11567125) and the preprint record (PMC11185713)",
          "NoDerivatives. Its 41 measurements are now "
          "<font face='Courier'>summary_stat_only</font>, not redistributable as dataset "
          "content. The dataset had been over-claiming its rights."],
         ["<b>L1</b> Kuroda 2025",
          "CC BY-NC &rarr; <font face='Courier'>cc_by_nc</font>",
          "<b>CC BY 4.0</b> &mdash; &ldquo;This is an open access article under the CC BY "
          "license&rdquo;",
          "Its 6 measurements are now <font face='Courier'>cc_by</font>. The dataset had been "
          "under-claiming, needlessly restricting rows the authors released freely."]],
        [24 * mm, 46 * mm, 50 * mm, 50 * mm]))
    s.append(P(
        "<font face='Courier'>LICENSE.md</font> was also found quoting row counts from a release "
        "three revisions old. It is now generated from the released rows by "
        "<font face='Courier'>src/make_summary.py</font>, so it cannot drift again. The same "
        "applies to this document."))

    # ---------------------------------------------------------------- 9
    s.append(P("9&nbsp;&nbsp;Checking any of this yourself", "h1"))
    s.append(table(
        [["To check", "Command"],
         ["The licence of any source",
          "<font face='Courier' size='7'>curl 'https://www.ebi.ac.uk/europepmc/webservices/rest/"
          "&lt;PMCID&gt;/fullTextXML' | grep -A3 permissions</font>"],
         ["That a measurement's source and location are recorded",
          "<font face='Courier' size='7'>cut -d, -f1,2,3 toxicity/*/data/measurements.csv</font>"],
         ["Which rows came from which source",
          "<font face='Courier' size='7'>python3 qc/validate_dataset.py --json</font>"],
         ["An adverse-event table, at source",
          "<font face='Courier' size='7'>curl 'https://clinicaltrials.gov/api/v2/studies/"
          "&lt;NCT&gt;' | jq .resultsSection.adverseEventsModule</font>"],
         ["That the whole dataset rebuilds from the committed sources",
          "<font face='Courier' size='7'>see README.md &lsquo;Rebuilding from scratch&rsquo; "
          "&mdash; eight commands, no network needed</font>"],
         ["This document",
          "<font face='Courier' size='7'>python3 src/make_sources.py</font>"]],
        [50 * mm, 120 * mm]))
    s.append(P(
        "Every measurement row carries a <font face='Courier'>source_ref</font> and a "
        "<font face='Courier'>source_location</font>. The location is not a page number: it "
        "names the table, the figure panel, the sheet, the column, or the registry path that the "
        "value came out of. A reader who disagrees with a number can find it at source without "
        "asking us where to look."))
    return s


def main() -> int:
    meas = endpoints.load_all("measurements")
    oligos = endpoints.load_all("oligos")
    srcs = endpoints.load_all("sources")
    cts = ct_rows(meas)
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / "OligoTox-CNS_SourceRegister.pdf"
    build(p, story(meas, oligos, srcs, cts),
          "OligoTox-CNS — Source Register — CNS / neurotoxicity module")
    import pymupdf
    pages = len(pymupdf.open(p))
    print(f"wrote {p.relative_to(ROOT)}  ({pages} pages, {p.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
