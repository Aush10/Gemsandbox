#!/usr/bin/env bash
# Usage: run_js.sh candidatescript.js input.csv output.json
CAND=$1
IN=$2
OUT=$3
# Use node and vm2; the script should export a function run(inputPath, outputPath)
node -e "
const { NodeVM } = require('vm2');
const fs = require('fs');
const vm = new NodeVM({ timeout: 2000, sandbox: {} });
const code = fs.readFileSync('$CAND', 'utf8');
const fnModule = vm.run(code, 'candidate.js');
(async () => {
  try {
    await fnModule.run('$IN','$OUT');
  } catch (e) {
    fs.writeFileSync('$OUT', JSON.stringify({error: String(e)}));
  }
})();
"