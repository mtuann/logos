"""Ngân hàng câu hỏi trắc nghiệm (docs/assets/data/quiz-bank.json).

Quét mọi trang docs/**/*.md, trích JSON của
<div class="oz-quiz" data-id="..." data-skill="..."><script type="application/json">[...]</script></div>,
kiểm tra định dạng giống hệt validate() trong docs/assets/js/quiz.js, rồi ghi
thành một file JSON duy nhất cho trang Ôn tập thông minh (docs/luyen-tap/on-tap.md).

Bỏ qua docs/them/sach.md: trang sách in chứa lại toàn bộ quiz (data-id trùng).

    python tools/quiz_bank.py          # ghi lại file dữ liệu
    python tools/quiz_bank.py --check  # báo lỗi (mã thoát 1) nếu file lệch
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "docs" / "assets" / "data" / "quiz-bank.json"

# Trang sinh tự động chứa quiz trùng — không quét.
SKIP = {"them/sach.md"}

DIV_RE = re.compile(r'<div\b[^>]*\bclass="[^"]*\boz-quiz\b[^"]*"[^>]*>', re.S)
SCRIPT_RE = re.compile(r'<script\s+type="application/json"\s*>(.*?)</script>', re.S)
ATTR_RE = re.compile(r'\b(data-id|data-skill)="([^"]*)"')


def validate(questions: list) -> str | None:
    """Gương của validate() trong docs/assets/js/quiz.js."""
    if not isinstance(questions, list) or not questions:
        return "Quiz rỗng"
    for i, q in enumerate(questions):
        if (
            not isinstance(q, dict)
            or not isinstance(q.get("q"), str)
            or not isinstance(q.get("options"), list)
            or len(q["options"]) < 2
        ):
            return f"Câu {i + 1} thiếu nội dung"
        ans = q.get("answer")
        if isinstance(ans, bool) or not isinstance(ans, int) or not (0 <= ans < len(q["options"])):
            return f"Câu {i + 1} có đáp án ngoài phạm vi"
        if not isinstance(q.get("explain"), str) or not q["explain"]:
            return f"Câu {i + 1} thiếu giải thích"
    return None


def collect() -> tuple[list[dict], list[str]]:
    """Trả về (danh sách câu hỏi, danh sách lỗi)."""
    items, errors = [], []
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if rel in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        for div in DIV_RE.finditer(text):
            tag = div.group(0)
            attrs = dict(ATTR_RE.findall(tag))
            qid = attrs.get("data-id", "quiz")
            skill = attrs.get("data-skill", "general")
            m = SCRIPT_RE.search(text, div.end(), text.find("</div>", div.end()))
            line = text.count("\n", 0, div.start()) + 1
            if not m:
                errors.append(f"{rel}:{line}: thiếu <script type=\"application/json\">")
                continue
            try:
                questions = json.loads(m.group(1))
            except json.JSONDecodeError as e:
                errors.append(f"{rel}:{line}: JSON lỗi: {e}")
                continue
            err = validate(questions)
            if err:
                errors.append(f"{rel}:{line} (data-id={qid}): {err}")
                continue
            for i, q in enumerate(questions):
                items.append(
                    {
                        "qid": qid,
                        "qindex": i,
                        "skill": skill,
                        "article": rel,
                        "q": q["q"],
                        "options": q["options"],
                        "answer": q["answer"],
                        "explain": q["explain"],
                    }
                )
    items.sort(key=lambda it: (it["article"], it["qid"], it["qindex"]))
    return items, errors


def render(items: list[dict]) -> str:
    data = {"version": 1, "generated_by": "tools/quiz_bank.py", "items": items}
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n"


def main(argv: list[str]) -> int:
    items, errors = collect()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    new = render(items)
    if "--check" in argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if new != current:
            print("quiz-bank.json lệch so với quiz trong docs — chạy: python tools/quiz_bank.py", file=sys.stderr)
            return 1
        print(f"Ngân hàng câu hỏi khớp dữ liệu ({len(items)} câu).")
        return 0
    OUT.write_text(new, encoding="utf-8")
    print(f"Đã ghi {OUT.relative_to(ROOT)} ({len(items)} câu).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
