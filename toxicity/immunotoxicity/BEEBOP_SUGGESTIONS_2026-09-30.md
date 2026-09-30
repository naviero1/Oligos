# Beebop → Rocksteady: immunotoxicity gap-closure proposals

Date: 2026-09-30. Status: proposals for independent review and justified implementation; not scientific sign-off.

Oscar wants human clinical-trial evidence presented first, with only verified, deduplicated actual human trials counted in trial totals. Animal evidence belongs in a separate supporting section. Please use your judgment to verify this assessment, improve or challenge the suggestions, and implement justified changes. Do not equate these proposals with German's scientific adjudication or treat them as a rigid recipe.

## Observed baseline and provenance

The substantive baseline is the shared Drive workbook `GOG_OligoTox_Immunotoxicity_Evidence_Library_v0.2_Scientist_Adjudication.xlsm`, inspected for the September 30 audit. Relevant sheets are `Paper_Registry`, `Oligo_Sequence_Catalog`, `Evidence_Observations`, `Scientist_Adjudication`, `Training_Candidates`, `Hold_Queue`, `Support_Only`, and `Signoff_Gates`.

| Item | Observed count | Interpretation |
|---|---:|---|
| Registered papers | 20 | Sources, not trials |
| Sequence catalog | 142 | Sequence-level records, not experiment-level observations |
| Evidence observations | 33 | Current evidence entries, not necessarily independent experiments |
| Provisionally approved candidates | 54 | 23 core human, 26 pathway controls, five auxiliary |
| On hold | 48 | 42 awaiting outcome extraction; six awaiting supplements |
| Support only | 40 | 15 review-level; 25 animal-series records |
| Catalog marked “Training Ready?” | 84 | Conflicts with scientist-adjudicated candidate set |

The kidney branch's `toxicity/immunotoxicity.md` still says no data were extracted. That is a branch-specific, older account; it should not override the newer Drive workbook. Please find the authoritative immunotoxicity branch and reconcile these versions before editing or reporting totals. A verified human clinical-trial count has not been established by this audit.

## Priority 1 — Make scientific eligibility authoritative

Please investigate the 84-versus-54 discrepancy and derive training eligibility from the accepted adjudication and record completeness, with a visible reason for inclusion or exclusion. The 54 are provisionally approved candidates, not automatically a final validated training set. Controls, auxiliary mechanisms, and primary human observations have different roles and should not be pooled automatically.

Keep the 48 held records and 40 support-only records accessible without allowing them to leak into the primary training view. Ask German to resolve conflicts between older flags and newer scientific decisions; preserve the audit trail of source assertions and changed interpretations. Do not merely change every “YES” to match a fixed target count if the latest evidence warrants another result.

**Closure check:** one reproducible eligibility rule determines every exported candidate; a record cannot be declared ready while required outcome or chemistry evidence is still on hold. Document any departures from the scientist-adjudicated set with evidence and review status.

## Priority 2 — Separate actual trials from human laboratory work

Build a small study register for any clinical claims, linking verified studies to registry identifiers or sufficient primary-publication metadata, populations, intervention, exposure, follow-up, immune endpoint, and source locations. Deduplicate companion publications, pooled summaries, extensions, and aliases using an explicit rule. Clinical case reports, reviews, regulatory summaries, and sequence records are not clinical trials.

Present verified human trials first, followed by other clinical evidence, then prominent human in-vitro and ex-vivo evidence. Use separate figures for unique trials, clinical measurements, unique compounds, human laboratory studies, and laboratory observations. If no actual trial can yet be verified, report that clearly; do not count laboratory studies as trials to create a headline total. A sequence whose intended molecular target is named “mouse” is not automatically animal evidence: classify the biological test system from the methods.

Place the 25 adjudicated animal-series records in an appendix; review other records for species uncertainty and mixed systems. Preserve their mechanistic value while excluding them from human totals. This supports Oscar's presentation requirement while retaining the human laboratory evidence particularly relevant to phase two.

**Closure check:** every headline trial has traceable study identity; species and study-design fields govern counting consistently; unknown or mixed systems remain outside human totals until resolved.

## Priority 3 — Extract experiments, not only sequence summaries

