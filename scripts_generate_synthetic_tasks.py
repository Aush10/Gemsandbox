#!/usr/bin/env python3
"""Combine DB and sheet generators into a task JSONL for training/eval."""
import json, os, argparse
from pathlib import Path

def combine(sql_tasks_dir, sheet_tasks_dir, out="data/tasks.jsonl"):
    tasks=[]
    for p in Path(sql_tasks_dir).glob("tasks.json"):
        tasks.extend(json.load(open(p)))
    for p in Path(sheet_tasks_dir).glob("tasks.json"):
        tasks.extend(json.load(open(p)))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out,"w") as f:
        for t in tasks:
            f.write(json.dumps(t)+"\n")
    print("Wrote", out)

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--sql", default="data/sqlite")
    p.add_argument("--sheets", default="data/sheets")
    p.add_argument("--out", default="data/tasks.jsonl")
    args=p.parse_args()
    combine(args.sql, args.sheets, args.out)