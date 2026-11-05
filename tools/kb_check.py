"""Kiểm kho dữ kiện data/kb/ và hồ sơ data/people/ (KE-HOACH.md mục 4, 5.4; ban-giao/dot-2.md việc 2.1).

    python tools/kb_check.py --check    # CI: mã thoát 1 khi có bản ghi sai

Kiểm:
  - mỗi file theo schema của nó trong schema/kb/ (jsonschema, quyết định 13);
  - khóa trùng trong YAML (PyYAML mặc định lặng lẽ giữ khóa sau: ở đây là lỗi);
  - tham chiếu chéo: people.influence → people; works.author → people; quotes.work → works;
    evidence (không phải URL) → sources; data/people/<id>.yml ↔ people.yml một–một;
    related[].path của hồ sơ → trang có trong docs/; used_in → đơn vị (trang.md#id) hoặc hồ sơ còn tồn tại;
  - philpapers: id câu không trùng, id lựa chọn không trùng trong một câu; số tổng `source.survey` có trong preamble.
File chưa tạo thì bỏ qua (kho được lấp dần trong đợt 2).
"""

from __future__ import annotations

import argparse
import json
import sys
from functools import lru_cache
from pathlib import Path

import jsonschema
import yaml

from lz import ROOT, units

KB = Path("data") / "kb"
PEOPLE_DIR = Path("data") / "people"
SCHEMAS = Path("schema") / "kb"
FILES = {  # loại → (file, schema)
    "people": (KB / "people.yml", "people"),
    "works": (KB / "works.yml", "works"),
    "quotes": (KB / "quotes.yml", "quotes"),
    "events": (KB / "events.yml", "events"),
    "sources": (KB / "sources.yml", "sources"),
    "philpapers": (KB / "philpapers-2020.json", "philpapers"),
}


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(None, None, f"khóa trùng {key!r}", key_node.start_mark)
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_file(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    return yaml.load(text, Loader=_UniqueKeyLoader)


def schema(name: str, root: Path) -> dict:
    return json.loads((root / SCHEMAS / f"{name}.schema.json").read_text(encoding="utf-8"))


def schema_errors(data, sch: dict, where: str) -> list[str]:
    v = jsonschema.Draft202012Validator(sch)
    out = []
    for e in sorted(v.iter_errors(data), key=lambda e: list(map(str, e.absolute_path))):
        path = "/".join(str(p) for p in e.absolute_path) or "(gốc)"
        out.append(f"{where}: {path}: {e.message}")
    return out


@lru_cache(maxsize=None)
def _unit_ids(page: str, root: Path) -> frozenset[str] | None:
    f = root / "docs" / page
    if not f.exists():
        return None
    return frozenset(u.id for u in units.split_file(page, root))


def check_used_in(where: str, refs, root: Path, people: dict) -> list[str]:
    out = []
    for ref in refs or []:
        if ref.startswith("people/"):
            if ref.split("/", 1)[1] not in people:
                out.append(f"{where}: used_in {ref}: không có trong people.yml")
            continue
        page, _, ident = ref.partition("#")
        ids = _unit_ids(page, root)
        if ids is None:
            out.append(f"{where}: used_in {ref}: không có trang docs/{page}")
        elif ident not in ids:
            out.append(f"{where}: used_in {ref}: trang không có mục #{ident}")
    return out


def check(root: Path = ROOT) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    data: dict[str, object] = {}
    counts: dict[str, int] = {}
    _unit_ids.cache_clear()
    for kind, (rel, sch) in FILES.items():
        f = root / rel
        if not f.exists():
            continue
        try:
            d = load_file(f)
        except (yaml.YAMLError, json.JSONDecodeError) as exc:
            errors.append(f"{rel}: không đọc được: {exc}")
            continue
        errors += schema_errors(d, schema(sch, root), str(rel))
        data[kind] = d
        counts[kind] = len(d["questions"]) if kind == "philpapers" and isinstance(d, dict) else len(d or {})

    people = data.get("people") or {}
    works = data.get("works") or {}
    sources = data.get("sources") or {}

    for pid, p in people.items():
        for other in p.get("influence", []):
            if other not in people:
                errors.append(f"people.yml: {pid}: influence {other!r} không có trong people.yml")
    for wid, w in works.items():
        if w.get("author") and w["author"] not in people:
            errors.append(f"works.yml: {wid}: author {w['author']!r} không có trong people.yml")
    for qid, q in (data.get("quotes") or {}).items():
        if q.get("work") and q["work"] not in works:
            errors.append(f"quotes.yml: {qid}: work {q['work']!r} không có trong works.yml")
    for kind in ("people", "works", "quotes", "events"):
        for key, rec in (data.get(kind) or {}).items():
            for ev in rec.get("evidence", []) if isinstance(rec, dict) else []:
                if not ev.startswith(("http://", "https://")) and ev not in sources:
                    errors.append(f"{kind}.yml: {key}: evidence {ev!r} không phải URL, cũng không có trong sources.yml")
    for kind in ("works", "quotes", "events", "sources"):
        for key, rec in (data.get(kind) or {}).items():
            if isinstance(rec, dict):
                errors += check_used_in(f"{kind}.yml: {key}", rec.get("used_in"), root, people)

    pp = data.get("philpapers")
    if isinstance(pp, dict):
        seen_q = set()
        for q in pp.get("questions", []):
            if q.get("id") in seen_q:
                errors.append(f"philpapers-2020.json: câu {q.get('id')!r} trùng")
            seen_q.add(q.get("id"))
            ids = [o.get("id") for o in q.get("options", [])]
            for dup in sorted({i for i in ids if ids.count(i) > 1}):
                errors.append(f"philpapers-2020.json: {q.get('id')}: lựa chọn {dup!r} trùng")
        src = pp.get("source", {})
        for field, v in (src.get("survey") or {}).items():   # số tổng phải chép đúng từ phần mở đầu
            if f"{v:,}".replace(",", ".") not in src.get("preamble", ""):
                errors.append(f"philpapers-2020.json: source.survey.{field} = {v} không có trong source.preamble")

    pdir = root / PEOPLE_DIR
    if pdir.is_dir():
        prof_schema = schema("person-profile", root)
        files = sorted(pdir.glob("*.yml"))
        counts["people-profiles"] = len(files)
        ids = {f.stem for f in files}
        for f in files:
            rel = f.relative_to(root)
            try:
                d = load_file(f)
            except yaml.YAMLError as exc:
                errors.append(f"{rel}: không đọc được: {exc}")
                continue
            errors += schema_errors(d, prof_schema, str(rel))
            for r in (d or {}).get("related", []) if isinstance(d, dict) else []:
                path = str(r.get("path", "")).split("#", 1)[0]
                if path and not (root / "docs" / path).exists():
                    errors.append(f"{rel}: related {path!r} không có trong docs/")
        if people:
            for pid in sorted(set(people) - ids):
                errors.append(f"data/people/: thiếu hồ sơ {pid}.yml cho người có trong people.yml")
            for pid in sorted(ids - set(people)):
                errors.append(f"data/people/{pid}.yml: không có {pid!r} trong people.yml")
    return errors, counts


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", required=True, help="kiểm kho dữ kiện (CI)")
    ap.parse_args(argv)
    errors, counts = check()
    if errors:
        print(f"Kho dữ kiện: {len(errors)} lỗi:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    summary = ", ".join(f"{k} {v}" for k, v in counts.items()) or "chưa có file nào"
    print(f"Kho dữ kiện khớp schema ({summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
