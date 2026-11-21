#!/bin/zsh
cd /Users/mitu/Desktop/work/projects/logos
uv run python tools/kiem_tra.py >/dev/null 2>&1 || { uv run python tools/kiem_tra.py | grep "✗"; echo "FAIL kiem_tra"; exit 1; }
uv run properdocs build --strict -f mkdocs.yml >"${TMPDIR:-/tmp}/logos-build.log" 2>&1 || { echo "FAIL build"; tail -20 "${TMPDIR:-/tmp}/logos-build.log"; exit 1; }
uv run python -m unittest discover -s tests 2>&1 | grep -E "^(Ran|OK|FAILED)"
npm test 2>&1 | grep -E "ℹ (pass|fail)"
