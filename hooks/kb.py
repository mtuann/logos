"""Shortcode dữ kiện: in số đếm, số liệu, dữ kiện từ dữ liệu lúc build (KE-HOACH.md mục 4, quyết định 3).

Cú pháp (chốt ở đợt 1, việc 1.8): `[[loại:khóa]]`, viết liền, chữ thường, không dấu cách.

    [[count:cau-hoi]]            số trang loại cau-hoi trong content.yml          → 57
    [[count:cau-hoi/dao-duc]]    số trang loại cau-hoi thuộc khối dao-duc          → 7
    [[count:lich-su]]            số bài lịch sử (không tính Dòng thời gian, Sơ đồ) → 8
    [[count:triet-gia]]          số trang triết gia (không tính index.md)          → 59
    [[count:nguy-bien]]          số đoạn hội thoại ngụy biện (fallacies.json)      → 100
    [[count:thuat-ngu]]          số thuật ngữ (terms.json)                         → 249
    [[count:quiz]]               số câu trong ngân hàng quiz (quiz-bank.json)      → 428

Loại `count` đọc content.yml: đếm trang có `type` cho trước, lọc thêm theo `block` nếu có `/khối`. Không đếm
trang he-thong và trang sinh tự động (lich-su/dong-thoi-gian.md…), trừ trang triết gia: mỗi trang là một hồ sơ. Số từ 1.000 trở lên in kiểu Việt Nam (1.234).
Các loại khác (số liệu PhilPapers, dữ kiện trong kho) được thêm ở đợt 2–3 bằng cách đăng ký vào HANDLERS.

    [[pp:tu-do-y-chi.tuong-thich-luan]]        % chấp nhận hoặc nghiêng về (data/kb/philpapers-2020.json) → 59,2
    [[pp:tu-do-y-chi.tuong-thich-luan/loai-tru]]  % loại trừ; `/bac-bo`: % bác bỏ (câu chấp nhận / bác bỏ)
    [[pp:tu-do-y-chi/n]]                        số người trả lời câu đó                → 1.760
    [[pp:khao-sat/nguoi-tra-loi]]               số tổng: nguoi-tra-loi, so-cau, cau-chinh, cau-bo-sung, cau-bo-sung-moi-nguoi

Số liệu PhilPapers in một chữ số thập phân, dấu phẩy; ô có `raw` trong JSON (bài báo in khác quy ước) in đúng chữ gốc.

    [[thoi-su:cau-hoi.tu-do-y-chi.bo-luat]]   thân khối data/thoi-su/<id>.md, nguyên văn (ban-giao/dot-3.md)

Khối thời sự được mở trước mọi shortcode khác (thân khối có thể chứa shortcode). Khối một dòng chèn tại chỗ; khối
nhiều dòng thì shortcode phải đứng riêng một dòng, và các dòng sau dòng đầu được thêm đúng thụt lề của dòng đó
(để khối nằm trong danh sách hay admonition). Mỗi khối chỉ được trang ghi ở `page` dùng (link trong khối viết tương
đối với trang đó); tools/thoi_su_check.py kiểm việc này ngoài build.

Shortcode trong khối code (```…```) và code inline (`…`) được giữ nguyên, để tài liệu có thể viết ra cú pháp.
Loại hoặc khóa không tồn tại thì build dừng (PluginError), kèm tên trang: không bao giờ in ra số sai hay chỗ trống.
Mã băm đơn vị (tools/lz/normalize.py) giữ shortcode nguyên dạng, nên số đếm đổi không mở khóa đơn vị Lõi.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Callable

import yaml

try:
    from properdocs.exceptions import PluginError
except ImportError:  # chạy dưới mkdocs 1.6.1 (lối lùi ở KE-HOACH.md mục 11)
    from mkdocs.exceptions import PluginError

SHORTCODE = re.compile(r"\[\[([a-z][a-z-]*):([a-z0-9][a-z0-9/._-]*)\]\]")
FENCE = re.compile(r"^([ \t]*)(`{3,}|~{3,})[^\n]*\n.*?^\1\2[ \t]*$", re.S | re.M)
CODE_SPAN = re.compile(r"(`+)(?!`).+?(?<!`)\1(?!`)", re.S)

THOI_SU = re.compile(r"\[\[thoi-su:([a-z0-9][a-z0-9._-]*)\]\]")
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)

_ctx: dict | None = None


def load_registry(root: Path) -> dict:
    return yaml.safe_load((root / "content.yml").read_text(encoding="utf-8"))


def load_thoi_su(root: Path) -> dict[str, dict]:
    """id → {"meta": front matter, "body": thân khối (bỏ đúng một ký tự xuống dòng cuối file)}."""
    out = {}
    d = root / "data" / "thoi-su"
    for f in sorted(d.glob("*.md")) if d.is_dir() else []:
        text = f.read_text(encoding="utf-8")
        m = FRONT.match(text)
        if not m:
            raise PluginError(f"{f.relative_to(root)}: thiếu front matter")
        body = text[m.end():]
        out[f.stem] = {"meta": yaml.safe_load(m.group(1)) or {}, "body": body[:-1] if body.endswith("\n") else body}
    return out


def load_context(root: Path) -> dict:
    """Mọi dữ liệu shortcode cần, đọc một lần mỗi lần build."""
    return {"root": root, "registry": load_registry(root), "thoi_su": load_thoi_su(root)}


def fmt_int(n: int) -> str:
    return f"{n:,}".replace(",", ".")


# Số bản ghi trong file dữ liệu: loại → (file, khóa của danh sách). Tên không trùng `type` của trang.
DATA_COUNTS = {
    "nguy-bien": ("docs/assets/data/fallacies.json", "questions"),
    "thuat-ngu": ("docs/assets/data/terms.json", "terms"),
    "quiz": ("docs/assets/data/quiz-bank.json", "items"),
}


def count(key: str, ctx: dict) -> str:
    registry = ctx["registry"]
    kind, _, block = key.partition("/")
    if kind in DATA_COUNTS:
        if block:
            raise KeyError(f"loại dữ liệu {kind!r} không lọc theo khối")
        path, field = DATA_COUNTS[kind]
        cache = ctx.setdefault("_data", {})
        if path not in cache:
            cache[path] = json.loads((ctx["root"] / path).read_text(encoding="utf-8"))
        return fmt_int(len(cache[path][field]))
    # Đếm "bài": bỏ trang he-thong và trang sinh tự động (Dòng thời gian, Sơ đồ ảnh hưởng…), trừ trang triết gia,
    # vì mỗi trang triết gia sinh ra là một hồ sơ.
    pages = [p for p in registry["pages"]
             if p["type"] != "he-thong" and (not p["generated"] or p["type"] == "triet-gia")]
    types = {p["type"] for p in pages}
    if kind not in types:
        raise KeyError(f"loại {kind!r} không có trong content.yml hay DATA_COUNTS (có: {', '.join(sorted(types | set(DATA_COUNTS)))})")
    hits = [p for p in pages if p["type"] == kind]
    if block:
        blocks = {p["block"] for p in hits}
        if block not in blocks:
            raise KeyError(f"khối {block!r} không có trang loại {kind} (có: {', '.join(sorted(b for b in blocks if b))})")
        hits = [p for p in hits if p["block"] == block]
    return fmt_int(len(hits))


PP_FIELDS = {"": "pct", "bac-bo": "pct_reject", "loai-tru": "pct_exclusive"}


def pp(key: str, ctx: dict) -> str:
    if "_pp" not in ctx:
        data = json.loads((ctx["root"] / "data" / "kb" / "philpapers-2020.json").read_text(encoding="utf-8"))
        ctx["_pp"] = (data, {q["id"]: q for q in data["questions"]})
    data, questions = ctx["_pp"]
    path, _, suffix = key.partition("/")
    if path == "khao-sat":
        survey = data["source"].get("survey", {})
        if suffix not in survey:
            raise KeyError(f"số tổng {suffix!r} không có (có: {', '.join(survey)})")
        return fmt_int(survey[suffix])
    qid, _, oid = path.partition(".")
    if qid not in questions:
        raise KeyError(f"câu {qid!r} không có trong philpapers-2020.json")
    q = questions[qid]
    if not oid:
        if suffix != "n" or "n" not in q:
            raise KeyError(f"câu {qid}: chỉ có [[pp:{qid}/n]] (số người trả lời)")
        return fmt_int(q["n"])
    o = next((o for o in q["options"] if o["id"] == oid), None)
    if o is None:
        raise KeyError(f"câu {qid}: lựa chọn {oid!r} không có (có: {', '.join(x['id'] for x in q['options'])})")
    if suffix not in PP_FIELDS:
        raise KeyError(f"hậu tố {suffix!r} không có (có: /bac-bo, /loai-tru)")
    field = PP_FIELDS[suffix]
    raw = o.get("raw", {}).get(field)
    if raw:
        return raw
    if o.get(field) is None:
        raise KeyError(f"{qid}.{oid}: không có {field}")
    return f"{o[field]:.1f}".replace(".", ",")


HANDLERS: dict[str, Callable[[str, dict], str]] = {"count": count, "pp": pp}


def _outside_code(markdown: str, fn: Callable[[str], str]) -> str:
    """Áp `fn` lên mọi đoạn ngoài khối code rào và code inline."""
    pos = 0
    protected = sorted([m.span() for m in FENCE.finditer(markdown)])
    spans = []
    for a, b in protected + [(len(markdown), len(markdown))]:
        chunk = markdown[pos:a]
        cpos = 0
        for m in CODE_SPAN.finditer(chunk):
            spans.append(fn(chunk[cpos:m.start()]))
            spans.append(m.group(0))
            cpos = m.end()
        spans.append(fn(chunk[cpos:]))
        spans.append(markdown[a:b])
        pos = b
    return "".join(spans)


def expand_thoi_su(markdown: str, blocks: dict, where: str = "") -> str:
    """Thay [[thoi-su:id]] bằng thân khối; khối nhiều dòng nhận thụt lề của dòng chứa shortcode."""
    def sub(m: re.Match) -> str:
        key = m.group(1)
        if key not in blocks:
            raise PluginError(f"{where}: shortcode [[thoi-su:{key}]]: không có data/thoi-su/{key}.md")
        page = blocks[key]["meta"].get("page")
        if where and page != where:
            raise PluginError(f"{where}: shortcode [[thoi-su:{key}]]: khối này thuộc trang {page!r}")
        body = blocks[key]["body"]
        if "\n" not in body:
            return body
        s, line_start = m.string, m.string.rfind("\n", 0, m.start()) + 1
        line_end = s.find("\n", m.end())
        line_end = len(s) if line_end < 0 else line_end
        indent = s[line_start:m.start()]
        if indent.strip() or s[m.end():line_end].strip():
            raise PluginError(f"{where}: shortcode [[thoi-su:{key}]]: khối nhiều dòng phải đứng riêng một dòng")
        return "\n".join(ln if (i == 0 or not ln) else indent + ln for i, ln in enumerate(body.split("\n")))

    return _outside_code(markdown, lambda chunk: THOI_SU.sub(sub, chunk))


def expand(markdown: str, ctx: dict, where: str = "") -> str:
    """Thay mọi shortcode ngoài code; KeyError/PluginError khi loại hay khóa không tồn tại."""
    if "[[thoi-su:" in markdown:
        markdown = expand_thoi_su(markdown, ctx.get("thoi_su", {}), where)

    def sub(m: re.Match) -> str:
        kind, key = m.group(1), m.group(2)
        handler = HANDLERS.get(kind)
        if handler is None:
            raise PluginError(f"{where}: shortcode [[{kind}:{key}]]: loại {kind!r} chưa có "
                              f"(có: {', '.join(sorted(HANDLERS))})")
        try:
            return handler(key, ctx)
        except KeyError as exc:
            raise PluginError(f"{where}: shortcode [[{kind}:{key}]]: {exc.args[0]}") from None

    return _outside_code(markdown, lambda chunk: SHORTCODE.sub(sub, chunk))


def on_config(config, **kwargs):
    global _ctx
    _ctx = load_context(Path(config["config_file_path"]).resolve().parent)
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    if "[[" not in markdown:
        return markdown
    return expand(markdown, _ctx, page.file.src_uri)
