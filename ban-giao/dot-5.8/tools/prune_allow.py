"""Mục miễn volatile mà linter báo mien-thua: nếu cùng trang còn chỗ bị bắt với cùng từ thì cập nhật ngữ cảnh mới (giữ lý do), không thì bỏ."""
import re, subprocess
def lint():
    return subprocess.run(["uv","run","python","tools/lint_volatile.py","--strict"],capture_output=True,text=True).stdout
out = lint()
stale = re.findall(r'(cau-hoi/[\w-]+\.md|[\w-]+/[\w-]+\.md):0: \[mien-thua\] (.+?) — mục miễn \((.+?)\) không còn khớp: ngữ cảnh "(.*)" đã đổi', out)
hits = re.findall(r'([\w-]+/[\w-]+\.md):(\d+): \[(?:cum-thoi-gian|nam|[a-z-]+)\] (.+?) — dời', out)
p = "data/style/volatile-allow.yml"; t = open(p).read()
blocks = re.split(r'(?m)^(?=- unit: )', t)
for page, found, reason, ctx in stale:
    idx = [i for i, b in enumerate(blocks) if ctx in b and page in b]
    if not idx: continue
    i = idx[0]
    h = [x for x in hits if x[0] == page and x[2] == found]
    if h:
        line = open("docs/" + page).read().split("\n")[int(h[0][1]) - 1]
        j = line.find(found); new = line[max(0, j-31):j + len(found) + 41]
        blocks[i] = blocks[i].replace(ctx, new); hits.remove(h[0]); print("cập nhật", page, found)
    else:
        blocks[i] = ""; print("bỏ", page, found)
open(p, "w").write("".join(blocks))
