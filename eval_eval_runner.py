#!/usr/bin/env python3
"""Run evaluation: given tasks JSON and candidate outputs, execute and compare to gold."""

import json, sys, os, argparse, subprocess
from pathlib import Path
import sqlite3, pandas as pd

def run_sql_task(task, candidate_sql, tmp_out="tmp/result.json"):
    db = task['db']
    subprocess.run(["bash","sandbox/run_sql.sh", db, candidate_sql, tmp_out])
    out = json.load(open(tmp_out))
    return out

def compare_sql_result(gold_sql, gold_db, candidate_out):
    # Simplest: execute gold_sql and compare JSON rows
    conn=sqlite3.connect(gold_db)
    cur=conn.cursor()
    cur.execute(gold_sql)
    gold_rows = cur.fetchall()
    # convert candidate_out rows to tuples
    if isinstance(candidate_out, dict) and 'error' in candidate_out:
        return False, {"error": candidate_out['error']}
    # assuming list-of-dicts
    cand_rows = [tuple(d.values()) for d in candidate_out]
    ok = (cand_rows == gold_rows)
    return ok, {"gold":len(gold_rows), "cand":len(cand_rows)}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--tasks", required=True)
    p.add_argument("--candidates-dir", required=True)
    args=p.parse_args()
    tasks = json.load(open(args.tasks))
    results=[]
    for t in tasks:
        nl = t.get('nl')
        if 'gold_sql' in t:
            cand_path = Path(args.candidates_dir)/ (nl.replace(" ", "_") + ".sql")
            if not cand_path.exists():
                print("No candidate for", nl); continue
            cand_sql = open(cand_path).read()
            out = run_sql_task(t, cand_sql)
            ok, meta = compare_sql_result(t['gold_sql'], t['db'], out)
            results.append({"nl":nl,"ok":ok,"meta":meta})
    print(json.dumps(results, indent=2))

if __name__=="__main__":
    main()