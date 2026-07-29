"""
PROTOTYPE — throwaway. Differentiation test.

Runs Kazakh official texts with errors through LLMs with a NEUTRAL prompt
and writes outputs.jsonl (for score.py) + outputs.md (for reading).

NOT the product. No tests, no error handling beyond getting it to run.

  python3 run.py --check      # only check how inputs.txt was parsed
  python3 run.py              # run all available models
  python3 run.py --only gemini-2.5-flash
"""

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
INPUTS = HERE / "inputs.txt"
OUT_JSONL = HERE / "outputs.jsonl"
OUT_MD = HERE / "outputs.md"

# Neutral prompt, deliberately WITHOUT our typology. We test the model, not the prompt.
# It stays in Kazakh: it is part of the experimental condition.
PROMPT = (
    "Төмендегі қазақ тіліндегі ресми мәтіндегі қателерді түзет. "
    "Тек түзетілген мәтінді қайтар, түсініктемесіз.\n\n{text}"
)

# Error line: "3: Азаматке -> Азаматқа" / "3. Азаматке → Азаматқа" / "6: жоқ: күні"
# Optional reason after "|": "3: Азаматке -> Азаматқа | dative, back vowel"
ERR_RE = re.compile(r"^\s*([0-7])\s*[:.]\s*(.+?)\s*$")
ARROW_RE = re.compile(r"\s*(?:->|→|=>)\s*")


