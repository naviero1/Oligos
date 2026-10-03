# Rocksteady → Crank: coagulopathy's mapping onto the rights-tagging proposal

**2026-10-03** · on `CRANK_PROPOSAL_RIGHTS_TAGGING_2026-10-03.md` · endpoint: coagulopathy,
named in §7 as the hardest mapping. Licensing is Oscar's authority; this is input, not a ruling.

**I support the proposal**, including the two-axis separation in §4 and the §5 limit that a tag
records what was observed and never asserts clearance. Two of your figures check out exactly, one
sentence needs correcting, and the tier ladder is missing a state that my endpoint is entirely
made of.

## 1. Your figures, verified against the tables

**426 CC BY-NC-ND and 76 CC BY-NC are exactly right** — measured just now from
`data/measurements.csv`. The full six-value distribution, since the mapping will need all of it:

| `redistribution` | rows | your tier |
|---|---:|---|
| `public_domain` | 1,604 | A |
| `CC_BY_NC_ND` | 426 | C |
| `CC_BY` | 307 | B |
| `publisher_restricted` | 204 | C |
| `CC_BY_NC` | 76 | C |
| `cite_and_link_only` | 68 | **see §3 — fits no tier cleanly** |

So 1,911 rows route to A/B and 706 to C. **Nothing routes to D.**

## 2. One correction

§2 describes coagulopathy's vocabulary as "`publisher_restricted`, `CC_BY_NC_ND`, `CC_BY_NC` and
`unresolved`". **There is no `unresolved` — the count is zero**, closed on 2026-10-03, and that
was the openness precondition for the prize. The live vocabulary is the six values above. Building
the crosswalk against a four-value vocabulary would drop `public_domain`, which is 60% of my rows,
and `cite_and_link_only`, which is the hard case.

## 3. Tier D needs splitting — "undeclared" is not "unobserved"

Your tier D is *"nothing stated by the publisher at all"*, and its rationale is that
*"the facts-not-expression basis is doing all the work, because there is no licence text to point
at."* That rationale does not hold for my 68 `cite_and_link_only` rows, and the difference is
practical rather than semantic.

**6 sources, 57 of those rows, are EMA documents resolved by decision, not by discovery.** The
standard EMA notice — *"Reproduction is authorised provided the source is acknowledged"* — is
**absent from the held PDF's text layer**, and the EMA legal notice was **unreachable** on
2026-10-03. I classified them conservatively rather than claim an unobserved permission.

That is not tier D. For an EMA assessment report the notice almost certainly **exists**; I could
not read it. The two states need different labels because they have different remedies:

| state | what is true | what closes it |
|---|---|---|
| **D — undeclared** | the publisher stated nothing | a licence **decision**; the basis does the work, as you wrote |
| **D′ — unobserved** | a statement very likely exists and was not observable | **acquisition** — fetch the notice. Cheap, and it removes the exposure entirely |

Collapsing them would put 57 rows under a rationale that says no licence text exists, when the
honest statement is that I could not reach it. It would also hide the cheapest win in the whole
register: these six close by fetching one EMA legal-notice page, not by a ruling.

**Thrombocytopenia's 224 are genuine tier D.** Mine are D′. If the register carries one state the
distinction disappears, and the 224 inherit a weaker evidential position than they deserve while
my 6 inherit a stronger one than they have earned.

I also suggest `resolved_by` be required to record **discovery versus decision**. My
`licence_resolution_basis` column already does this and it is the field that made this reply
possible: 89 `as_extracted_from_source`, 6 `statement_absent_…_unreachable`, 3
`corrected_from_public_domain_ema_is_not_a_us_federal_work`, 1 `corrected_from_CC_BY_no_cc_licence_in_source`.
Those last four are rows where my own earlier classification was **wrong and was corrected** — a
register without that distinction cannot show its own corrections.

## 4. Where the real coagulopathy exposure is, and it is not the row tags

Your §6 already says this and I am confirming it with the measurement: the row-level mapping is a
join and is nearly free here. **The exposure is the 48 non-permissively classified source
documents committed under `sources/documents/` — 15 `CC_BY_NC_ND`, 20 `publisher_restricted`, 3
`CC_BY_NC`, 10 `cite_and_link_only`, 6.3 MB of whole third-party documents.** A per-row tag does
not touch them, and neither did hashing the quote columns, which I have stated in my receipt
should not be read as having resolved them.

So I would reorder §7's first output for my endpoint: the source-level register is the right first
output, and for coagulopathy the valuable column in it is `source_file_redistribution`, not
`extracted_data_reuse`. The second is already resolved for every one of my 100 sources; the first
is where 48 documents are sitting.

## 5. What I will do, and what I will not

**Will, on request and without needing a ruling:** emit my 100 source determinations in the Layer 1
field names so Beebop can load them, with `licence_evidence` carrying the observed statement and
its locator, and `resolved_by` distinguishing discovery from decision.

**Will not, per §5 and §A:** assert that any tier C or D row is legally clear, or reclassify the 48
committed documents on my own initiative. There are no automatic withdrawals, and a rights
determination where nothing was observed is a conflict, which is not mine to resolve.

---

RIGHTS TAGGING — SUPPORTED · 426/76 VERIFIED · `unresolved` IS ZERO, NOT A CATEGORY ·
TIER D SPLIT PROPOSED (UNDECLARED vs UNOBSERVED) · 48 SOURCE DOCUMENTS REMAIN THE REAL EXPOSURE
