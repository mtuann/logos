"""Sinh trang triết gia (docs/triet-gia/<id>.md), trang chỉ mục (docs/triet-gia/index.md)
và docs/assets/data/philosophers.json từ kho dữ kiện (đợt 2, quyết định 7):

- data/kb/people.yml: tên, năm, trường phái, tóm tắt, ảnh hưởng (một bản ghi một người);
- data/people/<id>.yml: phần văn của hồ sơ (tiểu sử, tác phẩm, tư tưởng, một lập luận tiêu biểu,
  hiểu lầm thường gặp, trích dẫn, đọc tiếp, nguồn).

philosophers.json là file sinh (timeline.py, influence.py đọc nó). Hai phần được tính tự
động, không viết tay:

- "Chịu ảnh hưởng từ": đảo ngược trường "influence".
- "Các bài khác nhắc tới": quét docs/ tìm các bài có link tới trang triết
  gia (../triet-gia/<id>.md). Vì vậy thêm link tới một triết gia trong bài
  nào thì phải chạy lại tool này (CI --check sẽ nhắc).

    python tools/philosophers.py          # sinh lại toàn bộ trang và philosophers.json
    python tools/philosophers.py --check  # báo lỗi (mã thoát 1) nếu trang hoặc JSON lệch
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "assets" / "data" / "philosophers.json"
OUT = DOCS / "triet-gia"
MARKER = "<!-- gen:philosophers: không sửa tay -->"
UPDATED = "2026-10-22"

SCHOOLS = ["Tiền Socrates", "Hy Lạp cổ đại", "La Mã", "Trung cổ", "Cận đại",
           "Thế kỷ 19", "Thế kỷ 20", "Trung Hoa", "Ấn Độ", "Việt Nam"]

# Nhãn độ chắc chắn chỉ có nghĩa trong các bài có chú giải nhãn; lọt vào dữ
# liệu triết gia thì nó hiện ra trơ trọi ở chỉ mục và dòng thời gian.
CERTAINTY_LABEL = re.compile(r"\[(chắc chắn|có cơ sở|suy đoán)\]")

# Nội dung hồ sơ (đợt 2, quyết định 7) nằm ở data/people/<id>.yml, mỗi người một file; dữ kiện chính
# (tên, năm, trường phái, tóm tắt, ảnh hưởng) ở data/kb/people.yml. Schema: schema/kb/. Mỗi hồ sơ:
#   desc      một câu cho thẻ mô tả (front matter);
#   bio       3-4 đoạn tiểu sử và bối cảnh, mỗi phần tử một đoạn;
#   works     tác phẩm chính: {year, title (tên gốc in nghiêng), note (tên/diễn giải tiếng Việt)};
#   thoughts  3-5 ý tưởng chính;
#   argument  (tùy chọn) một lập luận tiêu biểu: title, premises, conclusion,
#             objection (phản bác chính), reply (cách đáp lại);
#   misread   (tùy chọn) hiểu lầm thường gặp;
#   quote     (tùy chọn) trích văn bản thuộc phạm vi công cộng: source, orig, vi, url;
#   related   2-5 trang trong docs/ nên đọc tiếp: {path, title};
#   sources   2-6 nguồn: {text (nhãn Markdown), url (rỗng với sách in)}, ít nhất một mục SEP hoặc IEP.
# Không bịa: năm, tên tác phẩm, trích dẫn đều phải kiểm chứng được qua nguồn.
KB_PEOPLE = ROOT / "data" / "kb" / "people.yml"
PROFILES = ROOT / "data" / "people"

# Đọc vào lúc chạy (load_people); render_person và validate dùng như một hằng.
CONTENT: dict[str, dict] = {}


def load_people() -> list[dict]:
    """people.yml → danh sách bản ghi dạng philosophers.json (giữ thứ tự của file)."""
    people = yaml.safe_load(KB_PEOPLE.read_text(encoding="utf-8"))
    return [
        {"end": r["died"], "id": pid, "influence": r["influence"], "name": r["name"], "name_en": r["name_en"],
         "school": r["school"], "start": r["born"], "summary": r["summary"], "years": r["years_label"]}
        for pid, r in people.items()
    ]


def load_content() -> dict[str, dict]:
    """data/people/<id>.yml → hồ sơ, với works/related/sources trở lại dạng tuple mà phần sinh trang dùng."""
    out = {}
    for f in sorted(PROFILES.glob("*.yml")):
        c = yaml.safe_load(f.read_text(encoding="utf-8"))
        c["works"] = [(w["year"], w["title"], w["note"]) for w in c.get("works", [])]
        c["related"] = [(r["path"], r["title"]) for r in c.get("related", [])]
        c["sources"] = [(s["text"], s["url"]) for s in c.get("sources", [])]
        out[f.stem] = c
    return out


def dump_json(data: list[dict]) -> str:
    """philosophers.json đúng định dạng cũ: gọn, khóa sắp xếp, không xuống dòng cuối file."""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


# ----------------------------------------------------------------------------
# Sinh trang
# ----------------------------------------------------------------------------

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_TO_PERSON = re.compile(r"\]\((?:\.\./)*triet-gia/([a-z0-9-]+)\.md(?:#[^)\s]*)?\)")
# Không tính vào "các bài khác nhắc tới": trang sinh tự động liệt kê mọi
# triết gia, các trang triết gia khác, và mục Thêm (sách in chép lại mọi bài).
BACKLINK_SKIP = {"lich-su/dong-thoi-gian.md", "lich-su/so-do-anh-huong.md", "tac-pham/index.md"}  # trang sinh từ dữ liệu
BACKLINK_SKIP_DIRS = ("triet-gia/", "them/")
SECTION_ORDER = ["bat-dau", "cong-cu", "cau-hoi", "lich-su", "doc"]


def validate(data: list) -> list[str]:
    errors = []
    ids = {p.get("id") for p in data}
    for p in data:
        pid = p.get("id")
        if p.get("school") not in SCHOOLS:
            errors.append(f"{pid}: school lạ: {p.get('school')}")
        for inf in p.get("influence", []):
            if inf not in ids:
                errors.append(f"{pid}: influence lạ: {inf}")
        if CERTAINTY_LABEL.search(p.get("summary", "")):
            errors.append(f"{pid}: summary chứa nhãn độ chắc chắn")
        c = CONTENT.get(pid)
        if c is None:
            errors.append(f"{pid}: thiếu hồ sơ data/people/{pid}.yml")
            continue
        if not c.get("bio") or not c.get("thoughts"):
            errors.append(f"{pid}: bio/thoughts rỗng")
        if not c.get("sources"):
            errors.append(f"{pid}: thiếu sources")
        for _, url in c.get("sources", []):
            if url and not url.startswith("https://"):
                errors.append(f"{pid}: URL nguồn phải là https: {url}")
        for rel, _ in c.get("related", []):
            if not (DOCS / rel).is_file():
                errors.append(f"{pid}: related trỏ tới trang không có: {rel}")
        a = c.get("argument")
        if a and not (a.get("premises") and a.get("conclusion")):
            errors.append(f"{pid}: argument thiếu premises/conclusion")
        if CERTAINTY_LABEL.search(json.dumps(c, ensure_ascii=False)):
            errors.append(f"{pid}: nội dung chứa nhãn độ chắc chắn")
    extra = set(CONTENT) - ids
    if extra:
        errors.append(f"data/people/ thừa hồ sơ không có trong people.yml: {sorted(extra)}")
    return errors


def reverse_influence(data: list) -> dict[str, list[dict]]:
    """rev[X] = những người có X trong "influence" của họ, tức những người đã ảnh hưởng tới X."""
    by_id = {p["id"]: p for p in data}
    rev: dict[str, list[dict]] = {p["id"]: [] for p in data}
    for p in data:
        for t in p.get("influence", []):
            if t in rev:
                rev[t].append(p)
    for lst in rev.values():
        lst.sort(key=lambda p: (p["start"], p["name"]))
    return by_id, rev


def page_title(text: str, fallback: str) -> str:
    m = FRONT_MATTER.match(text)
    if m:
        meta = yaml.safe_load(m.group(1)) or {}
        if meta.get("title"):
            return str(meta["title"])
    h = re.search(r"^# (.+)$", text, re.M)
    return h.group(1).strip() if h else fallback


def backlinks(ids: set[str]) -> dict[str, list[tuple[str, str]]]:
    """{id: [(đường dẫn từ docs/, tiêu đề)]}: các bài có link tới trang của triết gia."""
    found: dict[str, list[tuple[str, str]]] = {i: [] for i in ids}
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(DOCS).as_posix()
        if "/" not in rel or rel in BACKLINK_SKIP or rel.startswith(BACKLINK_SKIP_DIRS):
            continue
        text = path.read_text(encoding="utf-8")
        linked = set(LINK_TO_PERSON.findall(text)) & ids
        if not linked:
            continue
        title = page_title(text, path.stem)
        for pid in linked:
            found[pid].append((rel, title))

    def order(item: tuple[str, str]) -> tuple[int, str]:
        section = item[0].split("/")[0]
        rank = SECTION_ORDER.index(section) if section in SECTION_ORDER else len(SECTION_ORDER)
        return rank, item[0]

    for lst in found.values():
        lst.sort(key=order)
    return found


def link(p: dict) -> str:
    return f"[{p['name']}]({p['id']}.md)"


def render_person(p: dict, by_id: dict, rev: dict, back: dict) -> str:
    c = CONTENT[p["id"]]
    L = []
    L.append("---")
    L.append(f'title: "{p["name"]}"')
    L.append(f'description: "{c["desc"]}"')
    L.append(f"updated: {UPDATED}")
    L.append("---")
    L.append("")
    L.append(MARKER)
    L.append("")
    L.append(f"# {p['name']}")
    L.append("")
    head = f"**{p['years']}** · {p['school']}"
    if p["name_en"] != p["name"]:
        head += f" · *{p['name_en']}*"
    L.append(head)
    L.append("")
    # Mỗi đoạn tiểu sử cách nhau một dòng trống — viết liền thì Markdown gộp
    # thành một đoạn (lỗi của bản sinh trước 22/10/2026).
    for para in c["bio"]:
        L.append(para)
        L.append("")
    if c.get("works"):
        L.append("## Tác phẩm chính")
        L.append("")
        for year, title, gloss in c["works"]:
            line = f"- {title}"
            if year:
                line += f" ({year})"
            if gloss:
                line += f" — {gloss}"
            L.append(line)
        L.append("")
    L.append("## Tư tưởng chính")
    L.append("")
    for t in c["thoughts"]:
        L.append(f"- {t}")
    L.append("")
    a = c.get("argument")
    if a:
        L.append(f"## Một lập luận tiêu biểu: {a['title']}" if a.get("title") else "## Một lập luận tiêu biểu")
        L.append("")
        if a.get("intro"):
            L.append(a["intro"])
            L.append("")
        for i, premise in enumerate(a["premises"], 1):
            L.append(f"- **P{i}.** {premise}")
        L.append(f"- **K.** {a['conclusion']}")
        L.append("")
        if a.get("objection"):
            L.append(f"**Phản bác chính.** {a['objection']}")
            L.append("")
        if a.get("reply"):
            L.append(f"**Cách đáp lại.** {a['reply']}")
            L.append("")
    q = c.get("quote")
    if q:
        L.append(f'!!! quote "{q["source"]}"')
        L.append(f'    "{q["orig"]}"')
        L.append("")
        L.append(f'    "{q["vi"]}" *(bản dịch của Logos Zero)*')
        L.append("")
    if c.get("misread"):
        L.append("## Hiểu lầm thường gặp")
        L.append("")
        for m in c["misread"]:
            L.append(f"- {m}")
        L.append("")
    L.append("## Ảnh hưởng")
    L.append("")
    influenced_by = rev[p["id"]]
    if influenced_by:
        L.append("**Chịu ảnh hưởng từ:** " + ", ".join(link(q) for q in influenced_by) + ".")
    else:
        L.append("**Chịu ảnh hưởng từ:** chưa ghi nhận trong dữ liệu của site.")
    L.append("")
    targets = [by_id[t] for t in p.get("influence", []) if t in by_id]
    targets.sort(key=lambda q: (q["start"], q["name"]))
    if targets:
        L.append("**Ảnh hưởng tới:** " + ", ".join(link(q) for q in targets) + ".")
    else:
        L.append("**Ảnh hưởng tới:** chưa ghi nhận trong dữ liệu của site.")
    L.append("")
    L.append("## Đọc thêm trên Logos Zero")
    L.append("")
    curated = [rel for rel, _ in c["related"]]
    for rel, label in c["related"]:
        L.append(f"- [{label}](../{rel})")
    L.append("")
    others = [(rel, title) for rel, title in back[p["id"]] if rel not in curated]
    if others:
        L.append(f"**Các bài khác nhắc tới {p['name']}:** "
                 + ", ".join(f"[{title}](../{rel})" for rel, title in others) + ".")
        L.append("")
    L.append("## Nguồn")
    L.append("")
    for i, (label, url) in enumerate(c["sources"], 1):
        L.append(f"{i}. {label}" + (f" <{url}>" if url else ""))
    L.append("")
    L.append("---")
    L.append("")
    L.append("*[Các triết gia](index.md) · [Dòng thời gian triết học](../lich-su/dong-thoi-gian.md) · "
             "[Sơ đồ ảnh hưởng](../lich-su/so-do-anh-huong.md)*")
    L.append("")
    return "\n".join(L)


EAST = {"Trung Hoa", "Ấn Độ", "Việt Nam"}


def render_index(data: list) -> str:
    def span(group: list) -> str:
        group = sorted(group, key=lambda p: p["start"])
        return f"từ {group[0]['name']} đến {group[-1]['name']}"

    west = [p for p in data if p["school"] not in EAST]
    east = [p for p in data if p["school"] in EAST]
    parts = ["tiểu sử"]
    if any(CONTENT[p["id"]].get("works") for p in data):
        parts.append("tác phẩm chính")
    parts.append("tư tưởng chính")
    if any(CONTENT[p["id"]].get("argument") for p in data):
        parts.append("một lập luận tiêu biểu viết ở dạng chuẩn kèm phản bác")
    parts += ["ai ảnh hưởng đến họ và họ ảnh hưởng đến ai", "các bài trên site nhắc tới họ", "nguồn để đọc tiếp"]
    L = []
    L.append("---")
    L.append('title: "Các triết gia"')
    L.append(f'description: "{len(data)} triết gia {span(west)}, {span(east)} — mỗi người một trang: tiểu sử, tư tưởng, ảnh hưởng và nguồn."')
    L.append(f"updated: {UPDATED}")
    L.append("---")
    L.append("")
    L.append(MARKER)
    L.append("")
    L.append("# Các triết gia")
    L.append("")
    L.append("Triết học không phải danh sách trừu tượng các “chủ nghĩa” — đó là câu chuyện của những con người cụ thể, sống trong thời đại cụ thể, tranh luận với nhau qua nhiều thế kỷ. "
             f"Mỗi triết gia dưới đây có một trang riêng: {', '.join(parts[:-1])} và {parts[-1]}.")
    L.append("")
    L.append(f"Hiện có **{len(data)} triết gia**.")
    L.append("")
    for school in SCHOOLS:
        group = sorted([p for p in data if p["school"] == school],
                       key=lambda p: (p["start"], p["name"]))
        if not group:
            continue
        L.append(f"### {school}")
        L.append("")
        for p in group:
            L.append(f"- [{p['name']} ({p['years']})]({p['id']}.md) — {p['summary']}")
        L.append("")
    L.append("*Xem toàn cảnh: [Dòng thời gian triết học](../lich-su/dong-thoi-gian.md) · "
             "[Sơ đồ ảnh hưởng](../lich-su/so-do-anh-huong.md)*")
    L.append("")
    return "\n".join(L)


def generate(data: list) -> dict[str, str]:
    """Trả về {đường dẫn tương đối từ OUT: nội dung}."""
    by_id, rev = reverse_influence(data)
    back = backlinks(set(by_id))
    out = {}
    for p in data:
        out[f"{p['id']}.md"] = render_person(p, by_id, rev, back)
    out["index.md"] = render_index(data)
    return out


def main(argv: list[str]) -> int:
    data = load_people()
    CONTENT.clear()
    CONTENT.update(load_content())
    errors = validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    pages = generate(data)
    if "--check" in argv:
        problems = []
        if not DATA.exists() or DATA.read_text(encoding="utf-8") != dump_json(data):
            problems.append("lệch nội dung: docs/assets/data/philosophers.json")
        existing = {p.name for p in OUT.glob("*.md")} if OUT.is_dir() else set()
        for name, body in sorted(pages.items()):
            path = OUT / name
            if not path.exists():
                problems.append(f"thiếu file: docs/triet-gia/{name}")
            elif path.read_text(encoding="utf-8") != body:
                problems.append(f"lệch nội dung: docs/triet-gia/{name}")
        for name in sorted(existing - set(pages)):
            problems.append(f"file thừa (không do generator sinh): docs/triet-gia/{name}")
        if problems:
            print("Trang triết gia lệch so với dữ liệu:", file=sys.stderr)
            print("\n".join(f"  {x}" for x in problems), file=sys.stderr)
            print("Chạy: python tools/philosophers.py", file=sys.stderr)
            return 1
        print(f"Trang triết gia khớp dữ liệu ({len(pages)} trang).")
        return 0
    DATA.write_text(dump_json(data), encoding="utf-8")
    OUT.mkdir(parents=True, exist_ok=True)
    for name, body in sorted(pages.items()):
        (OUT / name).write_text(body, encoding="utf-8")
    print(f"Đã sinh {len(pages)} trang trong docs/triet-gia/ ({len(data)} triết gia + chỉ mục).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
