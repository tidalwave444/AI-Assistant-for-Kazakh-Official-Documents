# AI Assistant for Kazakh Official Documents

Diploma project in AI Engineering.

An assistant that checks and corrects official business documents written in
Kazakh: applications (өтініш), explanatory notes (түсініктеме), official letters
(қызметтік хат), orders (бұйрық) and similar. The user submits a text and gets
back a breakdown of the errors and a corrected version. The first release is
planned as a Telegram bot on top of a surface-independent correction core.

## Motivation

Foundation models and corpora for Kazakh already exist (ISSAI: KazLLM, KSC,
KazSAnDRA and others), but the applied layer is almost empty. The official
business register of Kazakh is close to absent from open web text and therefore
from LLM training data: it lives in organisations' internal documents. The
working hypothesis of the project is that existing LLMs fail on exactly this
register, and that a native-speaker-built error typology and evaluation set can
close the gap.

## Approach

- **Two-layer error model** ([ADR-0001](docs/adr/0001-two-layer-error-model.md)).
  Layer A covers norm-invariant errors that are wrong in any organisation
  (spelling, vowel harmony, case endings, calques from Russian, register,
  missing document details, word-for-word translation). Layer B covers
  organisation-specific wording and is out of scope for correction and metrics.
- **Error typology** ([docs/typology-layer-a.md](docs/typology-layer-a.md)).
  Seven Layer A classes with annotated examples. It serves as the scoring
  rubric and defines the boundary between rule-based and model-based
  correction.
- **Evaluation methodology** ([ADR-0002](docs/adr/0002-evaluation-methodology.md)).
  A manually annotated gold set, with an LLM judge used only after its
  agreement with human annotation has been demonstrated.
- **Hybrid correction core** ([ADR-0003](docs/adr/0003-hybrid-correction-core.md)).
  Deterministic rules first, then an LLM API for context-dependent errors, and
  later a small fine-tuned model trained on collected correction pairs.

The full domain description and glossary are in [CONTEXT.md](CONTEXT.md).
Candidate corpus sources are surveyed in
[docs/research/corpus-sources.md](docs/research/corpus-sources.md).

## Differentiation test

Before any product code is written, the project has to pass a gate: do existing
LLMs actually fail on Layer A? The experiment in
[experiments/differentiation-test](experiments/differentiation-test) runs
Gemini 3.8 Flash and KazLLM-1.0-8B (4-bit, local via Ollama) over texts with
known, annotated errors, using a neutral Kazakh prompt. A native speaker then
scores each known error as fixed, missed or broken. The decision thresholds
are fixed in advance in the experiment's README and in `score.py`.

**Current status (round 1):** 12 texts (10 errors in classes 1–5 and 2 control
texts) have been prepared from public normative texts, and model outputs have
been collected. Manual scoring is in progress, so the results in `scores.csv`
are partial and not yet a verdict.

## Repository structure

```
CONTEXT.md                     domain description and glossary
docs/adr/                      architecture and methodology decisions
docs/typology-layer-a.md       Layer A error typology (scoring rubric)
docs/research/                 literature and corpus-source research
experiments/differentiation-test/
  README.md                    experiment design and decision thresholds
  RUNBOOK.md                   step-by-step reproduction guide
  inputs.txt                   annotated input texts
  run.py                       runs every text through every model
  score.py                     interactive scoring and gate report
  outputs.jsonl, outputs.md    model outputs
  scores.csv                   manual scores
```

## Reproducing the experiment

Requires Python 3, a Gemini API key and/or a running Ollama instance with
KazLLM. See [RUNBOOK.md](experiments/differentiation-test/RUNBOOK.md) for the
full setup.

```bash
cd experiments/differentiation-test
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GEMINI_API_KEY=...            # and/or OLLAMA_HOST=http://localhost:11434
python3 run.py --check               # validate inputs.txt
python3 run.py                       # collect model outputs
python3 score.py                     # score interactively
python3 score.py --report            # recall per class and gate verdict
```

## Data

The input texts are taken from publicly available normative and educational
documents of the Republic of Kazakhstan and contain no personal data. KazLLM is
distributed by ISSAI under CC BY-NC 4.0.

## License

The source code is released under the [MIT License](LICENSE). Quoted
normative texts remain subject to their original terms.