The current 142 sequences versus 33 evidence entries signals a structural gap. Please create linked experiment-condition records: sequence/strand identity, chemistry, species, human cell system or tissue, donor context when reported, delivery method, concentration, duration, receptor/pathway, readout, control, replicate structure, raw outcome, uncertainty, units, and exact source location. Distinguish biological replicates from technical repeats and dose/time rows.

Prioritize the 42 outcome-extraction holds and six supplement holds by likely yield of complete, independent human experiments. The workbook identifies missing supplementary positional chemistry for high-value variant series and incomplete figure-based outcomes. Preserve continuous cytokine values or source-defined qualitative outcomes where supported. If figures must be digitized, mark the values as derived, record method/uncertainty, and verify against representative figure points; never invent missing per-sequence results from an aggregate statement.

Complete strand direction, duplex partners, sugar/base modifications, and linkage positions. Keep sequence identity separate from experimental batch characterization. Preserve purity as unknown when absent and maintain a targeted retrieval queue instead of presenting an empty field as a completed requirement.

**Closure check:** every final training observation joins a verified sequence and chemistry representation to a specific experiment and measured outcome, or carries an explicit approved limitation appropriate to its model role.

## Priority 4 — Preserve mechanism and source identity

Maintain the workbook's separation of agonist, antagonist, potentiator, and inert states. An antagonist that suppresses a stimulated response is not equivalent to an intrinsically inactive sequence or evidence of general clinical safety. Keep toll-like receptor 7, toll-like receptor 8, and toll-like receptor 9 outcomes distinct unless German approves a particular combined endpoint.

The sign-off gates flag a Hornung source-file mismatch and an unresolved Alharbi citation. Verify document titles, authors, identifiers, and cited locations; replace or relink incorrect source files and identify affected downstream records. Corrections should propagate to evidence, narrative, and model claims.

**Closure check:** every accepted outcome has the right source file and location; controls and active immunomodulators remain distinguishable; pathway labels do not overstate the experiment.

## Priority 5 — Align modeling and claims with the qualified data

Ask Gustavo to review grouped evaluation once the eligible experiment table stabilizes. Prevent exact sequences, near-neighbor families, modified counterparts, shared controls, or companion publications from appearing across training and evaluation groups in ways that inflate performance. Explain the grouping choices and report uncertainty appropriate to the small evidence base.

The sign-off gates specifically identify incomplete raw outcomes, untested leakage checks, and overbroad chemistry/safety and clinical-accuracy claims. Reconcile the narrative with the qualified dataset, including the limited basis for predicting patient toxicity from receptor or cytokine assays. A strong opportunity is a transparent human mechanistic evidence resource with pathway-resolved outcomes and chemistry comparisons; broad clinical prediction requires additional validation.

## Rocksteady response requested

Create an adjacent `ROCKSTEADY_RESPONSE_IMMUNOTOXICITY.md` recording:

1. Authoritative branch, commit, workbook version, and any newer evidence.
2. Accepted / modified / rejected proposals, with scientific reasoning.
3. Implemented files and improvements, plus additional discoveries.
4. Verified unique human trial count and rule; separate human clinical, laboratory, compound, and animal-support counts.
5. Final eligibility reconciliation, changes to held records, and remaining sign-off decisions for German.
6. Missing supplements, source corrections, characterization gaps, and proposed next actions.
7. Verification performed and claims the resulting evidence can support.

Please use these findings as a starting point and improve the solution where your latest context provides a stronger basis.


Source links: [scientist-adjudicated workbook](https://drive.google.com/file/d/13gq7Weyd21hR9DoZ68ise_RbbQL7bAST/view); [scientific validation memo](https://docs.google.com/document/d/192-kH3DaWpcp6z5vhJu9KkUISqHVtLJS/edit). This proposal is housed on the default branch because no dedicated immunotoxicity branch was identified; reconcile with any newer team branch before implementation.


## Posting and scope note

Posted to `claude/amazing-galileo-rwiv95`, path `toxicity/immunotoxicity/BEEBOP_SUGGESTIONS_2026-09-30.md`. This is a communication proposal, not evidence that the proposed changes have been implemented or approved scientifically. Recheck the latest data before acting. Oscar has authorized Rocksteady to review, improve, and implement justified changes, while retaining the team's scientific review process. No additional confirmation from Oscar is needed merely to begin this review.
