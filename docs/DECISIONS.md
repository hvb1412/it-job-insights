# Quyết định và vấn đề cần chốt

| ID | Ngày | Quyết định | Lý do / ảnh hưởng |
|---|---|---|---|
| D01 | Kế hoạch ban đầu | Repository làm việc là `it-job-insights` | Cô lập phạm vi chỉnh sửa |
| D02 | Kế hoạch ban đầu | Kiến trúc đích Python + FastAPI + React/TypeScript | Chỉ là đích đối chiếu, chưa phải phần đã chuyển |
| D03 | Kế hoạch ban đầu | Phân biệt raw, cleaned, artifacts và fixture | Bảo đảm truy nguyên và tái lập |
| D04 | 22/11/2026 | Chuyển theo Lecture từ nguồn chỉ đọc | Không viết lại/refactor/đổi tên; commit ghi việc transfer/verify |
| D05 | 22/11/2026 | Dùng SHA-256 cho file copy nguyên vẹn | Phát hiện thay đổi không chủ đích; 15 file L2 đã match |
| D06 | 22/11/2026 | Chuyển `config.py` và `requirements.txt` sớm | Dependency dùng chung của crawler/test, không đánh dấu L3–7 là đã có |
| D07 | 22/11/2026 | Hoãn `cli.py` và raw-contract/cross-stage tests | Chúng chứa/nhập cleaning của L3; tránh đưa code sau scope L2 |
| D08 | 22/11/2026 | Version đúng 5 snapshot raw/log mốc, ignore output mới | Giữ input đối chiếu nhưng tránh commit crawl/derived data chưa có provenance |

## Chưa chốt

- Thành viên, điều phối, reviewer và người tích hợp của nhóm.
- Quyền sử dụng/phân phối đầy đủ và metadata gốc của snapshot kế thừa.
- Phiên bản dữ liệu clean/model/figure nào khớp với code nguồn khi tái chạy.
- API contract chi tiết, giới hạn sample, quality/metrics và frontend integration.
- Nội dung/yêu cầu Lecture 8 và có hay không phần tương ứng trong nguồn.

Không đổi quyết định đã triển khai mà không ghi lý do, dependency và kiểm tra liên
quan. Quyết định không biến dữ liệu có sẵn thành dữ liệu được tạo trong lượt này.
