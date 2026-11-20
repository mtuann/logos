"""Kiểm tra tương đương: so văn bản hiển thị của mọi trang trước và sau một thay đổi cơ học (KE-HOACH.md mục 2, 8).

    python tools/parity.py --base main                  # build commit `main` và cây làm việc hiện tại, rồi so
    python tools/parity.py --base v1.0-moc --keep TMP   # như trên, giữ hai bản build trong TMP/truoc, TMP/sau
    python tools/parity.py TRUOC SAU                    # so hai thư mục site/ đã build sẵn
    python tools/parity.py --base main --expect-sub REGEX THAY   # thay đổi có chủ đích: áp phép thay (re.sub)
                                                        # lên bản trước rồi mới so; lệch còn lại mới là lỗi

Với mỗi trang HTML, so:
  - văn bản hiển thị trong <article class="md-content__inner"> (bỏ <script>, <style>; thanh điều hướng,
    đầu trang và chân trang nằm ngoài article nên tự bị bỏ);
  - <title> và <meta name="description">;
  - danh sách thuộc tính id trong article (anchor của tiêu đề, quiz…), để link nội bộ không gãy;
  - chỉ mục tìm kiếm search/search_index.json (từng mục: location, title, text), nếu cả hai bên có.
Thoát mã 0 và in "giống 100%" khi mọi trang trùng nhau; ngược lại in danh sách trang lệch, chỗ lệch đầu tiên
của mỗi trang, và thoát mã 1. Trang có ở một bên mà không có ở bên kia cũng tính là lệch.
"""

from __future__ import annotations

import argparse
import difflib
import fnmatch
import html as htmllib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARTICLE = re.compile(r'<article class="md-content__inner[^"]*">(.*)</article>', re.S)
TITLE = re.compile(r"<title>(.*?)</title>", re.S)
DESCRIPTION = re.compile(r'<meta name="description" content="([^"]*)"')
SKIP = {"script", "style", "template"}
BLOCK = {"p", "div", "li", "ul", "ol", "dl", "dt", "dd", "table", "tr", "td", "th", "thead", "tbody",
         "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre", "details", "summary", "figure",
         "figcaption", "br", "hr", "section", "article", "aside", "header", "footer", "nav", "text"}


VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SINH = "data-oz-sinh"   # phần giao diện sinh thêm (đợt 4): không phải chữ của bài, bỏ ở cả hai bên


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ids: list[str] = []
        self.skip = 0
        self.sinh = 0          # độ sâu bên trong một phần tử data-oz-sinh (0 = ngoài)

    def handle_starttag(self, tag, attrs):
        if self.sinh:
            if tag not in VOID:
                self.sinh += 1
            return
        if any(k == SINH for k, _ in attrs):
            if tag not in VOID:
                self.sinh = 1
            return
        if tag in SKIP:
            self.skip += 1
        for k, v in attrs:
            if k == "id" and v is not None:
                self.ids.append(v)
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_startendtag(self, tag, attrs):
        if self.sinh or any(k == SINH for k, _ in attrs):
            return
        for k, v in attrs:
            if k == "id" and v is not None:
                self.ids.append(v)
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if self.sinh:
            if tag not in VOID:
                self.sinh -= 1
            return
        if tag in SKIP and self.skip:
            self.skip -= 1
        if tag in BLOCK:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.skip and not self.sinh:
            self.parts.append(data)


@dataclass(frozen=True)
class PageText:
    title: str
    description: str
    lines: tuple[str, ...]     # văn bản hiển thị, mỗi khối một dòng, khoảng trắng đã gộp
    ids: tuple[str, ...]


def extract(html: str) -> PageText:
    m = ARTICLE.search(html)
    p = _Text()
    p.feed(m.group(1) if m else "")
    p.close()
    lines = tuple(ln for ln in (" ".join(x.split()) for x in "".join(p.parts).split("\n")) if ln)
    t = TITLE.search(html)
    d = DESCRIPTION.search(html)
    return PageText(
        title=" ".join(htmllib.unescape(t.group(1)).split()) if t else "",
        description=htmllib.unescape(d.group(1)) if d else "",
        lines=lines,
        ids=tuple(p.ids),
    )


def pages(site: Path) -> dict[str, Path]:
    return {str(f.relative_to(site)): f for f in sorted(site.rglob("*.html"))}


def first_diff(a: tuple[str, ...], b: tuple[str, ...], context: int = 1) -> str:
    diff = list(difflib.unified_diff(a, b, "truoc", "sau", n=context, lineterm=""))
    return "\n".join("      " + ln[:200] for ln in diff[2:14])


