#!/usr/bin/env python3
"""Render the Public Access and Dissemination Plan.

    deliverables/OligoTox-CNS_PADP.pdf     (limit: 5 pages)

The PADP is the third of the four required Phase 2 submission documents, and its content is
prescribed rather than free-form. The brief requires it to describe:

  (1) how winners will disseminate information about the solution, and make the solution AND the
      knowledge necessary to access and utilise the datasets available under NON-EXCLUSIVE
      LICENCES FOR RESEARCH PURPOSES;
  (2) how the winner would allow OTHERS to utilise the solution if the winner is unable to
      maximise public access themselves -- with specific licensing schemes and the scenarios in
      which each is employed;
  (3) how the winner will permit the U.S. GOVERNMENT to allow interested parties to utilise the
      solution if the winner neither utilises it nor licenses it to others on reasonable terms --
      again with licensing schemes and scenarios.

NIH intends to post the PADP publicly, and award recipients must agree to abide by it. Sections 3,
4 and 5 below map one-to-one onto those three requirements.

Numbers are interpolated from the live dataset, like every other document here.
"""
from __future__ import annotations

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from reportlab.lib import colors
from reportlab.lib.units import mm

from make_pdfs import BOXBG, WARNBG, B, P, box, build, caption, gather, table

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "deliverables"


