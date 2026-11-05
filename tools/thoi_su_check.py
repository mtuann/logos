"""Kiểm khối thời sự data/thoi-su/*.md (ban-giao/dot-3.md việc 3.1).

    python tools/thoi_su_check.py --check   # CI: mã thoát 1 khi có lỗi
    python tools/thoi_su_check.py           # như trên, in thêm danh sách khối

Kiểm:
  - front matter theo schema/thoi-su.schema.json; `review_by` không trước `updated_to`;
  - id (tên file) dạng `<trang, "/" thành ".">.<tên ngắn>`, khớp `page`;
  - thân khối không rỗng, không có dòng trống ở đầu hay cuối;
  - mỗi khối được trang `page` dùng đúng một lần (`[[thoi-su:<id>]]` ngoài code), và không trang nào khác dùng;
  - mọi shortcode thời sự trong docs/ trỏ tới một khối có thật;
  - khối nhiều dòng: shortcode đứng riêng một dòng (hook kb.py cũng chặn khi build).
Khối quá hạn rà soát do tools/lint_volatile.py báo (luật `thoi-su-qua-han`), không phải lỗi ở đây.
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import jsonschema

from lz import DOCS, ROOT

sys.path.insert(0, str(ROOT / "hooks"))
import kb  # noqa: E402

SCHEMA = ROOT / "schema" / "thoi-su.schema.json"


def uses(docs: Path = DOCS) -> dict[str, list[tuple[str, bool]]]:
    """id → [(trang, shortcode đứng riêng một dòng)] cho mọi [[thoi-su:…]] ngoài code trong docs/."""
    out: dict[str, list[tuple[str, bool]]] = {}
    for f in sorted(docs.rglob("*.md")):
        rel = f.relative_to(docs).as_posix()
        text = f.read_text(encoding="utf-8")
        if "[[thoi-su:" not in text:
            continue

        def scan(chunk: str) -> str:
            for m in kb.THOI_SU.finditer(chunk):
                ls = chunk.rfind("\n", 0, m.start()) + 1
                le = chunk.find("\n", m.end())
                alone = not chunk[ls:m.start()].strip() and not chunk[m.end():(len(chunk) if le < 0 else le)].strip()
                out.setdefault(m.group(1), []).append((rel, alone))
            return chunk
        kb._outside_code(text, scan)
    return out


def problems(root: Path = ROOT, docs: Path = DOCS) -> list[str]:
    errs = []
    try:
        blocks = kb.load_thoi_su(root)
    except kb.PluginError as e:
        return [str(e)]
    validator = jsonschema.Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
    used = uses(docs)
    for key, b in blocks.items():
        where = f"data/thoi-su/{key}.md"
        meta = {k: (v.isoformat() if isinstance(v, datetime.date) else v) for k, v in b["meta"].items()}
        errs += [f"{where}: {'/'.join(map(str, e.path)) or '(gốc)'}: {e.message}" for e in validator.iter_errors(meta)]
        page = meta.get("page")
        if not isinstance(page, str):
            continue
        prefix = page[:-3].replace("/", ".") + "."
        if not key.startswith(prefix) or not re.fullmatch(r"[a-z0-9-]+", key[len(prefix):]):
            errs.append(f"{where}: id phải dạng {prefix}<tên-ngắn>")
        if not (docs / page).is_file():
            errs.append(f"{where}: trang {page} không có trong docs/")
        body = b["body"]
        if not body.strip():
            errs.append(f"{where}: thân khối rỗng")
        elif body != body.strip("\n") or body.startswith(" "):
            errs.append(f"{where}: thân khối có dòng trống hoặc thụt lề ở đầu/cuối")
        if str(meta.get("review_by", "")) < str(meta.get("updated_to", "")):
            errs.append(f"{where}: review_by trước updated_to")
        hits = used.get(key, [])
        pages = [p for p, _ in hits]
        if pages.count(page) != 1:
            errs.append(f"{where}: trang {page} dùng khối {pages.count(page)} lần (phải đúng 1)")
        for other in sorted(set(pages) - {page}):
            errs.append(f"{other}: dùng khối {key} của trang {page}")
        if "\n" in body and any(not alone for _, alone in hits):
            errs.append(f"{where}: khối nhiều dòng, shortcode phải đứng riêng một dòng")
    for key in sorted(set(used) - set(blocks)):
        errs += [f"{p}: [[thoi-su:{key}]] không có khối data/thoi-su/{key}.md" for p, _ in used[key]]
    return errs


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="chỉ báo lỗi (CI)")
    args = ap.parse_args(argv)
    errs = problems()
    for e in errs:
        print(e, file=sys.stderr)
    if errs:
        print(f"Khối thời sự: {len(errs)} lỗi.", file=sys.stderr)
        return 1
    blocks = kb.load_thoi_su(ROOT)
    if not args.check:
        for key, b in blocks.items():
            print(f"{key}: {b['meta']['page']} · đúng tới {b['meta']['updated_to']} · rà trước {b['meta']['review_by']}")
    print(f"Khối thời sự hợp lệ ({len(blocks)} khối).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