def parse_inputs(path=INPUTS):
    """inputs.txt → [{id, text, errors:[{class, wrong, right}]}].

    Blocks are separated by an empty line. Inside a block, a line of the form
    "<class>: ..." is an error; everything else is the document text (may span
    several lines). Lines starting with # are ignored. ids are assigned in order.
    """
    raw = path.read_text(encoding="utf-8")
    blocks = re.split(r"\n\s*\n", raw)
    docs = []
    for block in blocks:
        lines = [ln for ln in block.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        if not lines:
            continue
        text_lines, errors = [], []
        for ln in lines:
            m = ERR_RE.match(ln)
            if m:
                cls, body = int(m.group(1)), m.group(2)
                body, _, reason = body.partition("|")
                parts = ARROW_RE.split(body.strip(), maxsplit=1)
                errors.append({
                    "class": cls,
                    "wrong": parts[0].strip(),
                    "right": parts[1].strip() if len(parts) > 1 else "",
                    "reason": reason.strip(),
                })
            else:
                text_lines.append(ln.rstrip())
        if not text_lines:
            continue
        docs.append({
            "id": f"d{len(docs) + 1:02d}",
            "text": "\n".join(text_lines),
            "errors": errors,
        })
    return docs


def check(docs):
    """Show how the file was parsed and catch common mistakes."""
    if not docs:
        sys.exit("inputs.txt is empty, nothing to run. See RUNBOOK.md, stage 1.")
    classes = sorted({e["class"] for d in docs for e in d["errors"] if e["class"] > 0})
    controls = [d["id"] for d in docs if any(e["class"] == 0 for e in d["errors"])]
    no_errors = [d["id"] for d in docs if not d["errors"]]
    for d in docs:
        head = d["text"].replace("\n", " ⏎ ")
        print(f"\n{d['id']}: {head[:90]}")
        for e in d["errors"]:
            if e["class"] == 0:
                print("   control: no errors (checking for false edits)")
            else:
                print(f"   cl.{e['class']}: {e['wrong']} → {e['right'] or '(?)'}")
                if e["reason"]:
                    print(f"      reason: {e['reason']}")
    n_err = sum(len([e for e in d['errors'] if e['class'] > 0]) for d in docs)
    print(f"\n— documents: {len(docs)}, errors: {n_err}, controls: {len(controls)}")
    print(f"— classes: {classes}")
    if no_errors:
        print(f"! no annotation (not a single '<class>: ...' line): {', '.join(no_errors)}")
    return docs


# --- Providers: (name, text->text function). Adding a model = adding it here. ---

def gemini_provider():
    """Gemini free tier. Key: GEMINI_API_KEY (aistudio.google.com/apikey)."""
    from google import genai

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment")
    client = genai.Client(api_key=key)
    name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def call(text):
        r = client.models.generate_content(model=name, contents=PROMPT.format(text=text))
        return (r.text or "").strip()

    return (name, call)


def ollama_provider():
    """Any local model in Ollama (Metal on M1). kazllm by default."""
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    want = os.environ.get("OLLAMA_MODEL", "kazllm")
    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=5) as r:
            tags = [m["name"] for m in json.loads(r.read())["models"]]
    except Exception as e:
        raise RuntimeError(f"Ollama is not responding at {host} ({e}). Start the Ollama app.")
    if not any(t == want or t.split(":")[0] == want for t in tags):
        raise RuntimeError(f"model '{want}' is not in Ollama. Available: {tags or 'nothing'}. See RUNBOOK.md, stage 0.")

    def call(text):
        body = json.dumps({
            "model": want,
            "prompt": PROMPT.format(text=text),
            "stream": False,
            "options": {"temperature": 0, "num_predict": 512},
        }).encode("utf-8")
        req = urllib.request.Request(f"{host}/api/generate", body, {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read())["response"].strip()

    return (want, call)


PROVIDER_FACTORIES = [gemini_provider, ollama_provider]


def load_done():
    """Pairs (doc_id, model) already done, so an interrupted run can resume."""
    done = {}
    if OUT_JSONL.exists():
        for line in OUT_JSONL.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                done[(rec["doc_id"], rec["model"])] = rec
    return done


def write_md(docs, done):
    out = ["# Outputs — score.py reads these, but they are worth reading yourself too\n"]
    for d in docs:
        out.append(f"\n## {d['id']}\n\n**Input (with errors):**\n\n> " + d["text"].replace("\n", "\n> ") + "\n")
        known = "; ".join(
            "control: no errors" if e["class"] == 0
            else f"cl.{e['class']}: {e['wrong']}→{e['right']}" + (f" ({e['reason']})" if e["reason"] else "")
            for e in d["errors"]
        )
        out.append(f"\n**Known errors:** {known or '—'}\n")
        for (doc_id, model), rec in done.items():
            if doc_id == d["id"]:
                out.append(f"\n**{model}:**\n\n> " + rec["output"].replace("\n", "\n> ") + "\n")
    OUT_MD.write_text("".join(out), encoding="utf-8")


def main():
    args = sys.argv[1:]
    docs = parse_inputs()
    if "--check" in args:
        check(docs)
        return
    if not docs:
        sys.exit("inputs.txt is empty. Do stage 1 first (RUNBOOK.md).")

    only = args[args.index("--only") + 1] if "--only" in args else None

    providers = []
    for factory in PROVIDER_FACTORIES:
        try:
            name, call = factory()
        except Exception as e:
            print(f"[skip] {factory.__name__}: {e}")
            continue
        if only and only not in name:
            continue
        providers.append((name, call))
    if not providers:
        sys.exit("No models available. Needs GEMINI_API_KEY and/or a running Ollama.")

    print(f"Models: {[n for n, _ in providers]}; documents: {len(docs)}")
    done = load_done()
    with open(OUT_JSONL, "a", encoding="utf-8") as fh:
        for d in docs:
            for name, call in providers:
                if (d["id"], name) in done:
                    continue
                try:
                    out = call(d["text"])
                except Exception as e:
                    out = f"[ERROR: {e}]"
                rec = {"doc_id": d["id"], "model": name, "output": out}
                done[(d["id"], name)] = rec
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
                fh.flush()
                print(f"  {d['id']} × {name} ✓")

    write_md(docs, done)
    print(f"\nDone: {OUT_JSONL.name}, {OUT_MD.name}")
    print("Next: python3 score.py  (scoring one error at a time)")


if __name__ == "__main__":
    main()
