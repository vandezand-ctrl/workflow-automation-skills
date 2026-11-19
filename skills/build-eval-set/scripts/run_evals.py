#!/usr/bin/env python3
"""Score an AI step's outputs against an evaluation set.

Input: two CSV files with the same id column and the same field columns:
  expected.csv  the correct values, checked by a person
  actual.csv    what the AI step produced for the same cases
Output: accuracy per field, the share of cases with every field right, and a
list of every mismatch. Exits with code 1 when the case pass rate is below
--min-pass, so it can block a change in a pipeline.

Standard library only. Example:
    python run_evals.py expected.csv actual.csv --numeric total_amount --out eval-report.md --min-pass 0.9
"""
import argparse
import csv
import re
import sys


def norm(value):
    return re.sub(r"\s+", " ", (value or "").strip().lower())


def to_number(value):
    v = re.sub(r"[^\d.\-]", "", (value or "").replace(",", ""))
    return float(v) if v not in ("", "-", ".") else None


def load(path, id_col):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if rows and id_col not in rows[0]:
        raise SystemExit(f"{path}: no '{id_col}' column")
    return {r[id_col].strip(): r for r in rows}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("expected")
    p.add_argument("actual")
    p.add_argument("--id", default="id", help="id column (default id)")
    p.add_argument("--numeric", nargs="*", default=[], help="fields compared as numbers")
    p.add_argument("--tolerance", type=float, default=0.01, help="allowed absolute difference for numeric fields")
    p.add_argument("--min-pass", type=float, default=0.0, help="minimum share of fully correct cases (0 to 1)")
    p.add_argument("--out", help="write the report to this file")
    a = p.parse_args()

    expected, actual = load(a.expected, a.id), load(a.actual, a.id)
    fields = [c for c in next(iter(expected.values())).keys() if c != a.id]
    correct = {f: 0 for f in fields}
    mismatches, missing, passed = [], [], 0

    for cid, exp in expected.items():
        act = actual.get(cid)
        if act is None:
            missing.append(cid)
            continue
        ok_all = True
        for f in fields:
            e, g = exp.get(f, ""), act.get(f, "")
            if f in a.numeric:
                en, gn = to_number(e), to_number(g)
                ok = en is not None and gn is not None and abs(en - gn) <= a.tolerance
            else:
                ok = norm(e) == norm(g)
            if ok:
                correct[f] += 1
            else:
                ok_all = False
                mismatches.append((cid, f, e, g))
        passed += ok_all

    n = len(expected)
    scored = n - len(missing)
    rate = passed / n if n else 0
    out = ["# Evaluation report\n",
           f"- Cases in the evaluation set: {n}",
           f"- Cases without an output: {len(missing)}" + (f" ({', '.join(missing)})" if missing else ""),
           f"- Cases with every field correct: {passed} of {n} ({rate:.0%})",
           f"- Required: {a.min_pass:.0%}. Result: {'PASS' if rate >= a.min_pass else 'FAIL'}\n",
           "## Accuracy per field\n", "| Field | Correct | Accuracy |", "|---|---:|---:|"]
    for f in fields:
        out.append(f"| {f} | {correct[f]} of {scored} | {correct[f] / scored:.0%} |" if scored else f"| {f} | 0 | n/a |")
    out += ["\n## Mismatches\n"]
    if mismatches:
        out += ["| Case | Field | Expected | Got |", "|---|---|---|---|"]
        out += [f"| {c} | {f} | {e} | {g} |" for c, f, e, g in mismatches]
    else:
        out.append("None.")
    report = "\n".join(out) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(report)
        print(f"Report written to {a.out}. Pass rate {rate:.0%}.")
    else:
        print(report)
    sys.exit(0 if rate >= a.min_pass else 1)


if __name__ == "__main__":
    main()
