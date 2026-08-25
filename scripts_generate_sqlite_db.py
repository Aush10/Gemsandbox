#!/usr/bin/env python3
"""Create random sqlite DBs and paired NL->SQL tasks (gold queries + results)."""

import sqlite3, json, os, random, argparse
import pandas as pd

TABLE_TEMPLATES = [
    {"name":"sales","cols":[("id","INTEGER PRIMARY KEY"),("date","TEXT"),("region","TEXT"),("amount","REAL")]},
    {"name":"users","cols":[("id","INTEGER PRIMARY KEY"),("name","TEXT"),("signup","TEXT"),("revenue","REAL")]},
    {"name":"orders","cols":[("id","INTEGER PRIMARY KEY"),("user_id","INTEGER"),("total","REAL"),("status","TEXT")]}
]

NL_TEMPLATES = [
    ("total revenue by region for 2023","SELECT region, SUM(amount) as total FROM sales WHERE date LIKE '2023-%' GROUP BY region"),
    ("count of users who signed up in 2022","SELECT COUNT(*) FROM users WHERE signup LIKE '2022-%'"),
    ("average order total for completed orders","SELECT AVG(total) FROM orders WHERE status='completed'")
]

def make_db(outdir, dbname="snapshot.db", seed=0):
    random.seed(seed)
    path = os.path.join(outdir, dbname)
    os.makedirs(outdir, exist_ok=True)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    # pick template and populate
    for t in TABLE_TEMPLATES:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {t['name']} ({', '.join([' '.join(c) for c in t['cols']])})")
        # insert rows
        for i in range(200):
            if t['name']=="sales":
                cur.execute("INSERT INTO sales (date,region,amount) VALUES (?,?,?)",
                            (f"2023-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                             random.choice(["north","south","east","west"]),
                             round(random.random()*1000,2)))
            elif t['name']=="users":
                cur.execute("INSERT INTO users (name,signup,revenue) VALUES (?,?,?)",
                             (f"user{random.randint(1,1000)}",
                              f"2022-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
                              round(random.random()*500,2)))
            elif t['name']=="orders":
                cur.execute("INSERT INTO orders (user_id,total,status) VALUES (?,?,?)",
                             (random.randint(1,100), round(random.random()*200,2), random.choice(["completed","cancelled","pending"])))
    conn.commit()
    conn.close()
    # create tasks
    tasks = []
    for nl, sql in NL_TEMPLATES:
        tasks.append({"nl":nl,"gold_sql":sql,"db":path})
    open(os.path.join(outdir,"tasks.json"),"w").write(json.dumps(tasks, indent=2))
    print("Wrote", path, "and tasks.json")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--out", default="data/sqlite")
    p.add_argument("--seed", type=int, default=0)
    args = p.parse_args()
    make_db(args.out, seed=args.seed)