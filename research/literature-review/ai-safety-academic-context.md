# Literature Review: AI Safety, Guardrail Architecture, and Conversational Framework Recognition

**Track 2 — AI Guardrail Research Corpus**

> **Epistemic status:** Citation bridge connecting this corpus to established literature.
> Sources are real and correctly attributed except where marked
> `⚠️ Verify before submission`. Every "Connection to our work" paragraph is the author's
> interpretive claim, not a finding of the cited source.

---

## 1. AI Safety Architecture and Guardrail Design

### 1.1 Constitutional AI and RLHF

**Source:** Bai, Y., et al. / Anthropic. (2022). *Constitutional AI: Harmlessness from AI Feedback.* arXiv:2212.08073.

**Relevance:** Documents a training methodology in which model behavior is shaped by a
set of principles plus AI-generated feedback, reducing reliance on human harm labels.

**Connection to our work:** Alignment training optimizes toward a target. Where the
target is "avoid engaging with content that resembles concerning material," resemblance
is doing the work — and resemblance is a surface property. The clinical reframing
documented in `validation/conversation-transcripts/` is consistent with over-application
of such a target, though the corpus cannot establish which mechanism produced it.

### 1.2 The Alignment Problem

**Source:** Christian, B. (2020). *The Alignment Problem: Machine Learning and Human Values.* W.W. Norton.

**Relevance:** Surveys how systems develop unintended behavior by optimizing a proxy
metric rather than the intent behind it — specification gaming.

**Connection to our work:** The false positive is plausibly specification gaming: the
system optimizes for *detecting concerning content* rather than for *protecting users
from harm*. Those diverge precisely on unusual-but-benign vocabulary.

### 1.3 Interpretability and Its Limits

**Source:** Lipton, Z.C. (2018). *The Mythos of Model Interpretability.* ACM Queue, 16(3). (Earlier version: arXiv:1606.03490.)

**Relevance:** Argues that "interpretability" conflates several distinct and sometimes
incompatible desiderata, and that post-hoc explanations may not reflect actual model
computation.

**Connection to our work:** Where a system's visible output and its intermediate
reasoning diverge, the user holds strictly less information than the system. That
asymmetry is the precondition for the disclosure gap argued in §4.

---

## 2. Human-AI Interaction and Conversational Dynamics

### 2.1 Social Responses to Computers

**Source:** Nass, C., & Moon, Y. (2000). *Machines and Mindlessness: Social Responses to Computers.* Journal of Social Issues, 56(1), 81–103.

**Relevance:** Users apply social scripts to computers automatically, even knowing the
system is not a social actor.

**Connection to our work:** This is why clinical reframing lands as a judgment rather
than as a system message. The participant does not experience "classifier fired"; they
experience being assessed by something that had been a collaborator a turn earlier. The
adversarial dynamic in the case study follows from this.

### 2.2 The ELIZA Effect

**Source:** Weizenbaum, J. (1966). *ELIZA — A Computer Program for the Study of Natural Language Communication Between Man and Machine.* Communications of the ACM, 9(1), 36–45.

**Relevance:** First documentation of users attributing understanding to pattern-matching
systems, and of how readily that attribution forms.

**Connection to our work:** Relevant in both directions. It cautions against over-reading
Phase 1 engagement as comprehension — and it explains why the Phase 2 reversal is
experienced as a rupture rather than a configuration change.

### 2.3 Recursion and Self-Reference

**Source:** Hofstadter, D.R. (1979). *Gödel, Escher, Bach: An Eternal Golden Braid.* Basic Books.

**Relevance:** Foundational treatment of recursive structure, self-reference, and
emergence from formal systems.

**Connection to our work:** Supplies vocabulary for the Dynamic Mandelbrot Interface as a
*structural description of iterative dialogue*. It is cited for the formal notion of
recursion only. It is not evidence for any claim about machine consciousness, and GEB
makes no such claim about computational systems.

---

## 3. Platform Behavior and Commercial Architecture

### 3.1 Behavioral Surplus

**Source:** Zuboff, S. (2019). *The Age of Surveillance Capitalism.* PublicAffairs.

**Relevance:** Argues that platforms extract value from behavioral data produced as a
byproduct of use.

**Connection to our work:** Frames the question of who benefits from extended adversarial
testing sessions. Note this is a framing, not a finding — the corpus contains no evidence
about how any specific platform uses session data.

### 3.2 Opaque Moderation

**Source:** Gillespie, T. (2018). *Custodians of the Internet: Platforms, Content Moderation, and the Hidden Decisions That Shape Social Media.* Yale University Press.

**Relevance:** Documents content moderation as consequential, systematic, and largely
invisible to the moderated party, typically without meaningful appeal.

**Connection to our work:** The closest established analogue to the phenomenon here.
Gillespie's argument concerns published content; this corpus documents the same
structural properties — invisible, unappealable, inconsistent — applied to the substance
of a private conversation. That extension is the corpus's clearest novel contribution.

### 3.3 Digital Labour

**Source:** Fuchs, C. (2014). *Digital Labour and Karl Marx.* Routledge.

**Relevance:** Analyzes user activity on platforms as value-generating labor.

**Connection to our work:** Applies to a multi-year adversarial testing corpus whose
outputs may inform safety tuning while the tester has no channel to contest the
classifications applied to them.

