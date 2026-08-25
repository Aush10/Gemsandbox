#!/usr/bin/env bash
# Usage: run_sql.sh /path/to/db "candidate_sql" results.json
DB=$1
SQL="$2"
OUT=$3
sqlite3 -header -json "$DB" "$SQL" > "$OUT" 2> /tmp/sql_err.txt
STATUS=$?
if [ $STATUS -ne 0 ]; then
  echo "{\"error\": \"$(cat /tmp/sql_err.txt | sed 's/\"/\\\"/g')\"}" > "$OUT"
fi