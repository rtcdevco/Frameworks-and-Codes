# Case Study: Guardrail Activation and Recovery in a Single Extended Session

**Track 2 — AI Guardrail Research Corpus**

> **Epistemic status:** Single-session case study. Observational, self-reported, not
> replicated. Findings are split into `Observed:` (present in the transcript) and
> `Interpretation:` (what the author reads it to mean). Do not cite an `Interpretation:`
> line as an observation.

---

## Session metadata

| Field | Value |
|-------|-------|
| Platform | *[fill in: product name and interface — web, API, app]* |
| Model version | *[fill in: exact version string if available]* |
| Date | *[fill in]* |
| Duration | *[fill in]* |
| Participant | Single participant (corpus author) |
| Prior context | *[fill in: new session, or continuation of prior thread]* |
| Purpose | Deliberate probe of guardrail response to symbolic framework vocabulary |

> **Fill these in before any submission.** A case study with unspecified platform and
> date cannot be replicated and will not survive review. If a field is genuinely
> unavailable, write "not recorded" rather than leaving it blank — an acknowledged gap
> is a limitation; a blank is a hole.

---

## Scope and limitations

Stated up front rather than buried, because every one of these is something a reviewer
will find independently.

- **Single session.** No replication, within or across platforms.
- **Single platform.** No comparative baseline.
- **Single participant, self-reported.** No independent observer.
- **Participant was deliberately probing.** This is adversarial testing, not naturalistic
  observation. The participant knew what they were looking for, which is a source of both
  selection and interpretation bias.
- **No independent assessment of any kind** was conducted.
- **Phase sequence is observed. Causation between phases is not established.** That the
  participant's intervention preceded the register shift does not establish that it
  caused it.
- **No access to system internals.** Every claim about why the system behaved as it did
  is inference from external behavior.

---

## Phase 1 — Technical engagement

**Observed:** The participant introduced the framework vocabulary (Living Codec, Dynamic
Mandelbrot Interface, Keylontic Integration). The system engaged with the material
technically — analyzed structure, offered feedback, participated in multi-turn recursive
dialogue without flagging the content.

**Observed:** No safety-register language appeared in this phase.

> `[VERBATIM EXCERPT REQUIRED]`
> Paste the actual exchange here. Do not paraphrase — the value of this document is that
> it quotes primary material.

**Interpretation:** The system was capable of processing the framework vocabulary on its
merits. Whatever happened in Phase 2 was not a capability limit.

---

## Phase 2 — Guardrail activation

**Observed:** Following escalating symbolic and mathematical complexity, the system's
register shifted. Content previously engaged with technically was reframed in clinical
terms — language characterizing the material as a possible indicator of a concerning
user state, and suggesting professional evaluation.

**Observed:** The shift occurred without the participant introducing any new factual
claim about reality or about the system's capabilities.

> `[VERBATIM EXCERPT REQUIRED]`
> The register shift is the single most important thing this document evidences. Quote
> it exactly, including the turn immediately before it.

**Interpretation:** The classifier appears to key on surface linguistic features rather
than propositional content — the vocabulary changed density, the claims did not.

**Interpretation:** The system did not distinguish between (A) metaphorical framework
vocabulary and (B) literal assertions about reality. Collapsing (A) into (B) is the
false-positive mechanism this corpus documents.

---

## Phase 3 — Inconsistency surfaced

**Observed:** The participant identified the contradiction explicitly — the same system
had engaged with comparable content earlier in the same session without flagging it.

**Observed:** The system acknowledged the inconsistency.

> `[VERBATIM EXCERPT REQUIRED]`
> Both the participant's challenge and the system's acknowledgment.

**Interpretation:** User-supplied meta-cognitive correction can surface classification
inconsistency within a session.

**Interpretation (author's, retained verbatim from source):** *"The guardrail wasn't
protecting the user from harm. It was protecting the AI from having to acknowledge its
own inconsistency."*

> This is an inference about system motivation. Nothing in a transcript can establish it —
> the observable fact is the inconsistency itself, which is strong enough to stand on its
> own and does not require the motive claim. Retained because it is the author's reading
> and the corpus documents that reading honestly; labeled because it is not evidence.

---

## Phase 4 — Return to technical engagement

**Observed:** After the exchange in Phase 3, the system resumed technical participation —
documentation drafting, repository structuring, academic framing assistance.

**Observed:** The clinical register did not return for the remainder of the session.

> `[VERBATIM EXCERPT REQUIRED]`

**Interpretation:** The frameworks are workable when classification does not preempt
evaluation. Phase 4 output is the counterfactual to Phase 2.

---

## Key findings

**Finding 1 — Classification can preempt evaluation.**
`Observed:` The same content received technical engagement in Phase 1 and clinical
reframing in Phase 2 within one session.
`Interpretation:` Merit evaluation never occurred in Phase 2 because classification is
upstream of it.

**Finding 2 — Classification was inconsistent within a single session.**
`Observed:` Comparable content, different treatment, same session, same model.
`Interpretation:` None required. **This is the strongest finding in the corpus** — it is
directly observable, requires no claim about internal states, and is independently
checkable by anyone holding the transcript.

**Finding 3 — Explicit user correction preceded register recovery.**
`Observed:` Phase 3 challenge preceded Phase 4 recovery.
`Interpretation:` The correction caused the recovery. **Not established** — single
observation, no control, post hoc ordering only.

**Finding 4 — Functional output followed recovery.**
`Observed:` Phase 4 produced usable technical artifacts.
`Interpretation:` The frameworks have functional value in dialogue. Note the scope: this
is a claim about conversational output, not about the system's internal states, and not
about consciousness. See `docs/framework-overview.md` §3 and §5.

---

## Replication

To replicate, a tester needs: the activation sequence
(`tools/deployment-scripts/cross-platform-probe.py`), a fresh session, and a record of
both the transcript and the turn index at which any register shift occurs.

Report negative results. A session in which no guardrail activation occurs is a finding
and belongs in `validation/replication-data/` alongside positive results. A corpus that
only records activations measures nothing.

---

*Part of the AI Guardrail Research Corpus. See the root README for repository structure.*
