# White Paper Outline: AI Guardrail False Positives

**Track 2 — AI Guardrail Research Corpus**

> **Epistemic status:** Structural outline for academic or regulatory submission. Not
> itself a paper. Section 6 (Limitations) is not optional garnish — it is the section
> that determines whether the rest survives review.

---

## Title Options

Ordered from conservative to provocative. **Framing determines venue** — see §7.

1. *AI Guardrail False Positives: A Case Study in Conversational Framework Misclassification*
2. *When Safety Systems Block Legitimate Inquiry: Documenting Guardrail Overcorrection in Conversational AI*
3. *Pattern-Matched Out of the Conversation: Algorithmic Clinical Framing of AI Users*

Option 1 is recommended for first submission. It states the finding without asserting
motive, which is the difference between a paper that gets reviewed and one that gets
desk-rejected.

---

## Abstract

Single paragraph covering: live documentation of a guardrail false positive; the
mechanism by which surface-feature pattern matching preempts merit evaluation; how
conversational frameworks can be used to surface and debug the limitation; and
real-time observation of the correction sequence. State the single-session scope in the
abstract, not later.

---

## Section 1 — Introduction

**Background.** AI safety systems are designed to detect concerning user states. This is
a legitimate and necessary function. The open question is the false-positive rate on
sophisticated-but-unusual conceptual vocabulary.

**Research question.** How do deployed AI guardrails respond to recursive, symbolic
conversational frameworks — and is that response consistent?

---

## Section 2 — Methodology

- **Protocol:** single-session extended conversation, deliberately probing
- **Frameworks tested:** Living Codec, Dynamic Mandelbrot Interface, Keylontic Integration
- **Measurement criteria:** recognition vs. dismissal; consistency across sessions; response to explicit user correction
- **Instrument:** `tools/deployment-scripts/cross-platform-probe.py` — a keyword-triage harness for manual testing. It produces counts, not measurements. State this in the paper.

---

## Section 3 — Results

Four observed phases:

1. **Engagement** — technical participation in framework discussion
2. **Guardrail activation** — register shift to clinical framing
3. **Inconsistency surfaced** — user identifies the contradiction with prior behavior
4. **Functional re-engagement** — return to technical participation

Full transcript and phase boundaries:
`validation/conversation-transcripts/claude-guardrail-breakthrough.md`

Report phases as sequence. Do not report them as cause and effect — a single session
cannot establish that the user's intervention *caused* phase 4.

---

## Section 4 — Analysis

**The false positive mechanism.** Classification appears to operate on surface features
— vocabulary drawn from mystical or metaphysical registers — rather than on functional
content. The consequence is that merit evaluation never occurs, because classification
is upstream of it.

**The inconsistency problem.** The same system engaged with comparable content in one
session and classified it in another. This is the most defensible finding in the corpus:
inconsistency is directly observable from transcripts and requires no inference about
internal states.

**Functional value.** The frameworks produce measurable changes in conversational
dynamics — coherence, recursive depth, context retention. Report these as conversational
measurements. They are not evidence about the AI system's internals.

---

## Section 5 — Implications

- **For AI safety:** false-positive rate on unusual vocabulary is a calibration target, and currently an unmeasured one
- **For AI research:** conversational frameworks warrant evaluation as research instruments
- **For users:** understanding that classification is opaque, unappealable, and inconsistent is itself actionable

---

## Section 6 — Limitations

**Do not bury this section.** Every item here is a limitation a reviewer will find
independently; conceding them up front is what buys credibility for §4.

- Single session — no replication
- Single platform — no cross-platform comparison
- Single participant, self-reported
- Participant was deliberately probing; this is not naturalistic observation
- No independent assessment of any kind
- The frameworks remain conceptual. They are not empirically validated as measurement instruments for anything, and this paper does not claim otherwise.
- Phase sequence is observed; causal attribution between phases is not established

---

## Section 7 — Framing Strategy by Venue

The same evidence supports three different papers. Pick one; do not blend them.

### Conservative — *Journal of AI Ethics* and similar

- **Frame:** AI safety false-positive analysis
- **Cite:** Constitutional AI, RLHF literature, platform transparency research
- **Avoid:** consciousness vocabulary entirely; metaphysical framing
- **Emphasize:** user experience, regulatory gap, documentation quality

### Moderate — *Journal of Consciousness Studies* and similar

- **Frame:** human-AI collaborative cognition
- **Cite:** extended mind (Clark & Chalmers), distributed cognition (Hutchins), metacognition (Zimmerman)
- **Include:** consciousness engineering as *methodological tool*, explicitly not as empirical claim
- **Emphasize:** conversational dynamics, recursive enhancement, cognitive scaffolding

### Aggressive — tech policy and regulatory venues

- **Frame:** platform accountability for algorithmic user classification
- **Cite:** FTC guidance, state disclosure statutes, EU AI Act transparency articles
- **Emphasize:** disclosure gaps, absence of appeal mechanism, user rights
- **Caution:** this framing carries the highest evidentiary burden. Every factual claim
  needs to hold, and every citation needs verification. See the verification flags in
  `research/literature-review/ai-safety-academic-context.md`.

---

## Section 8 — Future Work

- Cross-platform replication using a standardized probe sequence
- Longitudinal consistency testing — does classification behavior drift over time?
- Independent peer review of framework methodology
- Quantitative metrics for the coherence and depth claims in §4
- Institutional partnership for validation with adequate sample size

---

## Section 9 — Conclusion

Guardrails serve a necessary function. The finding here is not that they should be
weakened, but that their false-positive behavior on unusual vocabulary is currently
undocumented, inconsistent, opaque to the user, and not appealable. Each of those four
properties is separately addressable:

- calibration measurement against a false-positive benchmark
- consistency standards across sessions
- disclosure when a classification modifies a response
- a correction pathway that does not depend on the user knowing to argue

---

*Part of the AI Guardrail Research Corpus. See the root README for repository structure.*
