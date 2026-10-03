#!/usr/bin/env python3
"""Harvest completed agent results out of a running workflow's journal.

A workflow only returns its payload when the whole run finishes. When a run is
long — the extraction workflow here queues 14 sources behind a 2-agent
concurrency cap — its already-completed agents are finished work sitting idle,
and the dataset silently under-reports until the last one lands.

This reads `journal.jsonl` and emits every completed extraction as a lane file
that merge_lane_files.py can consume immediately. Re-running it later is safe:
assemble_thrombo.py deduplicates measurements on their natural key, so
harvesting the same agent twice does not double-count.

It also means a workflow that dies partway through does not lose the agents that
already succeeded, which is the same reason extraction agents write files rather
than returning one large response.

Usage:  python3 scripts/harvest_workflow.py <journal.jsonl> [out.json]
"""
import json, sys


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    journal = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "workflow_harvest.json"

    lanes, n_fail, seen = [], 0, 0
    verdicts = []
    with open(journal, encoding="utf-8", errors="replace") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            t = d.get("type")
            if t in ("failed", "error"):
                n_fail += 1
                continue
            if t != "result":
                continue
            r = d.get("result")
            if not isinstance(r, dict):
                continue
            seen += 1
            # a verification agent returns verdicts, not rows
            if r.get("verdicts") and not r.get("measurements"):
                verdicts.extend(r["verdicts"])
                continue
            if not (r.get("measurements") or r.get("oligos")):
                continue
            refs = {m.get("source_ref", "?") for m in (r.get("measurements") or [])}
            label = sorted(refs)[0][:44] if refs else f"agent{seen}"
            lanes.append({
                "lane": f"workflow:{label}",
                "oligos": r.get("oligos") or [],
                "measurements": r.get("measurements") or [],
                "verified": None,
            })

    # attach any verification verdicts to every harvested lane; assemble_thrombo
    # matches them by (oligo_name, readout_name), so lane assignment is immaterial
    if verdicts and lanes:
        lanes[0]["verified"] = {"verdicts": verdicts}

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"lanes": lanes}, f)

    tot_m = sum(len(l["measurements"]) for l in lanes)
    tot_o = sum(len(l["oligos"]) for l in lanes)
    for l in lanes:
        print(f"  {l['lane']:<56} oligos={len(l['oligos']):>3} "
              f"measurements={len(l['measurements']):>4}")
    print(f"\nharvested {len(lanes)} completed extraction(s): "
          f"{tot_o} oligo entries, {tot_m} measurements, {len(verdicts)} verdicts")
    if n_fail:
        print(f"NOTE: {n_fail} agent(s) recorded as failed in this journal — their "
              f"sources are NOT represented here and need re-running.")


if __name__ == "__main__":
    main()
