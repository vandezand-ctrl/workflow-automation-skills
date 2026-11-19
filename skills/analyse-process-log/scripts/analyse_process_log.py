#!/usr/bin/env python3
"""Analyse an event log exported from a ticketing, CRM or ERP system.

Input: a CSV with one row per event: a case id, an activity name and a timestamp.
Output: a Markdown report with throughput times, waits per step, the slowest
handoffs, rework and the most common paths.

Standard library only. Example:
    python analyse_process_log.py process-log.csv --out process-log-analysis.md
"""
import argparse
import csv
import statistics
from collections import Counter, defaultdict
from datetime import datetime

FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M", "%Y-%m-%d")


def parse_time(value):
    value = value.strip()
    for fmt in FORMATS:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    raise ValueError(f"Unrecognised timestamp: {value!r}")


def hours(delta):
    return delta.total_seconds() / 3600


def fmt_hours(h):
    if h is None:
        return "n/a"
    return f"{h / 24:.1f} days" if h >= 48 else f"{h:.1f} h"


def pct(values, q):
    if not values:
        return None
    values = sorted(values)
    k = (len(values) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(values) - 1)
    return values[lo] + (values[hi] - values[lo]) * (k - lo)


def load(path, case_col, act_col, ts_col):
    cases = defaultdict(list)
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = {case_col, act_col, ts_col} - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Missing columns: {', '.join(sorted(missing))}. Found: {reader.fieldnames}")
        for row in reader:
            cases[row[case_col].strip()].append((parse_time(row[ts_col]), row[act_col].strip()))
    for events in cases.values():
        events.sort()
    return cases


def analyse(cases, top):
    n_events = sum(len(e) for e in cases.values())
    starts = [e[0][0] for e in cases.values()]
    ends = [e[-1][0] for e in cases.values()]
    throughput = [hours(e[-1][0] - e[0][0]) for e in cases.values()]

    waits = defaultdict(list)          # wait before each activity
    transitions = defaultdict(list)    # (from, to) -> waits
    activity_count = Counter()
    cases_with = defaultdict(set)
    rework_cases = defaultdict(set)
    variants = Counter()

    for cid, events in cases.items():
        seen = Counter()
        path = []
        for i, (ts, act) in enumerate(events):
            activity_count[act] += 1
            cases_with[act].add(cid)
            seen[act] += 1
            if seen[act] > 1:
                rework_cases[act].add(cid)
            if not path or path[-1] != act:
                path.append(act)
            if i > 0:
                prev_ts, prev_act = events[i - 1]
                w = hours(ts - prev_ts)
                waits[act].append(w)
                transitions[(prev_act, act)].append(w)
        variants[" > ".join(path)] += 1

    n = len(cases)
    out = []
    out.append("# Process log analysis\n")
    out.append(f"- Cases: {n}")
    out.append(f"- Events: {n_events}")
    out.append(f"- Period: {min(starts):%Y-%m-%d} to {max(ends):%Y-%m-%d}")
    out.append(f"- Throughput time per case: median {fmt_hours(statistics.median(throughput))}, "
               f"90th percentile {fmt_hours(pct(throughput, 0.9))}\n")

    out.append("## Steps\n")
    out.append("| Activity | Events | Cases | Share of cases | Median wait before | 90th percentile wait |")
    out.append("|---|---:|---:|---:|---:|---:|")
    order = sorted(activity_count, key=lambda a: -len(cases_with[a]))
    for a in order:
        w = waits.get(a)
        out.append(f"| {a} | {activity_count[a]} | {len(cases_with[a])} | {len(cases_with[a]) / n:.0%} | "
                   f"{fmt_hours(statistics.median(w)) if w else 'start'} | {fmt_hours(pct(w, 0.9)) if w else ''} |")

    out.append("\n## Slowest handoffs\n")
    out.append("Transitions with at least 5 occurrences, ordered by median wait.\n")
    out.append("| From | To | Times | Median wait | Total wait |")
    out.append("|---|---|---:|---:|---:|")
    slow = [(k, v) for k, v in transitions.items() if len(v) >= 5]
    slow.sort(key=lambda kv: -statistics.median(kv[1]))
    for (a, b), v in slow[:top]:
        out.append(f"| {a} | {b} | {len(v)} | {fmt_hours(statistics.median(v))} | {fmt_hours(sum(v))} |")

    out.append("\n## Rework\n")
    if rework_cases:
        out.append("| Activity repeated within a case | Cases | Share of cases |")
        out.append("|---|---:|---:|")
        for a, cs in sorted(rework_cases.items(), key=lambda kv: -len(kv[1])):
            out.append(f"| {a} | {len(cs)} | {len(cs) / n:.0%} |")
    else:
        out.append("No activity is repeated within a case.")

    out.append("\n## Most common paths\n")
    out.append("| Path | Cases | Share |")
    out.append("|---|---:|---:|")
    for path, c in variants.most_common(top):
        out.append(f"| {path} | {c} | {c / n:.0%} |")
    out.append(f"\n{len(variants)} distinct paths in total.")
    return "\n".join(out) + "\n"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv")
    p.add_argument("--case", default="case_id", help="case id column (default case_id)")
    p.add_argument("--activity", default="activity", help="activity column (default activity)")
    p.add_argument("--timestamp", default="timestamp", help="timestamp column (default timestamp)")
    p.add_argument("--top", type=int, default=5, help="rows in the handoff and path tables")
    p.add_argument("--out", help="write the report to this file instead of printing it")
    a = p.parse_args()
    report = analyse(load(a.csv, a.case, a.activity, a.timestamp), a.top)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report written to {a.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
