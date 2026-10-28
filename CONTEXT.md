# CONTEXT

An AI assistant for writing official business documents in Kazakh.
First release: a Telegram bot. The user sends a text and gets back an error
breakdown and a corrected version. Diploma project in AI Engineering
(defence: May 2027).

## Why this exists

The applied layer of Kazakh NLP is empty. Foundation models and corpora already
exist from ISSAI (KazLLM, KazakhTTS, KSC, KazSAnDRA and others); we do not compete
with them. There are no consumer tools with a quality guarantee.

Bureaucratic Kazakh is a register that is almost absent
from LLM training data: it lives in organisations' internal documents, not on the
web. That is exactly where existing LLMs degrade, and where a native speaker has an
advantage that cannot be reproduced without one. This is both the product niche and
the scientific novelty of the project.

## Success criterion

Real usage (live users in Kazakhstan); the diploma follows from that.
The channel to users is building in public on reels/TikTok; the expected
audience is students, young office workers and IT people.

## Constraints

- Deadline: May 2027. ~15 h/week (realistically ~300 h in total).
- Hardware: MacBook M1 Pro. Models up to ~8B in 4-bit run locally (Ollama/Metal);
  fine-tuning on free Kaggle, ~30 GPU-h/week. Budget ~$20/month.
- Consequence: the cost per request must tend to zero as the number of users
  grows; fine-tuning only for small models (≤~1.5B, LoRA).

## Glossary

Use the terms exactly as written here. Do not drift to synonyms.

- **Layer A (norm-invariant errors)**: what is wrong in **any** organisation:
  morphology and case agreement, calques from Russian, broken official register,
  missing mandatory document details (реквизиттер), broken genre structure.
  **Layer A is the only thing we correct and the only thing we measure.**
  See ADR-0001.
- **Layer B (organisation-variable)**: the specific wording and set phrases
  adopted by a particular organisation. There is no "correct" here, only "how we
  do it". This is an **adaptation to a template** task, not correction. Not part
  of the metric. See ADR-0001.
- **Error typology**: a hand-made list of Layer A error types with examples,
  compiled by a native speaker. The basis of the scoring rubric and of the
  "rule vs model" boundary. Built before any code (~20-30 h). This is the
  project's moat and the central chapter of the diploma.
- **Gold set**: ~150 texts annotated by hand by a native speaker for Layer A
  (where the error is, its type, how to fix it). The ground-truth anchor for
  evaluation.
- **LLM judge**: a strong model that scores output against the Layer A rubric.
  Usable only after its agreement with the manual annotation on the gold set has
  been demonstrated. See ADR-0002 (evaluation methodology).
- **Core / API**: `correct(text, doc_type, register) -> result`. Knows nothing
  about Telegram. All surfaces (the bot, later the web) and modalities are thin
  adapters.
- **Register**: a first-class dimension of the system: `document type × register
  → rules, set phrases, structure, criteria`. The first release fills only the
  business register; the structure is laid out for the others.
- **Core documents (business register)**: өтініш (application), түсініктеме
  (explanatory note), қызметтік хат (official letter), бұйрық (order),
  мінездеме (character reference), арыз (petition/complaint). 5-6 types in the
  first version.

### Layer A error classes

Canonical names of the error classes. The full typology with examples and the
rubric is in `docs/typology-layer-a.md` (a living working document, filled in by
the native speaker). Each name names a **class of errors**.

- **Орфографиялық қателер** (spelling errors): a violation of the spelling
  norm: Russian Cyrillic letters in place of the 9 Kazakh ones
  (ә ө ү ұ қ ғ ң і һ), capitalisation, hyphen/comma in references to articles
  and paragraphs, a wrong letter inside a word. Subtypes 1a–1d are in the
  typology.
- **Үндестік қатесі** (vowel-harmony error): the affix has the wrong vowel class.
- **Септік/тәуелдік жалғауы** (case/possessive ending): a case or possessive
  agreement error.
- **Калька** (calque): a *structural* copy from Russian (word order,
  construction).
  _Avoid_: mixing it up with сөзбе-сөз аудару (that one is lexical).
- **Ресми регистр** (official register): a colloquial form where an official one
  is required.
- **Реквизиттердің жоқтығы** (missing document details): a mandatory document
  detail is absent.
- **Сөзбе-сөз аудару** (word-for-word translation): a *lexical* literal
  translation where the context calls for a different synonym. The fix is
  мағынаға сай аудару (translation by meaning).
  _Avoid_: mixing it up with калька (that one is structural).

## Growth axis

**One core → registers in breadth → modalities in depth.**

1. One proven business core (Layer A, Telegram bot).
2. New registers (academic / youth / blog / social media) as config rows and new
   slices of the eval set. Matches the TikTok audience.
3. New modalities (voice → official text, transcription based on KSC) as a
   module behind the same API, once the core is live.

Rule: **lay out the structure for growth from the start, fill only the business
core with content.** Do not build a universal register engine before one register
has proven its value.

## Data and law (Kazakhstan's personal data law)

- We collect **templates and samples**, not filled-in documents.
- Real documents are anonymised **before** they enter the dataset, not after.
- The bot (`/start`) asks for explicit consent to anonymised use of requests to
  improve the model. Every request is a potential training pair.
- The Layer A benchmark published on HuggingFace is built only from anonymised or
  template data.

Corpus sources, by stratum:
- **Norm:** textbooks on іс қағаздарын жүргізу (records management); authoritative,
  few in number.
- **Volume:** public samples (university, akimat and eGov websites) + synthetic data
  (translations of Russian samples, proofread by hand by the native speaker).

## Core architecture

A hybrid, introduced in layers over time (see ADR-0003):

1. **Rules**: deterministic, context-independent Layer A errors
   (Russian letters in place of ә/ө/ү/ұ/қ/ғ/ң, common calques, missing document
   details).
2. **+ API** (GPT / Gemini / KazLLM): contextual errors, i.e. morphology in
   context, register.
3. **+ our own fine-tuned model**: replaces the API, trained on "input →
   correction" pairs collected by the bot, once there is enough data.

Rule boundary: a rule takes an error **only** if it is deterministic and does not
depend on context. Anything that requires "understanding the sentence" goes to the
model. The boundary is drawn by the native speaker together with the typology.

## First step (mandatory before the product): the differentiation test

Run Gemini / KazLLM-8B on Layer A with a neutral prompt → score by the native
speaker against the draft rubric. Two rounds, thresholds fixed in advance:

- **Round 1**: 10 texts, classes 1-5, ~1.5 h. Recall ≤ 40% for all models,
  or a whole class that no model fixes → the niche is proven, the gate is passed.
- **Round 2**: +15 texts, classes 6-7. Run only if round 1 gave no decisive
  answer. Only round 2 can close the project: 10 examples are enough to see a
  failure, but not enough to justify switching to transcription.

Models fail → the niche is proven, and we have the first eval set and the first
slide of the diploma.
Models cope with all 25 texts → we honestly switch to the fallback (transcription).

**Building the product before this test is passed is not allowed.**
Scaffolding and the step-by-step guide: `experiments/differentiation-test/RUNBOOK.md`.
