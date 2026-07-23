# ADR-0001: Two-layer error model (Layer A is normed, Layer B is parameterised)

Status: Accepted
Date: 2026-07-24

## Context

There is no single norm for Kazakh official business writing: every organisation
writes its own way. So the word "correct" is ambiguous, and a single correction
metric cannot cover it. If an organisation's own wording counts as an "error", the
product will correct the user on things that are normal in their organisation, and
lose their trust the first time. In the diploma such a metric collapses under the
question "whose norm did you use to call it an error?".

## Decision

Errors are split into two layers:

- **Layer A (norm-invariant)**: wrong in any organisation: morphology and case
  agreement, calques from Russian, broken official register, missing mandatory
  document details, broken genre structure.
  **We correct and measure only Layer A.**
- **Layer B (organisation-variable)**: specific wording and set phrases.
  Not corrected; adapted to the user's template (second release). It is **not
  part of** the metric, and this is stated explicitly.

## Consequences

- The metric is unambiguous and defensible: a Layer A "error" does not depend on
  the organisation.
- The differentiation test is fair: GPT is run on Layer A only, so the conclusion
  "the LLM degrades" cannot be dismissed with "you made up your own norm".
- Scientific novelty: a formalisation of the class of norm-invariant errors in
  Kazakh official text, plus a benchmark for it.
- Cost: the native speaker compiles the Layer A typology by hand (~20-30 h) before
  any code. This is a deliberate investment (the moat and a chapter of the
  diploma).
- The product positioning is more honest: "I remove errors and adapt to your
  style", not "write like the textbook".
