"""Kiểm bảng thay chữ (không ghi file): python check_rep.py bang.json
Mỗi mục [path, old, new]; old phải xuất hiện đúng 1 lần trong file (sau khi áp các mục trước của cùng bảng)."""
import json, sys, re
rows = json.load(open(sys.argv[1]))
cache = {}
ok = True
for p, old, new in rows:
    s = cache.get(p) or open("/Users/mitu/Desktop/work/projects/logos/" + p, encoding="utf-8").read()
    n = s.count(old)
    if n != 1:
        print(f"LỖI {p}: old xuất hiện {n} lần: {old[:80]!r}"); ok = False; continue
    s = s.replace(old, new); cache[p] = s
for p, s in cache.items():
    for line in s.splitlines():
        if line.lstrip().startswith('{"q"'):
            try: json.loads(line.strip().rstrip(','))
            except Exception as e: print(f"LỖI JSON quiz {p}: {e}: {line[:80]}"); ok = False
print("ok" if ok else "CÓ LỖI")
