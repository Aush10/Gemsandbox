# genai-sandbox (text→SQL / spreadsheet / code evaluation harness)

Small repo to help bootstrap a generative-AI evaluation & sandbox for SQL, spreadsheet transformations, JS, and Java snippets.

Features
- Docker sandbox running SQLite, Node (vm2), OpenJDK and Python for executing/running generated candidates safely.
- Synthetic task generators producing (NL intent → gold SQL / transformation script) pairs for training or evaluation.
- Evaluation harness that runs model outputs, captures errors, and measures execution accuracy.
- Prompt templates that inject schema, sample rows, and ask for multiple candidates for reranking.

Quickstart (local)
1. Build image:
   docker build -t genai-sandbox .
2. Generate data:
   python3 scripts/generate_sqlite_db.py --out data/sqlite --n_schemas 5
   python3 scripts/generate_spreadsheets.py --out data/sheets --n 20
3. Start sandbox (optional services):
   docker-compose up -d
4. Run evaluation demo:
   python3 eval/eval_runner.py --tasks examples/sample_task.json --candidates-dir examples/candidates

If you want this pushed to a GitHub repo, give me the repo owner/name and I will create files there.