# ADR-0002: Evaluation methodology: gold set + calibrated LLM judge

Status: Accepted
Date: 2026-07-24

## Context

The project is an AI Engineering diploma; everything rests on being able to
measure whether things got better. There are no ready-made correction benchmarks
for Kazakh. Each of the two obvious approaches is insufficient on its own:

- Pure automatic metrics (exact match / F0.5) are misleading: agglutination yields
  dozens of valid forms of one correction, and exact match penalises correct
  answers.
- A pure LLM judge with no anchor is a hole: "a model praising a model", and the
  committee will open with "how do you know the judge is not wrong?".

## Decision

A two-part scheme with calibration, on Layer A only (see ADR-0001):

1. **Gold set**: ~150 texts annotated by hand by the native speaker (where the
   error is, its type, the correction). The ground-truth anchor.
2. **LLM judge with the Layer A rubric.** Before it is used, it is **validated**:
   we measure the judge's agreement with the manual annotation on the gold set
   (Cohen's kappa / agreement). Until then we do not trust the judge, and we say
   so.
3. **Baseline ladder** (rules → rules+API → rules+model, see ADR-0003), run
   through the validated judge on a large set → a defensible chart.

## Consequences

- The evaluation is measurable, reproducible and calibrated against the native
  speaker, which is rare even outside diploma projects.
- The question about the judge is answered with a number (agreement with the
  native speaker on 150 examples).
- Publishable contribution: the Layer A benchmark plus the methodology.
- Cost: the most labour-intensive part after the typology (manual annotation of
  150 texts, several weekends). Without it this is a demo, not engineering.
