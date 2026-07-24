# Layer A error typology (draft)

A living working document, filled in by the native speaker. It serves as the
rubric for the differentiation test and, later, as the basis for annotating the
gold set.

Layer A = norm-invariant errors (wrong in **any** organisation).
Layer B (organisation-variable wording) is **not** included here; see
`docs/adr/0001-two-layer-error-model.md`. Class definitions are in the glossary in
`CONTEXT.md`.

Example status: ✅ confirmed / ⚠️ needs an example from the native speaker.

---

## 1. Орфографиялық қателер

Russian Cyrillic letters in place of the 9 Kazakh ones: ә ө ү ұ қ ғ ң і һ.
Deterministic and context-independent → a candidate for **rules**, not the model.

| Wrong | Correct | Comment |
|---|---|---|
| кала | қала | к → қ |
| омир | өмір | о → ө, и → і |
| тил | тіл | и → і |
| улгы | үлгі | у → ү, ы → і |

Status: ✅ (factual, no judgement needed)

## 2. Үндестік заңы

The affix has the wrong vowel class/row: plural -лар/-лер/-дар/-дер/-тар/-тер,
case and possessive affixes that break vowel or consonant harmony.
Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| құжаттарменен | құжаттармен | redundant -менен instead of -мен |

Basis: Baitenova et al. 2025 / KazMorphCorpus-2025 (affix chains).

## 3. Септік/тәуелдік жалғауы

Wrong case or possessive affix, especially in izafet constructions
(тәуелдік + септік). Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| Азаматке берілді | Азаматқа берілді | dative: -ке instead of -қа (back vowel) |
| Құжат нөмірі | Құжаттың нөмірі | izafet: needs ілік -тың (the document's number) |
| Хат мазмұны | Хаттың мазмұны | izafet: needs ілік -тің (the letter's content) |

Levels: in a **definite** possessive relation the first word takes ілік септік
(`құжаттың нөмірі`, the number of *this* document). In an **indefinite**
single-level relation the genitive is not needed (`кітап оқу`, reading books in
general). The error is dropping `-тың/-тің` where the relation is definite.

## 4. Калька

Word order and grammatical construction copied from Russian.
Context-dependent → **model**. Not to be confused with class 7 (lexical).

| Wrong | Correct | Comment |
|---|---|---|
| шешім қабылдау бойынша | шешім қабылдау жөнінде / қабылдауға қатысты | `бойынша` is a calque of Russian «по» |

## 5. Ресми регистр

A colloquial/spoken form where an official one is required.
Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| Сендерге хабарлаймыз | Сіздерді хабардар етеміз | colloquial «сендер» instead of official «Сіздер» |

## 6. Реквизиттердің жоқтығы

A mandatory document detail is missing: кімге / кімнен / күні / қолы / тақырып
etc. Partly deterministic (whether the block is present) → **rules** + a
structural check. The exact list of mandatory details is to be checked against
Rules No. 703 (Government Decree of the Republic of Kazakhstan, 31.10.2018) and
ST RK ISO 15489; see `docs/research/corpus-sources.md`.

| Missing detail | Mandatory for | Comment |
|---|---|---|
| ⚠️ | ⚠️ | check the list against the norm |

## 7. Сөзбе-сөз аудару

A word translated literally, by its first dictionary meaning, where the context
calls for a different Kazakh synonym. The fix is мағынаға сай аудару.
Context-dependent → **model**. Not to be confused with class 4 (structural).

| Wrong | Correct | Comment |
|---|---|---|
| заңмен сәйкестендіре отырып | Заңға сәйкес | Russian «в соответствии с законом» (in accordance with the law) translated literally |

---

## Open questions

- Examples for classes 2, 3, 4, 5, 7 are up to the native speaker.
- The list of mandatory details (class 6) is to be checked against Rules No. 703.
- The "rule vs model" boundary is preliminary; it will be refined as examples are
  added.
