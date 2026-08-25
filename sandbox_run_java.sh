#!/usr/bin/env bash
# Usage: run_java.sh Candidate.java input.json output.json
JAVA_FILE=$1
IN=$2
OUT=$3
javac "$JAVA_FILE" 2> /tmp/java_err.txt
if [ $? -ne 0 ]; then
  jq -n --arg err "$(cat /tmp/java_err.txt)" '{"error":$err}' > "$OUT"
  exit 0
fi
MAIN_CLASS=$(basename "$JAVA_FILE" .java)
java -cp . "$MAIN_CLASS" "$IN" "$OUT" 2> /tmp/java_run_err.txt
if [ $? -ne 0 ]; then
  jq -n --arg err "$(cat /tmp/java_run_err.txt)" '{"error":$err}' > "$OUT"
fi