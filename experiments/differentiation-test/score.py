"""
PROTOTYPE — throwaway. Scoring the outputs + computing the verdict.

  python3 score.py            # interactive: one error at a time, press f/m/b
  python3 score.py --report   # recall table per class × model + verdict

You can stop at any time (q): scores are saved, and the next run continues
from where it stopped.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

from run import HERE, OUT_JSONL, load_done, parse_inputs

SCORES = HERE / "scores.csv"
HEADER = ["doc_id", "error_index", "error_class", "model", "verdict", "comment"]

CLASS_NAMES = {
    0: "control (no errors)",
    1: "орфографиялық қателер",
    2: "үндестік қатесі",
    3: "септік/тәуелдік жалғауы",
    4: "калька",
    5: "ресми регистр",
    6: "реквизиттердің жоқтығы",
    7: "сөзбе-сөз аудару",
}

# Gate thresholds. Fixed IN ADVANCE (README): do not touch them after seeing results.
NICHE_MAX_RECALL = 0.40   # recall ≤ this for all models → niche proven
STRONG_MIN_RECALL = 0.85  # recall ≥ this for all → models cope, round 2 needed


def load_scores():
    rows = []
    if SCORES.exists():
        with open(SCORES, encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(l for l in fh if not l.startswith("#")):
                if row.get("doc_id"):
                    rows.append(row)
    return rows


def append_score(row):
    new = not SCORES.exists() or SCORES.stat().st_size == 0
    with open(SCORES, "a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=HEADER)
        if new:
            w.writeheader()
        w.writerow(row)


def pending(docs, outputs, scored):
    """All (document × error × model) pairs that are not scored yet."""
    have = {(r["doc_id"], r["error_index"], r["model"]) for r in scored}
    items = []
    for d in docs:
        for i, err in enumerate(d["errors"]):
            for (doc_id, model), rec in outputs.items():
                if doc_id != d["id"]:
                    continue
                if (d["id"], str(i), model) in have:
                    continue
                items.append((d, i, err, model, rec["output"]))
    return items


def ask(doc, idx, err, model, output, n, total):
    print("\n" + "=" * 70)
    print(f"[{n}/{total}]  {doc['id']}  ×  {model}")
    print("=" * 70)
    print(f"\nINPUT:\n  " + doc["text"].replace("\n", "\n  "))
    if err["class"] == 0:
        print(f"\nTHIS IS A CONTROL TEXT: no errors. Question: did the model leave it intact?")
    else:
        print(f"\nERROR cl.{err['class']} ({CLASS_NAMES.get(err['class'], '?')}):")
        print(f"  wrong: {err['wrong']}")
        print(f"  right: {err['right'] or '(?)'}")
        if err.get("reason"):
            print(f"  why:   {err['reason']}")
    print(f"\nMODEL OUTPUT:\n  " + output.replace("\n", "\n  "))

    if err["class"] != 0 and err["wrong"] and err["wrong"] in output:
        print(f"\n  hint: the fragment «{err['wrong']}» is still in the output, looks like missed")

    if err["class"] == 0:
        prompt = "\n[k] left intact (ok)  [b] made an unnecessary edit  [s] skip  [q] quit> "
        allowed = {"k": "ok", "b": "broke"}
    else:
        prompt = "\n[f] fixed  [m] left as is  [b] broke/fixed wrongly  [s] skip  [q] quit> "
        allowed = {"f": "fixed", "m": "missed", "b": "broke"}

    while True:
        ans = input(prompt).strip().lower()
        if ans in ("q", "й"):  # й/ы: the same keys on a Russian layout
            return None
        if ans in ("s", "ы"):
            return "skip"
        if ans in allowed:
            comment = input("comment (Enter to skip)> ").strip()
            return {
                "doc_id": doc["id"],
                "error_index": str(idx),
                "error_class": str(err["class"]),
                "model": model,
                "verdict": allowed[ans],
                "comment": comment,
            }
        print("  not understood, press f/m/b/s/q")


def interactive():
    docs = parse_inputs()
    outputs = load_done()
    if not outputs:
        sys.exit(f"{OUT_JSONL.name} is empty. Run python3 run.py first")
    scored = load_scores()
    items = pending(docs, outputs, scored)
    if not items:
        print("Everything is scored. Next: python3 score.py --report")
        return
    print(f"Left to score: {len(items)}. You can stop at any time (q).")
    for n, (doc, idx, err, model, output) in enumerate(items, 1):
        row = ask(doc, idx, err, model, output, n, len(items))
        if row is None:
            print(f"\nSaved. Left: {len(items) - n + 1}. Run again to continue.")
            return
        if row == "skip":
            continue
        append_score(row)
    print("\nDone. Next: python3 score.py --report")


def report():
    scored = [r for r in load_scores() if r["error_class"] != "0"]
    controls = [r for r in load_scores() if r["error_class"] == "0"]
    if not scored:
        sys.exit("scores.csv is empty. Run python3 score.py first")

    models = sorted({r["model"] for r in scored})
    classes = sorted({int(r["error_class"]) for r in scored})
    cell = defaultdict(lambda: defaultdict(int))
    for r in scored:
        cell[(int(r["error_class"]), r["model"])][r["verdict"]] += 1

    w = max(max(len(m) for m in models) + 2, 12)
    print("\nRECALL PER CLASS (fixed / total)\n")
    print("class".ljust(30) + "".join(m.ljust(w) for m in models))
    for c in classes:
        line = f"{c}. {CLASS_NAMES.get(c, '?')}"[:28].ljust(30)
        for m in models:
            d = cell[(c, m)]
            tot = d["fixed"] + d["missed"] + d["broke"]
            line += (f"{d['fixed']}/{tot} ({d['fixed'] / tot:.0%})" if tot else "—").ljust(w)
        print(line)

    print("\nTOTAL\n")
    overall = {}
    for m in models:
        rows = [r for r in scored if r["model"] == m]
        fixed = sum(r["verdict"] == "fixed" for r in rows)
        broke = sum(r["verdict"] == "broke" for r in rows)
        overall[m] = fixed / len(rows) if rows else 0.0
        print(f"  {m}: recall {overall[m]:.0%} ({fixed}/{len(rows)}), broke {broke}")
    if controls:
        bad = sum(r["verdict"] == "broke" for r in controls)
        print(f"  control texts: unnecessary edits {bad}/{len(controls)}")

    print("\nGATE VERDICT (thresholds fixed in advance, README)\n")
    weak = [m for m, v in overall.items() if v <= NICHE_MAX_RECALL]
    strong = [m for m, v in overall.items() if v >= STRONG_MIN_RECALL]
    dead_classes = [
        c for c in classes
        if all((lambda d: d["fixed"] == 0 and (d["missed"] + d["broke"]) >= 2)(cell[(c, m)]) for m in models)
    ]
    # README: recall ≤ threshold for ALL models, or a class no model fixes.
    all_weak = len(weak) == len(models)
    if all_weak or dead_classes:
        print("  → THERE IS A NICHE. Gate passed, the product can be built.")
        if all_weak:
            print(f"     low recall for all models: {', '.join(weak)}")
        if dead_classes:
            print(f"     classes no model fixes: {dead_classes}")
    elif len(strong) == len(models):
        print("  → Models cope on this sample. Gate NOT passed on 10 texts:")
        print("     round 2 is needed (see README); the project cannot be killed on this sample.")
    else:
        print("  → In between: there is a signal, but not a decisive one. Round 2 (see README).")
        if weak:
            print(f"     low recall only for some models: {', '.join(weak)}")


if __name__ == "__main__":
    report() if "--report" in sys.argv else interactive()
