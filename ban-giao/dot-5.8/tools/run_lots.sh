#!/bin/zsh
# run_lots.sh START END TAG : áp các lô START..END (chỉ số trong lots.json)
S=/Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/tools
cd /Users/mitu/Desktop/work/projects/logos
for N in $(seq $1 $2); do
  git checkout -q main && git checkout -q -b dot-5-5-8-sua-$3-$N || exit 1
  msg=$(uv run python $S/apply.py $N) || { echo "apply $N lỗi"; exit 1; }
  echo "$msg"
  uv run python $S/prune_allow.py; uv run python tools/verify.py --ghi-so 5.8 >/dev/null
  for t in kb_sources kb_works kb_events kb_quotes; do uv run python tools/$t.py >/dev/null; done
  zsh /Users/mitu/Desktop/work/projects/logos/ban-giao/dot-5.8/tools/fin.sh "Đợt 5: 5.8 sửa theo bằng chứng lượt 1 — $msg" > ${TMPDIR:-/tmp}/logos-5.8-last.out ; grep -E "ĐỎ|merged|FAIL" ${TMPDIR:-/tmp}/logos-5.8-last.out; grep -q "^merged" ${TMPDIR:-/tmp}/logos-5.8-last.out || exit 1
done
