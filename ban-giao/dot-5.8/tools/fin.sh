#!/bin/zsh
# fin.sh "<commit msg>" : sinh lại, chạy bộ kiểm tra, commit, merge --no-ff
set -u
cd /Users/mitu/Desktop/work/projects/logos
B=$(git branch --show-current)
for t in verification_page philosophers book quiz_bank works_page; do uv run python tools/$t.py >/dev/null || { echo "gen $t fail"; exit 1; }; done
uv run python tools/lint_lien_ket.py --write -q >/dev/null; uv run python tools/lint_terms.py --write -q >/dev/null
out=$(zsh /Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/tools/run_all.sh 2>&1) || true
echo "$out" | grep -E "FAIL|Ran|^OK|fail|lint_" 
if echo "$out" | grep -qE "FAIL|ℹ fail [1-9]" || ! echo "$out" | grep -q "^OK"; then echo "ĐỎ — không commit"; exit 1; fi
git add -A && git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git checkout -q main && git merge -q --no-ff "$B" -m "Merge $B" && echo "merged $B"
