# Codex review of the finished book, round 4 — marketing-book

reviewed_commit: 8696791

Read-only review, same request as `audit/codex-prompt.md`. Saved verbatim from the verdict line on. Kept as a
record: its findings were fixed in the next commit.

verdict: fail
open_blocker_major: 2
reviewer_model: GPT-5 Codex

| ID | severity | location | finding | why it matters | suggested fix |
|---|---|---|---|---|---|
| C-001 | major | Chapter 5, §5.3 and Q7: “Laboratory analysers, reagents … all belong here” | The book classifies laboratory analysers and reagents categorically as in-vitro diagnostic medical devices. IVD status depends on the manufacturer’s intended medical use for examining human specimens; research-use-only reagents and general-purpose laboratory equipment are not automatically IVDs. The keyed MCQ repeats the overstatement. | This misstates a regulatory definition for laboratory students and could lead them to apply registration and quality requirements to the wrong product class. The [WHO definition](https://extranet.who.int/prequal/content/glossary) expressly includes the intended-purpose condition. | Add the intended-purpose qualification, distinguish IVDs from research/general laboratory products, and rewrite Q7 accordingly. |
| C-002 | major | Chapter 9, §9.2, Table 9.1 and Q2 | The “main/supporting elements” taxonomy is not the cited Kotler and Keller communications mix. It omits direct/database marketing, online/social media, mobile marketing, and events/experiences as major modes, while treating branding and “service policy” as supporting communication elements. Q2 then keys a conference as merely supporting. | This is a claim–source mismatch and teaches an obsolete or unidentified taxonomy in the chapter devoted to marketing communications. The cited framework lists eight major modes, including events and digital channels ([framework summary](https://ebrary.net/80667/management/marketing_communications)). | Replace Table 9.1 with the cited eight-mode framework, or identify and justify a different source. Update LO1, Q2, its key, and the glossary to match. |
| C-003 | minor | Chapter 2, §2.5, elasticity worked example | The printed elasticity of −0.4 uses percentage changes from the initial values but describes the result as elasticity “over this range.” For a discrete movement between two observations, midpoint arc elasticity is approximately −0.474; reversing the book’s calculation also produces a different value. | The arithmetic reproduces, but the unstated denominator convention makes the measure direction-dependent and may confuse students applying the formula to two-point data. The inelastic conclusion is unchanged. | Label the calculation explicitly as the initial-value method, or use the midpoint formula and report approximately −0.47. |
| C-004 | minor | Chapter 8, §8.3 versus Key Takeaways | Section 8.3 states that channels perform eight functions and includes risk taking, but the chapter summary lists only seven and omits risk taking. | The summary used for revision does not reproduce the chapter’s own classification, despite LO1 requiring students to list the functions. | Add risk taking to the Key Takeaways list. |
| C-005 | minor | Chapter 6, Q10 rationale | The rationale says pre-registration promotion is prohibited because the product’s “introduction stage … begins only after regulatory approval.” That is circular and gives the product-life-cycle label as the legal reason. The actual reason is the EDA rule prohibiting promotion of an unlicensed prescription product. | The key is the only plausible option, but its rationale fails to teach the governing rule and incorrectly presents a marketing model as a source of legal authority. | Cite the EDA prohibition directly in the rationale and treat post-registration introduction as a consequence, not the reason. |

## Notes

All worked calculations, numeric MCQs, and numeric essay answers were recomputed. Apart from C-003’s unstated elasticity convention, the printed arithmetic, units, dominance decisions, ICERs, benefit–cost ratios, and QALY calculations reproduce. No inducement-based or misleading promotional practice is endorsed; the Egyptian data-protection, medicine-promotion, and out-of-pocket-spending claims checked were supportable.
