#!/usr/bin/env python3
"""Generate CSV sheets and transformations (gold) — we represent gold as small pandas scripts."""

import os, json, argparse, random
import pandas as pd
from datetime import datetime, timedelta

TRANSFORM_TEMPLATES = [
    ("monthly_revenue","groupby date month -> sum amount",
     "def transform(df):\n    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')\n    out = df.groupby('month', as_index=False)['amount'].sum().rename(columns={'amount':'monthly_amount'})\n    return out"),
    ("remove_duplicates_and_total","drop duplicates on id then sum amount",
     "def transform(df):\n    df2 = df.drop_duplicates(subset=['id'])\n    return pd.DataFrame({'total': [df2['amount'].sum()]})")
]

def make_sheets(outdir, n=10):
    os.makedirs(outdir, exist_ok=True)
    tasks=[]
    for i in range(n):
        df = pd.DataFrame({
            'id': range(1,51),
            'date': [(datetime(2023,1,1)+timedelta(days=random.randint(0,365))).strftime('%Y-%m-%d') for _ in range(50)],
            'region': [random.choice(['north','south','east','west']) for _ in range(50)],
            'amount': [round(random.random()*1000,2) for _ in range(50)]
        })
        fname=f"sheet_{i}.csv"
        df.to_csv(os.path.join(outdir,fname), index=False)
        tpl = random.choice(TRANSFORM_TEMPLATES)
        tasks.append({"sheet":os.path.join(outdir,fname),"nl":tpl[0],"gold_transform":tpl[2]})
    open(os.path.join(outdir,"tasks.json"),"w").write(json.dumps(tasks, indent=2))
    print("Wrote", outdir, "with tasks.json")

if __name__=="__main__":
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--out", default="data/sheets")
    p.add_argument("--n", type=int, default=20)
    args=p.parse_args()
    make_sheets(args.out, n=args.n)