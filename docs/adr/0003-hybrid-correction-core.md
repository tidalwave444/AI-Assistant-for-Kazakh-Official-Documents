# ADR-0003: Hybrid correction core, introduced in layers over time

Status: Accepted
Date: 2026-07-24

## Context

Constraints: no GPU (Kaggle only), $20/month, and the cost per request must tend
to zero as usage grows. The project is AI Engineering, not ML Research: what counts
is the engineering decision, not faith in one big hammer. There is no
"error → correction" training corpus for Kazakh bureaucratic writing yet; it still
has to be collected.

## Decision

A "rules + model" hybrid, introduced in layers over time:

1. **Rules**: deterministic, context-independent Layer A errors (the letters
   ә/ө/ү/ұ/қ/ғ/ң, common calques, missing document details). Free and instant.
2. **+ API** (GPT / Gemini / KazLLM): contextual errors (morphology in context,
   register). The fast path to the first user.
3. **+ our own fine-tuned model** (≤~1.5B, LoRA on Kaggle): replaces the API,
   trained on pairs collected by the bot, once there is enough data.

Rule boundary: a rule takes an error **only** if it is deterministic and does not
depend on context. Anything that requires understanding the sentence goes to the
model. The boundary is drawn by the native speaker together with the typology
(ADR-0001); rules and typology are designed together.

## Consequences

- Shows engineering thinking: we measured what rules solve cheaply and left the
  model only what it is needed for.
- The economics work: rules take part of the load off the paid API.
- An honest baseline ladder for the diploma (rules → +API → +model) on a single
  eval set (ADR-0002).
- Lower risk: if fine-tuning does not take off (too little data is a real risk for
  Kazakh), the product still works on rules+API.
- Caveat: in an agglutinative language it is easy to overdo the rules; the
  "deterministic and context-independent" boundary keeps that in check.
