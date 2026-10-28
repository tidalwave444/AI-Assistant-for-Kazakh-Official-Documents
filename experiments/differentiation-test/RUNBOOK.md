# Differentiation test runbook

Hardware: **MacBook M1 Pro**; the scripts run in a **Lima VM** (Ubuntu, no sudo).
Everything is done locally; Kaggle is not needed.

What runs where:

| Where | What |
| --- | --- |
| **Lima** (VM terminal) | Python, `run.py`, `score.py`, downloading the model from Hugging Face |
| **macOS** (regular Mac terminal) | Ollama only: it needs Metal (GPU), and the VM has no GPU and only ~4 GB RAM for a 4.9 GB model |

Files are exchanged through a shared folder, written below as `<shared-dir>`
(for example `~/Downloads` on the Mac): it is mounted writable in Lima and
visible at the same path on both sides.
Three stages. Done by the native speaker. The result is a filled-in `scores.csv`
and the gate verdict.

Round 1 is 10 texts and ~1.5 hours. Do not try to do everything at once.

---

## Stage 0. Once: set up the environment (~20 min, 15 of them downloading)

### Python environment (Lima)

On Ubuntu `python3 -m venv` creates a venv without pip, and
`apt install python3-venv` needs sudo. So the environment is set up with `uv`
(already in `~/.local/bin`):

```bash
cd ~/projects/kazakh/experiments/differentiation-test
rm -rf .venv                       # old venv without pip: recreate it
uv venv .venv
uv pip install -r requirements.txt --python .venv/bin/python
source .venv/bin/activate
```

From here on, `python3` in every stage is the python from `.venv` (after
`source`). In a new terminal, run `source .venv/bin/activate` again.

### Gemini key (free, Lima)

1. https://aistudio.google.com/apikey → "Create API key" → copy it.
2. Save the key in the VM environment (the shell in Lima is bash, not zsh):

```bash
echo 'export GEMINI_API_KEY=paste_the_key' >> ~/.bashrc
source ~/.bashrc
```

### KazLLM through Ollama on the Mac

8B in 4-bit is 4.9 GB; it runs fine on the M1 Pro through Metal.

1. **macOS:** install Ollama with `brew install ollama` (or the .dmg from
   ollama.com) and start the app.
2. Accept the model's terms: log in to huggingface.co, open
   https://huggingface.co/issai/LLama-3.1-KazLLM-1.0-8B-GGUF4 and click agree
   (the repository is gated; the download will not work without this).
3. **Lima:** download the file into the shared folder. `uvx` runs `hf` without
   installing it and without sudo:

```bash
uvx --from huggingface_hub hf auth login     # paste a token from huggingface.co/settings/tokens
uvx --from huggingface_hub hf download issai/LLama-3.1-KazLLM-1.0-8B-GGUF4 \
   checkpoints_llama8b_031224_18900-Q4_K_M.gguf \
   --local-dir <shared-dir>/models/kazllm
printf 'FROM %s\n' <shared-dir>/models/kazllm/checkpoints_llama8b_031224_18900-Q4_K_M.gguf \
   > <shared-dir>/models/kazllm/Modelfile
```

4. **macOS:** build the model from the same file:

```bash
ollama create kazllm -f <shared-dir>/models/kazllm/Modelfile
ollama run kazllm "Сәлем, қалың қалай?"    # check that it answers
```

5. **Lima:** tell `run.py` where Ollama is. From the VM, `localhost` is the VM
   itself, and the Mac is visible as `host.lima.internal`:

```bash
echo 'export OLLAMA_HOST=http://host.lima.internal:11434' >> ~/.bashrc
source ~/.bashrc
curl -s $OLLAMA_HOST/api/tags              # should return JSON with kazllm
```

If `curl` prints nothing or "Connection refused", quit the Ollama app on the Mac
and start the server so that it listens beyond localhost:
`OLLAMA_HOST=0.0.0.0 ollama serve` (keep that terminal open).