def _subbed(t: PageText, subs) -> PageText:
    if not subs:
        return t
    f = lambda s: _apply(s, subs)  # noqa: E731
    return PageText(f(t.title), f(t.description), tuple(f(x) for x in t.lines), t.ids)


def _apply(s: str, subs) -> str:
    for rx, rep in subs:
        s = rx.sub(rep, s)
    return s


def _match(p: str, globs) -> bool:
    return any(fnmatch.fnmatch(p, g) for g in globs)


def compare(before: Path, after: Path, subs=(), exempt=(), new_ok=(), notes: list | None = None, both=()) -> tuple[list[str], int]:
    """(danh sách mô tả chỗ lệch, số trang đã so); danh sách rỗng nghĩa là tương đương 100%.
    `subs`: các (regex đã biên dịch, chuỗi thay) áp lên bản trước — thay đổi có chủ đích.
    `exempt`: mẫu đường dẫn HTML (glob) được phép đổi chữ; khác biệt ghi vào `notes`, không tính là lệch.
    `new_ok`: mẫu đường dẫn của trang mới có chủ đích (chỉ có ở bản sau).
    `both`: các (regex, chuỗi thay) áp lên cả hai bản (chuẩn hóa, ví dụ kiểu ngoặc kép: --bo-kieu-ngoac)."""
    notes = notes if notes is not None else []
    a, b = pages(before), pages(after)
    problems = [f"{p}: chỉ có ở bản trước" for p in sorted(a.keys() - b.keys())]
    for p in sorted(b.keys() - a.keys()):
        (notes if _match(p, new_ok) else problems).append(f"{p}: chỉ có ở bản sau{' (trang mới có chủ đích)' if _match(p, new_ok) else ''}")
    for p in sorted(a.keys() & b.keys()):
        if _match(p, exempt):
            x = _subbed(_subbed(extract(a[p].read_text(encoding="utf-8")), subs), both)
            y = _subbed(extract(b[p].read_text(encoding="utf-8")), both)
            if x != y:
                notes.append(f"{p}: ngoại lệ, có đổi chữ\n{first_diff(x.lines, y.lines)}")
            continue
        x = _subbed(_subbed(extract(a[p].read_text(encoding="utf-8")), subs), both)
        y = _subbed(extract(b[p].read_text(encoding="utf-8")), both)
        if x.title != y.title:
            problems.append(f"{p}: <title> lệch: {x.title!r} → {y.title!r}")
        if x.description != y.description:
            problems.append(f"{p}: description lệch:\n      {x.description!r}\n    → {y.description!r}")
        if x.lines != y.lines:
            problems.append(f"{p}: văn bản hiển thị lệch\n{first_diff(x.lines, y.lines)}")
        if x.ids != y.ids:
            gone = [i for i in x.ids if i not in y.ids][:5]
            new = [i for i in y.ids if i not in x.ids][:5]
            problems.append(f"{p}: id lệch (mất {gone}, thêm {new}"
                            f"{', hoặc đổi thứ tự' if not gone and not new else ''})")
    problems += compare_search(before, after, subs, exempt, notes, new_ok, both)
    return problems, len(a.keys() | b.keys())


NOACCENT = re.compile(r'<span hidden class="oz-noaccent">.*?</span>', re.S)


def _no_accent_copy(doc: dict) -> dict:
    """Bỏ bản sao không dấu mà hooks/search_vi.py thêm tới đợt 3 (đợt 4.5: bỏ dấu ở trình duyệt, không còn trong file)."""
    return {k: NOACCENT.sub("", v) if isinstance(v, str) else v for k, v in doc.items()}


def compare_search(before: Path, after: Path, subs=(), exempt=(), notes: list | None = None, new_ok=(), both=()) -> list[str]:
    fa, fb = before / "search" / "search_index.json", after / "search" / "search_index.json"
    if not (fa.exists() and fb.exists()):
        return []
    def page_of(d):   # "lich-su/dong-thoi-gian/#muc" → "lich-su/dong-thoi-gian/index.html"
        return d["location"].split("#")[0] + "index.html"
    norm = lambda d: {k: _apply(v, both) if isinstance(v, str) else v for k, v in d.items()}  # noqa: E731
    da = [norm(_no_accent_copy(d)) for d in json.loads(_apply(fa.read_text(encoding="utf-8"), subs))["docs"]]
    db = [norm(_no_accent_copy(d)) for d in json.loads(fb.read_text(encoding="utf-8"))["docs"]]
    skipped = {page_of(d) for d in da + db if _match(page_of(d), exempt)}
    a_pages = {page_of(d) for d in da}
    fresh = {page_of(d) for d in db if page_of(d) not in a_pages and _match(page_of(d), new_ok)}
    if fresh and notes is not None:
        notes += [f"search_index.json: {p}: trang mới có chủ đích" for p in sorted(fresh)]
    skipped |= fresh
    if skipped and notes is not None:
        changed = sorted(p for p in skipped if [d for d in da if page_of(d) == p] != [d for d in db if page_of(d) == p])
        notes += [f"search_index.json: {p}: ngoại lệ, mục tìm kiếm có đổi" for p in changed]
    da = [d for d in da if page_of(d) not in skipped]
    db = [d for d in db if page_of(d) not in skipped]
    if da == db:
        return []
    ka = {d["location"]: d for d in da}
    kb = {d["location"]: d for d in db}
    diff = sorted(loc for loc in ka.keys() | kb.keys() if ka.get(loc) != kb.get(loc))
    order = "" if diff else " (chỉ khác thứ tự)"
    return [f"search_index.json lệch{order}: {len(diff)} mục, ví dụ {diff[:5]}"]


