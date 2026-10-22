# Differentiation test (PROTOTYPE, throwaway)

> ⚠️ This is an **experiment**, not the product. It answers one question and is thrown away.
> Not production code: no tests, no error handling beyond what is needed.

## The question it answers

Do existing LLMs fail on **Layer A** of official Kazakh?

- **They fail** → there is a niche, we build the product.
- **They cope** → there is no product, we switch to transcription.

This is a **gate**: the product is not built until it is passed. See `CONTEXT.md`.

## Two rounds instead of one big run

The test used to require 20–30 texts and all 7 classes before the first run. That
is too much input for one sitting, so it is split into two rounds.

**Round 1: 10 texts, classes 1–5, 2 control texts.** ~1.5 hours of work.
Answers the question in its crudest form: do the models fix Layer A at all.

**Round 2: +15 texts, classes 6 and 7 are added.** Run only if round 1 gave no
decisive answer.

The thresholds are fixed **in advance** (they are also hard-coded in `score.py`), so
there is no fitting afterwards:

| Round 1 result | Verdict |
|---|---|
| recall ≤ 40% for all models, **or** a whole class that no model fixes | **Niche proven.** Gate passed, build the product |
| recall ≥ 85% for all models | Models cope on this sample → **round 2** |
| in between | There is a signal, but not a decisive one → **round 2** |

The asymmetry is deliberate and declared in advance: 10 examples are enough to see
a failure, but not enough to close the project. Only round 2 on 25 texts can kill
it. This is not fitting: round 1 cannot confirm the hypothesis, it can only send
us to round 2.

Of special interest: a failure of **KazLLM** (a Kazakh model that cannot handle
official Kazakh) is the strongest argument for the niche.

## How it works

1. `inputs.txt`: texts with errors, in a plain-text format (not JSON).
   Written by the native speaker (you).
2. `python3 run.py --check` shows how the file was parsed. The format is almost
   impossible to break, but it is worth checking.
3. `python3 run.py` runs every text through every model with a **neutral**
   prompt → `outputs.jsonl` (for the scorer) + `outputs.md` (for reading).
   An interrupted run resumes where it stopped.
4. `python3 score.py` is interactive: it shows one error and one model output,
   and you press `f`/`m`/`b`. No CSV to fill in by hand. You can stop at any
   time.
5. `python3 score.py --report` prints recall per class × model and the gate
   verdict.

## Why the prompt is neutral

We do NOT give the model the 7 classes. Otherwise we would be testing our prompt,
not the model's own ability. The whole niche hypothesis is "the models make
mistakes on their own". A neutral prompt is the only fair test for the gate.

The prompt stays in Kazakh on purpose: it is part of the experimental condition.

The typology prompt (the second condition from
`docs/research/assignment-1-research-topic.md`) is added **after** the gate, for
the research part.

## Models (hardware: MacBook M1 Pro)

- **Gemini**: free API (key from aistudio.google.com), the `google-genai` package.
- **KazLLM-8B**: the official 4-bit GGUF from ISSAI
  (`issai/LLama-3.1-KazLLM-1.0-8B-GGUF4`, Q4_K_M, 4.9 GB), run locally through
  **Ollama** on Metal. Kaggle is no longer needed. CC BY-NC 4.0: non-commercial,
  fine for the test.
- Adding GPT/Claude is one provider function in `run.py`. Not a blocker.
