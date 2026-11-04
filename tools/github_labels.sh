#!/usr/bin/env bash
# Tạo hoặc cập nhật nhãn GitHub của repo logos (việc 0.7, ban-giao/dot-0.md). Cần gh đã đăng nhập.
#   bash tools/github_labels.sh [owner/repo]     # mặc định mtuann/logos
set -euo pipefail
REPO="${1:-mtuann/logos}"
label() { gh label create "$1" --repo "$REPO" --color "$2" --description "$3" --force; }
label cho       FBCA04 "Việc chờ: lỗi hoặc ý tưởng ngoài phạm vi đợt đang làm"
label doi-loi   B60205 "PR được phép sửa đơn vị Lõi đã đóng băng, kèm bằng chứng mới"
label bao-loi   D93F0B "Báo lỗi từ người đọc (mẫu .github/ISSUE_TEMPLATE/bao-loi.yml)"
label link-hong 5319E7 "Link web hỏng, do kiểm tra link hằng tuần tự mở"
for n in 0 1 2 3 4 5 6 7; do label "dot-$n" 1D76DB "Việc của đợt $n (KE-HOACH.md)"; done
echo "Đã tạo hoặc cập nhật nhãn trên $REPO."