def padp(n):
    sc = n["subject_class_distribution"]
    s = []
    s.append(P("OligoTox-CNS &mdash; Public Access and Dissemination Plan", "title"))
    s.append(P("NIH/NCATS Oligonucleotide Toxicity Open Data Challenge &mdash; Phase 2 "
               "&nbsp;&middot;&nbsp; CNS / neurotoxicity module &nbsp;&middot;&nbsp; release v1.0",
               "subtitle"))

    s.append(box([
        P("<b>This plan is binding.</b> The Challenge states that award recipients must agree to "
          "abide by the terms of the PADP they submit, and that NIH intends to post it publicly. "
          "Everything below is written to be honoured as stated, not as an aspiration. Sections "
          "3, 4 and 5 correspond one-to-one to the three requirements the Challenge sets for this "
          "document.", "small")]))
    s.append(P("", "body"))

    # ---------------- 1
    s.append(P("1&nbsp;&nbsp;What is covered by this plan", "h1"))
    s.append(P(
        f"&ldquo;The solution&rdquo; means the whole CNS module, not only its tables: the dataset "
        f"({n['n_oligos']:,} oligonucleotides, {n['n_measurements']:,} CNS toxicity measurements, "
        f"{n['n_modification_rows']:,} per-position chemical-modification records), the build "
        f"pipeline that produces it, the schema and data dictionary, the quality-control suite, "
        f"the figures, and the narrative and methodology documents. A dataset without the code "
        f"and vocabulary needed to use it is not usable, so the plan covers all of it together."))
    s.append(table([
        ["Component", "Form", "Covered"],
        ["Dataset", "CSV per endpoint, plus an XLSX workbook", "yes"],
        ["Data dictionary and schema", "Markdown, generated from the code", "yes"],
        ["Build pipeline and QC suite", "Python, no proprietary dependencies", "yes"],
        ["Source material", "the retrieved files the pipeline reads, where redistributable", "yes &mdash; see &sect;6"],
        ["Narrative and methodology documents", "PDF", "yes"],
        ["Measurement instruments and grading rubric", "Markdown", "yes"]],
        [52 * mm, 78 * mm, 40 * mm]))

    # ---------------- 2
    s.append(P("2&nbsp;&nbsp;Where it will live, and how people will find it", "h1"))
    s.append(table([
        ["Channel", "Purpose", "Terms", "When"],
        ["Public git repository", "canonical source; full history, so any figure or number traces "
                                  "to the commit that produced it", "CC BY 4.0", "live now"],
        ["Zenodo deposit", "archival copy with a citable DOI; a concept DOI always resolving to "
                           "the latest version", "CC BY 4.0", "at submission"],
        ["Challenge submission portal", "the four required documents", "as required by NIH", "at submission"]],
        [38 * mm, 66 * mm, 34 * mm, 32 * mm]))
    s.append(P(
        "Zenodo is chosen over a domain-specific repository because no established public "
        "repository for oligonucleotide toxicity data exists &mdash; which is part of the gap this "
        "dataset addresses. There is <b>no registration, no data-use agreement, no access "
        "committee and no embargo</b>. Files are plain CSV, XLSX and Markdown, openable without "
        "proprietary software. No component requires a licence key, a hosted service, or a "
        "credential of any kind."))
    s.append(P(
        "<b>Dissemination of the knowledge to use it, not only the files.</b> The Challenge asks "
        "for the knowledge necessary to access and utilise the dataset, so the repository ships "
        "the schema and data dictionary, the measurement instruments verbatim from their sources, "
        "the grading rubric with the rule recorded on every graded row, a worked baseline model "
        "that trains from the released files alone, and a build pipeline that regenerates every "
        "artefact from the committed sources. Announcement will be through a preprint describing "
        "the dataset, the Zenodo DOI, and direct notice to the oligonucleotide-safety groups whose "
        "published work the dataset curates."))

    # ---------------- 3
    s.append(P("3&nbsp;&nbsp;Non-exclusive licensing for research purposes", "h1"))
    s.append(P(
        "<b>Every licence granted under this plan is non-exclusive, irrevocable, worldwide and "
        "royalty-free.</b> No exclusive licence to any part of the solution has been granted, and "
        "none will be. No party &mdash; including any future commercial partner &mdash; will "
        "receive rights that would prevent any researcher from using the dataset."))
    s.append(table([
        ["Component", "Licence", "What a researcher may do"],
        ["Everything created by this project &mdash; schema, code, documentation, figures, all "
         "derived and computed fields", "<b>CC BY 4.0</b>", "any use, including commercial, with attribution"],
        ["Rows curated from a CC BY source", "CC BY 4.0", "any use, with attribution to this dataset and the primary source"],
        ["Rows curated from a CC BY-NC source", "CC BY-NC 4.0", "non-commercial research use, with attribution"],
        ["Rows from US Government works (FDA labels)", "public domain", "any use"],
        ["Build pipeline and QC suite", "CC BY 4.0", "any use, including commercial"]],
        [50 * mm, 34 * mm, 86 * mm]))
    s.append(P(
        f"A curated dataset cannot grant rights its sources did not grant, so terms are recorded "
        f"<b>per row</b> in a <font face='Courier'>redistribution</font> column rather than "
        f"asserted uniformly. {n['open_rows']:,} of {n['n_measurements']:,} measurements "
        f"({n['pct_open']}%) are CC BY 4.0 or US public domain and are reusable for any purpose "
        f"including commercially; the remainder derive from CC BY-NC sources, are individually "
        f"marked, and are removable with a one-line filter. <b>This is stated rather than "
        f"smoothed over: labelling the whole release CC BY would over-claim, and labelling it all "
        f"non-commercial would needlessly restrict {n['pct_open']}% of it.</b>"))
    s.append(P(
        "For research purposes specifically, no separate permission is needed for any part: the "
        "CC BY-NC portion already permits non-commercial research, and the remainder permits "
        "everything. A researcher can therefore use the entire dataset for research without "
        "contacting us."))

    # ---------------- 4
    s.append(P("4&nbsp;&nbsp;If we cannot maximise public access ourselves", "h1"))
    s.append(P(
        "The Challenge requires a plan for the case where the winner is unable to maximise public "
        "access. Our answer is structural rather than promissory: <b>the licences above are "
        "already irrevocable, and the artefacts are already deposited in an archive we do not "
        "control.</b> A CC BY 4.0 grant cannot be withdrawn, so nothing we later do &mdash; or "
        "fail to do &mdash; can remove the public's rights to what has been released. The "
        "scenarios below therefore concern <i>continuity of stewardship</i>, not restoration of "
        "access."))
    s.append(table([
        ["Scenario", "What happens", "Licensing scheme employed"],
        ["<b>A.</b> The team stops maintaining the dataset", "The Zenodo deposit and its DOI "
         "persist independently of us. Anyone may fork, correct and redistribute the repository, "
         "including under their own name, provided attribution is kept.",
         "CC BY 4.0 &mdash; already granted, irrevocable; no further act needed from us"],
        ["<b>B.</b> A team member becomes unavailable", "No single person holds a credential the "
         "release depends on. The repository has more than one maintainer, and the Zenodo record "
         "is deposited under an institutional-neutral account with a named co-depositor.",
         "unchanged; stewardship transfers, licence does not"],
        ["<b>C.</b> Hosting fails or a provider withdraws", "Every source file the pipeline reads "
         "is committed alongside the code, so the dataset rebuilds from any surviving copy. "
         "Mirrors may be created by anyone without asking.",
         "CC BY 4.0 permits redistribution and mirroring by any party"],
        ["<b>D.</b> We are unable or unwilling to act on a correction", "Any party may publish a "
         "corrected derivative. We will additionally grant, on written request and at no cost, a "
         "non-exclusive licence naming that party as a maintainer of record.",
         "CC BY 4.0 for the derivative; a separate written non-exclusive stewardship licence"],
        ["<b>E.</b> A third party wants terms beyond CC BY-NC on the NC-derived rows", "We cannot "
         "grant what we do not hold. We will identify the upstream rightsholder and the exact "
         "rows affected so the requester can seek permission directly; the other "
         f"{n['pct_open']}% needs no permission.",
         "referral, plus our own CC BY 4.0 grant on the structure, code and derived fields"]],
        [34 * mm, 74 * mm, 62 * mm]))

    # ---------------- 5
    s.append(P("5&nbsp;&nbsp;Permitting the U.S. Government to enable others", "h1"))
    s.append(P(
        "The Challenge requires a plan describing how the winner will permit the U.S. Government "
        "to allow interested parties to utilise the solution, should the winner fail to utilise it "
        "and fail to permit others to do so on reasonable terms."))
    s.append(box([
        P("<b>Standing grant.</b> We hereby grant the United States Government a non-exclusive, "
          "irrevocable, worldwide, royalty-free, fully paid-up licence to use, reproduce, "
          "distribute, prepare derivative works of, publicly display and publicly perform the "
          "solution, and <b>to authorise others to do so on its behalf</b>, for any purpose. "
          "This grant is made now and is not conditional on any failure by us &mdash; it does not "
          "need to be triggered, and there is nothing for the Government to determine before "
          "exercising it.", "small")], WARNBG, colors.HexColor("#ec835a")))
    s.append(P("Why the grant is unconditional", "h2"))
    s.append(P(
        "A conditional grant would require someone to adjudicate whether the winner had in fact "
        "failed to act, and on what timescale &mdash; which is precisely the delay the requirement "
        "exists to prevent. Granting it up front removes the determination step. In practice the "
        "grant is also redundant for the CC BY 4.0 portion, which already permits the Government "
        "and everyone else to do all of the above; it matters for the CC BY-NC-derived rows, "
        "where it removes the non-commercial restriction as far as we are able to remove it."))
    s.append(table([
        ["Scenario", "Government action available", "Licensing scheme"],
        ["We fail to maintain or disseminate the solution", "Host, mirror, update or republish it "
         "directly, or authorise any third party to", "the standing grant above; no notice to us required"],
        ["We refuse a reasonable request from a third party", "Authorise that party directly under "
         "the standing grant", "standing grant; we waive any right to object"],
        ["Government wishes to fund a derivative or extension", "Commission it from any party, "
         "including a competitor", "standing grant, plus CC BY 4.0 on the underlying work"],
        ["Upstream CC BY-NC terms limit a Government use", "We will identify the rightsholder and "
         "the affected rows and support the request", "referral; our own rights already granted in full"]],
        [46 * mm, 66 * mm, 58 * mm]))
    s.append(P(
        "The one limit we state honestly: we cannot grant rights in third-party copyrighted "
        "material we merely curated. That limit is bounded and documented row by row, and it "
        f"touches {n['n_measurements'] - n['open_rows']} of {n['n_measurements']:,} measurements."))

    # ---------------- 6
    s.append(P("6&nbsp;&nbsp;Limits, stated plainly", "h1"))
    s.append(B(
        "<b>Three source documents are deliberately not redistributed.</b> Two conference "
        "presentations and one journal correspondence item are copyrighted and not licensed for "
        "redistribution. They are named in the source register with everything needed to obtain "
        "them independently, and <b>no released row depends on any of them</b>. Curating a source "
        "is not the same act as republishing it, and we have not conflated the two."))
    s.append(B(
        f"<b>The dataset contains no human <i>in vitro</i> data.</b> Of {n['n_measurements']:,} "
        f"measurements, {sc['human_clinical']} are human clinical and "
        f"<b>{sc['human_invitro']} are human <i>in vitro</i></b>; the rest are animal. This plan "
        f"is framed by the Challenge around &ldquo;winning datasets from in vitro human-based "
        f"systems&rdquo;, so the limit is material and we state it here rather than only in the "
        f"narrative. The dataset's contribution is the sequence-to-toxicity pairing and the "
        f"in-vitro-to-in-vivo structure; the human arm of that structure is not yet present."))
    s.append(B(
        "<b>Severity grades are provisional</b> pending subject-matter-expert review. Every grade "
        "carries the rule that produced it, so a reviewer can audit rather than re-derive."))
    s.append(B(
        "<b>No personal data is involved.</b> Every measurement is either a preclinical result or "
        "an aggregate incidence already published in a regulatory document. There are no human "
        "subjects, no identifiable information, and therefore no consent or privacy constraint on "
        "any part of the release."))

    s.append(P("7&nbsp;&nbsp;Maintenance and preservation", "h1"))
    s.append(P(
        "Corrections are made by pull request against the public repository, with the "
        f"{n['checks_total']}-check quality suite as the merge gate. Each release is re-deposited "
        f"to Zenodo with a new version DOI while the concept DOI continues to resolve to the "
        f"latest. The repository is self-contained &mdash; the source files the pipeline reads are "
        f"committed alongside the code &mdash; so the dataset remains rebuildable even if a "
        f"publisher URL rots. Preservation does not depend on us: the Zenodo deposit is "
        f"independently archived, and the CC BY 4.0 grant permits anyone to mirror it."))
    return s


def main() -> int:
    OUT.mkdir(exist_ok=True)
    n = gather()
    p = build(OUT / "OligoTox-CNS_PADP.pdf", padp(n),
              "OligoTox-CNS v1.0 · Public Access and Dissemination Plan · "
              "NCATS Oligonucleotide Toxicity Challenge, Phase 2")
    import pymupdf
    pages = len(pymupdf.open(p))
    print(f"{p.name}: {pages} pages (limit 5) [{'OK' if pages <= 5 else 'OVER LIMIT'}]")
    return 0 if pages <= 5 else 1


if __name__ == "__main__":
    sys.exit(main())