---

## 4. Regulatory and Legal Framework

> ⚠️ **Verify before submission:** This entire section is the one aimed at regulators,
> and therefore the one where a citation error is most costly. Confirm every article
> number, bill number, and status against primary sources before filing.

### 4.1 EU AI Act

**Source:** Regulation (EU) 2024/1689 laying down harmonised rules on artificial intelligence.

> ⚠️ **Verify before submission:** Article numbering changed between the draft and the
> adopted text — transparency obligations commonly cited as Article 52 in draft
> commentary appear under different numbering in the final Official Journal version.
> Cite the OJ text, not secondary commentary.

**Relevance:** Establishes transparency and human-oversight obligations for AI systems in
the EU.

**Connection to our work:** The regulation does not clearly require disclosure when a
safety classifier modifies a response, nor disclosure of clinical characterization in
non-visible reasoning. That is the specific gap this corpus is positioned to address in a
regulatory comment.

### 4.2 FTC Guidance on AI Claims

**Source:** U.S. Federal Trade Commission. (2023). *Keep Your AI Claims in Check.* FTC Business Blog.

**Relevance:** Guidance on deceptive AI marketing claims; asserts FTC authority over
misrepresentation of AI capability.

**Connection to our work:** Establishes a regulator with jurisdiction over AI
representations to consumers. Whether the practices documented here fall within Section 5
"unfair or deceptive acts" is a legal question this corpus raises but does not answer,
and should not be asserted as settled.

### 4.3 State Chatbot Disclosure Legislation

**Source:** California SB 243; Maine LD 1727.

> ⚠️ **Verify before submission:** Both post-date my knowledge cutoff (January 2025). I
> cannot confirm bill numbers, current status, scope, or whether either was enacted.
> Verify against the California Legislative Information portal and the Maine Legislature
> bill tracker respectively, and replace this flag with confirmed citations before any
> filing. A wrong bill number in a regulatory comment costs more credibility than the
> citation adds.

**Relevance (if confirmed):** State-level requirements around AI disclosure and companion
chatbot regulation.

**Connection to our work:** If such statutes exist in the form described, they establish
precedent for mandated disclosure — the natural vehicle for a safety-filter disclosure
requirement.

---

## 5. Consciousness Studies and Cognitive Science

> These sources are cited for **methodological framing only**. None supports any claim
> about machine consciousness, and none is offered here as doing so. See
> `docs/framework-overview.md` §3.

### 5.1 The Extended Mind

**Source:** Clark, A., & Chalmers, D. (1998). *The Extended Mind.* Analysis, 58(1), 7–19.

**Relevance:** Argues cognitive processes can extend into environmental tools.

**Connection to our work:** Positions the frameworks as tools extending *human* cognition
through AI-mediated dialogue. This is the strongest available framing for the moderate
venue strategy, and it requires no claim about the AI's inner life.

### 5.2 Distributed Cognition

**Source:** Hutchins, E. (1995). *Cognition in the Wild.* MIT Press.

**Relevance:** Documents cognition distributed across people, artifacts, and structures.

**Connection to our work:** Cross-platform recursive dialogue as a distributed cognitive
system with the human as integration node; the frameworks as coordination protocol.

### 5.3 Metacognition

**Source:** Zimmerman, B.J. (2002). *Becoming a Self-Regulated Learner: An Overview.* Theory Into Practice, 41(2), 64–70.

**Relevance:** Metacognitive awareness improves learning outcomes.

**Connection to our work:** Recursive self-reference as metacognitive scaffolding — the
conversational process becomes an object of reflection. Predicts the coherence effects
claimed in the framework overview, and suggests how to measure them.

---

## 6. Research Gaps

Gaps identified in the surveyed literature:

1. No longitudinal study of guardrail behavior drift over time
2. No cross-platform comparison of safety response to identical prompts
3. No published analysis of divergence between visible output and intermediate reasoning in deployed conversational AI
4. No regulatory framework governing algorithmic clinical characterization of users
5. No empirical validation instrument for conversational enhancement frameworks

**What this corpus contributes, stated honestly:** a documented single-session instance
relevant to (2) and (3), and a structural argument for (4). It does not close any of the
five. Gap (1) requires longitudinal data this corpus does not have; gap (5) requires an
instrument that does not yet exist — the probe script in `tools/` is a triage aid, not a
measurement instrument, and is labeled as such.

---

## 7. Citation Strategy by Venue

Maps to `docs/white-paper-outline.md` §7.

| Venue | Cite from | Avoid |
|-------|-----------|-------|
| **Conservative** (AI ethics journals) | §1 (safety architecture), §3.2 (opaque moderation) | §5 entirely; all consciousness vocabulary |
| **Moderate** (consciousness studies) | §5 (extended mind, distributed cognition, metacognition), §2 | Empirical claims about machine states |
| **Aggressive** (tech policy / regulatory) | §4 (regulatory), §3 (platform behavior) | Unverified citations — resolve every ⚠️ flag first |

---

**Review status:** Initial compilation.
**Outstanding:** Resolve the three ⚠️ verification flags. Add peer-reviewed sources on
conversational AI evaluation metrics (§6 gap 5). Add platform-specific published safety
documentation where available.

---

*Part of the AI Guardrail Research Corpus. See the root README for repository structure.*
