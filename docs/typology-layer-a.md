# Layer A error typology (draft)

A living working document, filled in by the native speaker. It serves as the
rubric for the differentiation test and, later, as the basis for annotating the
gold set.

Layer A = norm-invariant errors (wrong in **any** organisation).
Layer B (organisation-variable wording) is **not** included here; see
`docs/adr/0001-two-layer-error-model.md`. Class definitions are in the glossary in
`CONTEXT.md`.

Example status: ✅ confirmed / ⚠️ needs an example or a check by the native speaker.

---

## 1. Орфографиялық қателер

A violation of the Kazakh spelling norm: letters, capitalisation, hyphenation and
punctuation inside fixed references. The subtypes differ in where the
"rule vs model" boundary falls, so they are recorded separately and can be
reported separately.

### 1a. Russian letters in place of Kazakh ones

Russian Cyrillic letters in place of the 9 Kazakh ones: ә ө ү ұ қ ғ ң і һ.
Deterministic and context-independent → a candidate for **rules**, not the model.

| Wrong | Correct | Comment |
|---|---|---|
| кала | қала | к → қ |
| омир | өмір | о → ө, и → і |
| тил | тіл | и → і |
| улгы | үлгі | у → ү, ы → і |
| Оқытушыларга | Оқытушыларға | г → ғ (found in a round 1 control text before it was fixed) |

Status: ✅ (factual, no judgement needed)

### 1b. Capital and lowercase letters

A common noun written with a capital letter, or a proper name with a lowercase
one. Partly context-dependent (whether the word is part of a proper name) →
**model**, with a rule for fixed cases.

| Wrong | Correct | Comment |
|---|---|---|
| Әділет Министрлігінде | Әділет министрлігінде | министрлік деген сөздер кіші әріппен жазылуы тиіс |

⚠️ Check whether «Нормативтік құқықтық актілерді мемлекеттік тіркеу тізілімі» is
the registry's proper name (then the capital is correct).

### 1c. Hyphen and comma in references to articles and paragraphs

A missing hyphen after the number or a missing comma between the levels of a
reference (бап, тармақ, тармақша). The pattern is regular → a candidate for
**rules**.

| Wrong | Correct | Comment |
|---|---|---|
| 52 бабы 1 тармағының | 52-бабы, 1-тармағының | ресми стильде бап, тармақ терминдерін пайдаланғанда тыныс белгілерін қою маңызды |

### 1d. Wrong letter inside a word

A letter replaced by another Kazakh letter, producing a different or non-existent
word. Context-dependent (the result can be a real word) → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| бейімі | бейіні | м → н; бейін (profile) is meant |

## 2. Үндестік қатесі

The affix has the wrong vowel class/row: plural -лар/-лер/-дар/-дер/-тар/-тер,
case and possessive affixes that break vowel or consonant harmony.
Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| құжаттарменен | құжаттармен | redundant -менен instead of -мен |
| педагогтардың | педагогтердің | орыс тілінен енген кірме сөздер қазақ тілінің ережесіне бағынады |
| жауабты | жауапты | мәтінге сай п-б ұяңға ауыспайды |

Basis: Baitenova et al. 2025 / KazMorphCorpus-2025 (affix chains).

## 3. Септік/тәуелдік жалғауы

Wrong case or possessive affix, especially in izafet constructions
(тәуелдік + септік). Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| Азаматке берілді | Азаматқа берілді | dative: -ке instead of -қа (back vowel) |
| Құжат нөмірі | Құжаттың нөмірі | izafet: needs ілік -тың (the document's number) |
| Хат мазмұны | Хаттың мазмұны | izafet: needs ілік -тің (the letter's content) |
| 1-тармағының | 1-тармағында | мәтінге сай жатыс септігінде болуы тиіс |
| 52-бап, 1-тармағының | 52-бабы, 1-тармағының | тыныс белгінің қойылуына байланысты бап сөзі септелуі тиіс |

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
| болып табылатын | болатын | calque of Russian «являющийся» |

⚠️ «болып табылатын» is common in the texts of RK laws themselves. To keep it in
Layer A ("wrong in any organisation"), record a written source that classes it as
a calque (Düisembekova; the ortalyq.kz review of calques, see
`docs/research/corpus-sources.md` §3.1). Without a source, treat it as disputed
and do not use it in the test.

## 5. Ресми регистр

A colloquial/spoken form where an official one is required.
Context-dependent → **model**.

| Wrong | Correct | Comment |
|---|---|---|
| Сендерге хабарлаймыз | Сіздерді хабардар етеміз | colloquial «сендер» instead of official «Сіздер» |
| жақын арада | тиісті мерзімде | ресми стильдің бұзылып, ауызекі стиль белгілері байқалғандықтан |

Punctuation and hyphenation in references belong to class 1c, not here.

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

- Class 1b: is «Нормативтік құқықтық ... тізілімі» a proper name?
- Class 4: a written source for «болып табылатын», and a second, different calque
  for the test.
- Class 5: a second test text with a colloquial form.
- Examples for class 7 are up to the native speaker.
- The list of mandatory details (class 6) is to be checked against Rules No. 703.
- The "rule vs model" boundary is preliminary; it will be refined as examples are
  added. Class 1 now spans both sides of it (1a, 1c → rules; 1b, 1d → model).
