#!/bin/zsh
cd /Users/mitu/Desktop/work/projects/logos
for t in gen_glossary figures review_check timeline influence philosophers book frontmatter_check quiz_bank terms_policy kb_sources kb_works kb_quotes kb_philpapers kb_events works_page verification_page nav_gen; do
  uv run python tools/$t.py --check >/dev/null 2>&1 || { echo "FAIL gen $t"; exit 1; }
done
for c in "content_registry.py --check" "add_heading_ids.py --check" "check_ledger.py --check" "kb_check.py --check" "thoi_su_check.py --check" "lint_volatile.py --strict -q"; do
  uv run python tools/${=c} >/dev/null 2>&1 || { echo "FAIL $c"; exit 1; }
done
for l in lint_terms lint_structure lint_facts lint_quotes lint_so_lieu lint_lien_ket; do uv run python tools/$l.py --strict -q >/dev/null 2>&1 || { echo "FAIL $l"; exit 1; }; done
uv run properdocs build --strict -f mkdocs.yml >"${TMPDIR:-/tmp}/logos-build.log" 2>&1 || { echo "FAIL build"; tail -20 "${TMPDIR:-/tmp}/logos-build.log"; exit 1; }
uv run python -m unittest discover -s tests 2>&1 | grep -E "^(Ran|OK|FAILED)"
npm test 2>&1 | grep -E "ℹ (pass|fail)"
