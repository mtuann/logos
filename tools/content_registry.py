"""Sổ đăng ký nội dung `content.yml`: sinh lần đầu từ `nav` của mkdocs.yml, và kiểm tra.

    python tools/content_registry.py --check           # CI: mã thoát 1 khi sổ và trang lệch nhau
    python tools/content_registry.py --init            # sinh content.yml lần đầu (không ghi đè file đã có)
    python tools/content_registry.py --init --stdout   # in bản sinh ra màn hình để so, không ghi
    python tools/content_registry.py --init --force    # sinh lại, ghi đè (mất mọi chỉnh tay)
    python tools/content_registry.py --sync-frontmatter  # ghi tier, block từ content.yml vào front matter trang viết tay

Mỗi trang trong docs/ và mỗi file dữ liệu một dòng: loại (`type`/`kind`), tầng (`tier`), khối (`block`),
có sinh tự động hay không (`generated`). Danh sách giá trị cho phép đọc từ schema/content.schema.json.
Đặc tả và lý do: ban-giao/dot-0.md, KE-HOACH.md mục 4–5.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = "content.yml"
SCHEMA = Path("schema") / "content.schema.json"
MKDOCS = "mkdocs.yml"
DATA_DIR = Path("docs") / "assets" / "data"
# Thư mục mà mọi file trong đó phải có dòng trong content.yml (hoặc nằm trong một mục thư mục, đường dẫn kết thúc "/").
DATA_DIRS = [DATA_DIR, Path("data") / "kb"]

# Nhóm con của "Câu hỏi lớn" trong nav → khóa khối (KE-HOACH.md mục 5.3).
CAU_HOI_BLOCKS = {
    "Tri thức và chân lý": "tri-thuc",
    "Tâm trí, AI và cái tôi": "tam-tri",
    "Tự do và trách nhiệm": "tu-do",
    "Đạo đức học": "dao-duc",
    "Luân lý ứng dụng": "luan-ly-ung-dung",
    "Triết học chính trị": "chinh-tri",
    "Cái đẹp và nghệ thuật": "my-hoc",
    "Tôn giáo": "ton-giao",
    "Siêu hình học": "sieu-hinh",
    "Ý nghĩa cuộc sống": "y-nghia",
    "Tư tưởng Việt Nam": "viet-nam",
}
# Thư mục cấp một → (type, block) của bài không phải index.md. Bài cau-hoi lấy khối theo nhóm nav.
DIR_RULES = {
    "cau-hoi": ("cau-hoi", None),
    "cong-cu": ("cong-cu", "cong-cu"),
    "lich-su": ("lich-su", "lich-su"),
    "doc": ("doc", "van-ban"),
    "bat-dau": ("bat-dau", "bat-dau"),
    "triet-gia": ("triet-gia", "triet-gia"),
}
HE_THONG_DIRS = {"them", "luyen-tap"}
# Trang do tool trong tools/ viết ra toàn bộ (ngoài ra: mọi triet-gia/*.md, do tools/philosophers.py).
GENERATED_PAGES = {"them/sach.md", "them/tu-dien.md", "lich-su/dong-thoi-gian.md", "lich-su/so-do-anh-huong.md"}
# File dữ liệu: (đường dẫn từ gốc repo, kind, tier, block, generated). Thứ tự giữ nguyên khi sinh.
DATA_FILES = [
    ("docs/assets/data/terms.json", "thuat-ngu", "loi", "thuat-ngu", False),
    ("data/kb/people.yml", "triet-gia", "loi", "triet-gia", False),
    ("data/people/", "ho-so-triet-gia", "loi", "triet-gia", False),
    ("docs/assets/data/philosophers.json", "triet-gia", "he-thong", None, True),
    ("data/kb/sources.yml", "nguon", "loi", None, True),
    ("data/kb/works.yml", "tac-pham", "loi", None, True),
    ("data/kb/quotes.yml", "trich-dan", "loi", None, True),
    ("tools/philpapers-2020.md", "philpapers", "loi", None, False),
    ("docs/assets/data/fallacies.json", "luyen-tap", "loi", "luyen-tap", False),
    ("docs/assets/data/lap-luan.json", "luyen-tap", "loi", "luyen-tap", False),
    ("docs/assets/data/logic.json", "luyen-tap", "loi", "luyen-tap", False),
    ("docs/assets/data/thi-nghiem.json", "luyen-tap", "loi", "luyen-tap", False),
    ("docs/assets/data/quiz-bank.json", "quiz", "he-thong", None, True),
]
PAGE_FIELDS = ["path", "type", "tier", "block", "generated"]
DATA_FIELDS = ["path", "kind", "tier", "block", "generated"]
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)


# ---------------------------------------------------------------- quy tắc chung cho --init và --check

def is_he_thong(path: str) -> bool:
    """Trang chủ, mọi index.md, them/ và luyen-tap/ (KE-HOACH.md mục 5.1)."""
    return path == "index.md" or path.endswith("/index.md") or path.split("/", 1)[0] in HE_THONG_DIRS


def expected_generated(path: str) -> bool:
    return path in GENERATED_PAGES or path.startswith("triet-gia/")


def expected_type(path: str) -> str:
    if is_he_thong(path):
        return "he-thong"
    top = path.split("/", 1)[0]
    if top not in DIR_RULES:
        raise ValueError(f"{path}: thư mục chưa có quy tắc trong DIR_RULES")
    return DIR_RULES[top][0]


def schema_enums(root: Path) -> dict[str, list]:
    s = json.loads((root / SCHEMA).read_text(encoding="utf-8"))
    d = s["$defs"]
    return {
        "type": d["page"]["properties"]["type"]["enum"],
        "kind": d["data"]["properties"]["kind"]["enum"],
        "tier": d["tier"]["enum"],
        "block": [b for alt in d["block"]["oneOf"] if "enum" in alt for b in alt["enum"]],
    }


# ---------------------------------------------------------------- sinh lần đầu từ nav

def walk_nav(items, groups=()):
    """Trả về (đường dẫn, tuple tên nhóm) theo đúng thứ tự nav."""
    for item in items:
        if isinstance(item, str):
            yield item, groups
        elif isinstance(item, dict):
            for title, value in item.items():
                if isinstance(value, str):
                    yield value, groups
                else:
                    yield from walk_nav(value, groups + (title,))


def build_registry(root: Path = ROOT) -> tuple[dict, list[tuple[str, str]]]:
    """Sổ sinh từ nav, kèm danh sách (đường dẫn, tên nhóm cấp một) để in chú thích."""
    nav = yaml.safe_load((root / MKDOCS).read_text(encoding="utf-8"))["nav"]
    pages, sections = [], []
    for path, groups in walk_nav(nav):
        ptype = expected_type(path)
        if ptype == "he-thong":
            tier, block = "he-thong", None
        elif ptype == "cau-hoi":
            if len(groups) < 2 or groups[1] not in CAU_HOI_BLOCKS:
                raise ValueError(f"{path}: nhóm nav {groups!r} chưa có khóa trong CAU_HOI_BLOCKS")
            tier, block = "loi", CAU_HOI_BLOCKS[groups[1]]
        else:
            tier, block = "loi", DIR_RULES[path.split("/", 1)[0]][1]
        pages.append({"path": path, "type": ptype, "tier": tier, "block": block, "generated": expected_generated(path)})
        sections.append((path, " › ".join(groups[:2]) if groups else "Trang chủ"))
    data = [dict(zip(DATA_FIELDS, row)) for row in DATA_FILES]
    return {"version": 1, "pages": pages, "data": data}, sections


def _flow(entry: dict, fields: list[str], widths: list[int]) -> str:
    def val(v):
        return "null" if v is None else ("true" if v is True else "false" if v is False else str(v))
    cells = [f"{f}: {val(entry[f])}," for f in fields[:-1]] + [f"{fields[-1]}: {val(entry[fields[-1]])}"]
    return "{" + " ".join(c.ljust(w) for c, w in zip(cells, widths + [0])).rstrip() + "}"


def dump_registry(reg: dict, sections: list[tuple[str, str]]) -> str:
    sec = dict(sections)
    pw = [max(len(f"{f}: {e[f]},") for e in reg["pages"]) for f in PAGE_FIELDS[:-1]]
    dw = [max(len(f"{f}: {'null' if e[f] is None else e[f]},") for e in reg["data"]) for f in DATA_FIELDS[:-1]]
    out = [
        "# Sổ đăng ký nội dung của Logos. Đặc tả: ban-giao/dot-0.md; giá trị cho phép: schema/content.schema.json.",
        "# Sinh lần đầu bằng `tools/content_registry.py --init` từ nav của mkdocs.yml; từ đó chủ biên sửa tay (nhất là tier, block).",
        "# Kiểm tra: `tools/content_registry.py --check` (chạy trong CI).",
        "version: 1",
        "pages:",
    ]
    last = None
    for e in reg["pages"]:
        if sec.get(e["path"]) != last:
            last = sec.get(e["path"])
            out.append(f"  # {last}")
        out.append("  - " + _flow(e, PAGE_FIELDS, pw))
    out.append("data:")
    out += ["  - " + _flow(e, DATA_FIELDS, dw) for e in reg["data"]]
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- kiểm tra

def check(reg, root: Path = ROOT) -> list[str]:
    """Danh sách lỗi (rỗng nếu sổ khớp trang và dữ liệu)."""
    enums = schema_enums(root)
    errors: list[str] = []
    if not isinstance(reg, dict):
        return ["content.yml phải là một mapping"]
    extra = set(reg) - {"version", "pages", "data"}
    if extra:
        errors.append(f"khóa lạ ở gốc content.yml: {sorted(extra)}")
    if reg.get("version") != 1:
        errors.append("version phải là 1")
    pages, data = reg.get("pages") or [], reg.get("data") or []

    def check_entry(e, fields, label):
        if not isinstance(e, dict):
            errors.append(f"{label}: mỗi dòng phải là mapping, nhận {e!r}")
            return None
        missing, unknown = [f for f in fields if f not in e], sorted(set(e) - set(fields))
        if missing or unknown:
            errors.append(f"{label} {e.get('path')}: thiếu {missing} / thừa {unknown}")
            return None
        if e["tier"] not in enums["tier"]:
            errors.append(f"{label} {e['path']}: tier {e['tier']!r} không thuộc {enums['tier']}")
        if e["block"] is not None and e["block"] not in enums["block"]:
            errors.append(f"{label} {e['path']}: block {e['block']!r} không thuộc KE-HOACH.md mục 5.3")
        if not isinstance(e["generated"], bool):
            errors.append(f"{label} {e['path']}: generated phải là true/false")
        return e["path"]

    seen = set()
    for e in pages:
        path = check_entry(e, PAGE_FIELDS, "trang")
        if path is None:
            continue
        if path in seen:
            errors.append(f"trang {path}: đường dẫn trùng")
        seen.add(path)
        if not (root / "docs" / path).is_file():
            errors.append(f"trang {path}: không còn file docs/{path}")
            continue
        if e["type"] not in enums["type"]:
            errors.append(f"trang {path}: type {e['type']!r} không thuộc {enums['type']}")
            continue
        try:
            want = expected_type(path)
        except ValueError as ex:
            errors.append(str(ex))
            continue
        if e["type"] != want:
            errors.append(f"trang {path}: type {e['type']!r}, theo thư mục phải là {want!r}")
        if e["type"] == "he-thong":
            if e["tier"] != "he-thong" or e["block"] is not None:
                errors.append(f"trang {path}: trang he-thong phải có tier: he-thong, block: null")
        else:
            if e["tier"] == "he-thong":
                errors.append(f"trang {path}: chỉ trang he-thong mới có tier: he-thong")
            top = path.split("/", 1)[0]
            if e["type"] == "cau-hoi":
                if e["block"] not in CAU_HOI_BLOCKS.values():
                    errors.append(f"trang {path}: bài cau-hoi phải thuộc một trong 11 khối chủ đề, nhận {e['block']!r}")
            elif e["block"] != DIR_RULES[top][1]:
                errors.append(f"trang {path}: block phải là {DIR_RULES[top][1]!r}")
        if e["generated"] != expected_generated(path):
            errors.append(f"trang {path}: generated phải là {str(expected_generated(path)).lower()}")
        m = FRONT_MATTER.match((root / "docs" / path).read_text(encoding="utf-8"))
        meta = (yaml.safe_load(m.group(1)) or {}) if m else {}
        meta = meta if isinstance(meta, dict) else {}
        for f in ("tier", "block"):
            if f in meta and meta[f] != e[f]:
                errors.append(f"trang {path}: front matter {f}: {meta[f]!r} lệch content.yml ({e[f]!r})")
        # Trang viết tay phải mang tier (và block khi khác null) trong front matter (ban-giao/dot-1.md việc 1.4).
        if not e["generated"]:
            want = frontmatter_fields(e)
            lacking = [f for f in want if f not in meta]
            if lacking:
                errors.append(f"trang {path}: front matter thiếu {', '.join(lacking)} "
                              "(chạy: python tools/content_registry.py --sync-frontmatter)")
    for p in sorted((root / "docs").rglob("*.md")):
        rel = p.relative_to(root / "docs").as_posix()
        if rel not in seen:
            errors.append(f"trang {rel}: có trong docs/ nhưng thiếu trong content.yml")

    seen_data = set()
    generated_data = {row[0] for row in DATA_FILES if row[4]}
    for e in data:
        path = check_entry(e, DATA_FIELDS, "dữ liệu")
        if path is None:
            continue
        if path in seen_data:
            errors.append(f"dữ liệu {path}: đường dẫn trùng")
        seen_data.add(path)
        if path.endswith("/"):
            if not (root / path).is_dir():
                errors.append(f"dữ liệu {path}: không còn thư mục")
        elif not (root / path).is_file():
            errors.append(f"dữ liệu {path}: không còn file")
        if e["kind"] not in enums["kind"]:
            errors.append(f"dữ liệu {path}: kind {e['kind']!r} không thuộc {enums['kind']}")
        if e["generated"] != (path in generated_data):
            errors.append(f"dữ liệu {path}: generated phải là {str(path in generated_data).lower()}")
    for d in DATA_DIRS:
        if not (root / d).is_dir():
            continue
        for p in sorted((root / d).iterdir()):
            rel = p.relative_to(root).as_posix()
            if p.is_file() and rel not in seen_data:
                errors.append(f"dữ liệu {rel}: có trong {d.as_posix()}/ nhưng thiếu trong content.yml")
    return errors


def frontmatter_fields(entry: dict) -> dict:
    """Các trường tầng/khối một trang viết tay mang trong front matter: tier luôn có; block khi khác null."""
    out = {"tier": entry["tier"]}
    if entry["block"] is not None:
        out["block"] = entry["block"]
    return out


def sync_frontmatter(reg: dict, root: Path = ROOT) -> int:
    """Ghi tier, block từ sổ vào front matter của mọi trang viết tay; trả về số file đã đổi.
    Chỉ thay hoặc thêm đúng các dòng `tier:`, `block:` ở cuối front matter; các dòng khác giữ nguyên từng byte."""
    changed = 0
    for e in reg["pages"]:
        if e["generated"]:
            continue
        f = root / "docs" / e["path"]
        text = f.read_text(encoding="utf-8")
        m = FRONT_MATTER.match(text)
        if not m:
            raise ValueError(f"{e['path']}: không có front matter")
        lines = [ln for ln in m.group(1).split("\n") if not re.match(r"(tier|block):", ln)]
        lines += [f"{k}: {v}" for k, v in frontmatter_fields(e).items()]
        new = "---\n" + "\n".join(lines) + "\n---\n" + text[m.end():]
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def load_registry(root: Path = ROOT):
    return yaml.safe_load((root / REGISTRY).read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--check", action="store_true", help="kiểm tra content.yml (CI)")
    g.add_argument("--init", action="store_true", help="sinh content.yml lần đầu từ nav")
    g.add_argument("--sync-frontmatter", action="store_true",
                   help="ghi tier, block từ content.yml vào front matter của trang viết tay")
    ap.add_argument("--force", action="store_true", help="cùng --init: ghi đè content.yml đã có")
    ap.add_argument("--stdout", action="store_true", help="cùng --init: in ra, không ghi file")
    args = ap.parse_args(argv)

    if args.init:
        reg, sections = build_registry(ROOT)
        text = dump_registry(reg, sections)
        assert yaml.safe_load(text) == reg, "bản in ra không đọc lại được đúng như dữ liệu"
        if args.stdout:
            sys.stdout.write(text)
            return 0
        target = ROOT / REGISTRY
        if target.exists() and not args.force:
            print("content.yml đã có; không ghi đè (thêm --force nếu thật sự muốn sinh lại).", file=sys.stderr)
            return 1
        target.write_text(text, encoding="utf-8")
        errors = check(copy.deepcopy(reg), ROOT)
        print(f"Đã ghi content.yml: {len(reg['pages'])} trang, {len(reg['data'])} file dữ liệu"
              + (f"; {len(errors)} lỗi khi kiểm tra lại" if errors else "."))
        return 1 if errors else 0

    if not (ROOT / REGISTRY).exists():
        print("Chưa có content.yml — chạy: python tools/content_registry.py --init", file=sys.stderr)
        return 1
    reg = load_registry(ROOT)
    if args.sync_frontmatter:
        n = sync_frontmatter(reg, ROOT)
        print(f"Front matter: đã cập nhật {n} trang.")
    errors = check(reg, ROOT)
    if errors:
        print(f"content.yml lệch với trang và dữ liệu ({len(errors)} lỗi):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    n_pages = len(reg["pages"])
    tiers = {}
    for e in reg["pages"]:
        tiers[e["tier"]] = tiers.get(e["tier"], 0) + 1
    print(f"Sổ đăng ký khớp: {n_pages} trang ({', '.join(f'{k} {v}' for k, v in sorted(tiers.items()))}), "
          f"{len(reg['data'])} file dữ liệu.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