def build(src: Path, dest: Path) -> None:
    cmd = [sys.executable, "-m", "properdocs", "build", "--strict", "-q", "-f", "mkdocs.yml", "-d", str(dest)]
    r = subprocess.run(cmd, cwd=src, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"build lỗi ở {src}:\n{r.stdout}{r.stderr}")


def build_pair(base: str, tmp: Path) -> tuple[Path, Path]:
    """Build commit `base` (qua git worktree tạm) vào tmp/truoc và cây làm việc hiện tại vào tmp/sau."""
    worktree = tmp / "nguon-truoc"
    subprocess.run(["git", "worktree", "add", "--detach", "-q", str(worktree), base], cwd=ROOT, check=True)
    try:
        build(worktree, tmp / "truoc")
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(worktree)], cwd=ROOT, check=True)
    build(ROOT, tmp / "sau")
    return tmp / "truoc", tmp / "sau"


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dirs", nargs="*", metavar="THU_MUC", help="hai thư mục site đã build: TRUOC SAU")
    ap.add_argument("--base", help="commit/nhánh/tag làm bản trước; bản sau là cây làm việc hiện tại")
    ap.add_argument("--keep", type=Path, help="cùng --base: giữ hai bản build trong thư mục này")
    ap.add_argument("--expect-sub", nargs=2, action="append", default=[], metavar=("REGEX", "THAY"),
                    help="thay đổi có chủ đích, áp lên bản trước trước khi so (lặp lại được)")
    ap.add_argument("--ngoai-le", action="append", default=[], metavar="TRANG",
                    help="trang HTML (glob, ví dụ index.html) được phép đổi chữ: in khác biệt, không tính lệch")
    ap.add_argument("--bo-kieu-ngoac", action="store_true",
                    help="coi “ ” như \" ở cả hai bản (quyết định 26, 39: kiểu ngoặc hiển thị đổi được mà không đổi chữ)")
    ap.add_argument("--trang-moi", action="append", default=[], metavar="TRANG",
                    help="trang HTML mới có chủ đích (glob, ví dụ 'tac-pham/*')")
    args = ap.parse_args(argv)
    notes: list[str] = []
    opts = dict(exempt=args.ngoai_le, new_ok=args.trang_moi, notes=notes,
                both=[(re.compile(r"[“”]|\\u201[cd]"), '"'), (re.compile(r"&quot;"), '"')] if args.bo_kieu_ngoac else [])
    subs = [(re.compile(rx), rep) for rx, rep in args.expect_sub]

    if args.base:
        if args.dirs:
            ap.error("dùng --base hoặc hai thư mục, không dùng cả hai")
        tmp = args.keep or Path(tempfile.mkdtemp(prefix="parity-"))
        tmp.mkdir(parents=True, exist_ok=True)
        try:
            before, after = build_pair(args.base, tmp)
            problems, n = compare(before, after, subs, **opts)
            label = f"{args.base} → cây làm việc"
        finally:
            if not args.keep:
                shutil.rmtree(tmp, ignore_errors=True)
    elif len(args.dirs) == 2:
        before, after = map(Path, args.dirs)
        for d in (before, after):
            if not d.is_dir():
                ap.error(f"{d}: không phải thư mục")
        problems, n = compare(before, after, subs, **opts)
        label = f"{before} → {after}"
    else:
        ap.error("cần --base REF hoặc hai thư mục TRUOC SAU")

    for x in notes:
        print("  · " + x)
    if problems:
        print(f"Tương đương: LỆCH ({label}), {len(problems)} chỗ:")
        for p in problems:
            print("  - " + p)
        return 1
    note = f"; sau khi áp {len(subs)} phép thay có chủ đích" if subs else ""
    note += f"; {len(notes)} ghi chú (ngoại lệ, trang mới)" if notes else ""
    print(f"Tương đương: giống 100% ({label}, {n} trang{note}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