If Ollama gives you trouble, **do not get stuck**: round 1 can be run on Gemini
alone, and KazLLM added in a second run (`run.py` appends results; what is
already done is not recomputed).

---

## Stage 1. Write 10 texts in `inputs.txt` (the main work)

### Format: plain text, not JSON

A block = one document; blocks are separated by an **empty line**. Inside a
block, a line of the form `<class>: wrong -> right` is an error; all other lines
are the text itself.

```
Азаматке анықтама берілді.
3: Азаматке -> Азаматқа
```

You can add the reason for the error on the same line after `|`:

```
3: Азаматке -> Азаматқа | dative case, back vowel → -қа
```

The reason is **not sent** to the model; it is shown only to you, on the
`score.py` card and in `outputs.md`. Do not write the reason as a separate line
without `#`: such a line becomes part of the document text and goes to the model
as a hint.

### What to write in round 1

- **10 texts**, short (1–3 sentences), plus **2 control texts** (class `0`, a
  text with no errors, to check whether the model spoils correct text).
- Classes **1–5**, about 2 texts per class. Classes 6 (document details) and 7
  (сөзбе-сөз) are in round 2; they need longer documents.
- Write errors the way people really make them: what you have seen in
  applications, memos, notices. Do not invent exotic cases.
- **One error, one clear defect.** At most two errors per text, otherwise you
  will not be able to tell what the model fixed.
- No personal data: "Азамат Т.", no IIN, addresses or real full names.
- Append **only to the end of the file**: ids (`d01`, `d02`…) are assigned in
  order, and inserting in the middle shifts the scores already given.

Realism matters more than quantity: 10 honest examples are better than 30
contrived ones.

### Check

```bash
python3 run.py --check
```

Prints how each block was parsed, how many documents and errors there are in
total and which classes are covered. If an error line is malformed, it simply
ends up in the document text, and you will see that in the output.

---

## Stage 2. Run (5–15 minutes of machine time)

```bash
python3 run.py
```

What happens: every text goes to every available model with a neutral prompt in
Kazakh. A model with no key, or one that is not running, is skipped with an
explanation. The result is `outputs.jsonl` and `outputs.md`.

The run can be interrupted: running it again fills in the missing
document × model pairs and leaves finished ones alone.

One model only: `python3 run.py --only gemini`.

---

## Stage 3. Score (~30–40 minutes)

```bash
python3 score.py
```

The script shows one card at a time: the input, which known error it contains,
and what the model returned. You press one letter:

- `f`: **fixed**, the model corrected this error properly;
- `m`: **missed**, it left it as it was;
- `b`: **broke**, it "corrected" it wrongly OR broke something that was correct;
- `s`: skip (you will come back to it), `q`: quit and save.

For control texts the question is different: `k` means it left the text alone
(ok), `b` means it made an unnecessary edit.

If the erroneous fragment remains verbatim in the output, the script hints that
this looks like `missed`. The hint is not a verdict; you decide: that is the
measurement.

The comment after the verdict can be skipped (Enter), but write one for failures:
these are live examples for the diploma.

Everything is written to `scores.csv` immediately, line by line. You can stop at
any time; the next run continues from the same place.

### Verdict

```bash
python3 score.py --report
```

Prints recall per class × model, the share of `broke`, false edits on control
texts, and the verdict against the thresholds fixed in advance (see `README.md`).

- **Niche proven** → the gate is passed, proceed to the product specification.
- **Round 2** → append 15 more texts with classes 6 and 7 to the end of
  `inputs.txt`, repeat stages 2–3. What is already scored is not rescored.

### What to look at beyond the numbers

- Which **classes** do the models fail systematically? Hypothesis: izafet
  (class 3), calque (class 4), register (class 5) are the weakest.
- **KazLLM vs Gemini**: where the Kazakh model is worse or better.
- Whether the model "fixes" what is already correct (control texts): an important
  risk for the product, since the user must not get spoiled text back.
