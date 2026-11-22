# Lộ trình chuyển nguyên trạng theo Lecture

Repository này chuyển mã từ `it-jobmarket-react`, không viết lại chức năng tương
đương. Commit phải mô tả phần **đã chuyển và đã kiểm tra**, không mô tả chúng như
lịch sử phát triển gốc. Với file nhiều Lecture, chỉ chuyển phần phù hợp khi vẫn giữ
hành vi; nếu không an toàn, hoãn file và ghi dependency.

## Trạng thái hiện tại

| Giai đoạn | Trạng thái | Mốc đối chiếu |
|---|---|---|
| Khởi tạo | DONE | `d75492b`: docs/config/README/ignore/dependency |
| Lecture 2 | DONE | 15 file hash-match; 12 test offline/mock pass |
| Lecture 3 | TODO | Chờ chuyển cleaning/skills và test phụ thuộc |
| Lecture 4–7 | TODO | Chờ thứ tự tích hợp |
| Lecture 8 | BLOCKED | Chỉ xác minh nguồn khi đến giai đoạn; không tự bổ sung |
| Backend, frontend, final | TODO | Chờ pipeline Lecture hoàn chỉnh |

## Quy tắc chuyển và nghiệm thu

1. Đọc nguồn chỉ đọc, phạm vi task và dependency trước khi copy.
2. Không chuyển `.git`, `.venv`, `node_modules`, cache hoặc build output.
3. So SHA-256 cho từng file copy nguyên vẹn. Với dữ liệu, kiểm tra header/số bản
   ghi/log và ghi provenance; không sửa để khớp output đã có.
4. Chạy chỉ test có dependency đã chuyển; phần chưa test phải ghi rõ, không suy ra PASS.
5. Cập nhật STATUS, TASK_BOARD, DATA_AND_SOURCES và contract liên quan trước commit.

## Theo giai đoạn

### Khởi tạo — hoàn thành

Đã hợp nhất tài liệu vào gốc repo, kiểm tra Git/branch/trạng thái, thay README,
tạo `.gitignore` có whitelist raw inputs cần version và dùng `requirements.txt`
nguồn nguyên vẹn. Môi trường `.venv` được tạo mới tại đích và bị ignore.

### Lecture 2 — hoàn thành

- Chuyển nguyên vẹn `schema.py`, `crawler.py`, `__init__.py`, `config.py`, fixture,
  parser/listing crawler tests, URL seed và raw datasets/log cần thiết.
- `crawler.py` nhận URL listing/detail hoặc fixture offline, tôn trọng robots khi
  crawl live, rồi ghi record raw 18 cột và JSON log. Không crawl live trong lượt này.
- Historical CSV 13 cột và live snapshot 18 cột được chuyển như input có sẵn;
  provenance/hash ở `DATA_AND_SOURCES.md`.
- Hoãn `cli.py`, raw-contract test và mọi code cleaning vì chúng chứa hoặc nhập L3.

### Lecture 3 — bước kế tiếp

Chuyển nguyên vẹn `jobmarket/cleaning.py`, `jobmarket/skills.py`, các phần
`cli.py`/test cần thiết và output metadata phù hợp. Chạy test cleaning và raw
contract sau khi dependencies đã đủ. Không dùng CSV sạch/model/figure đóng gói để
thay thế kết quả chạy mới.

### Lecture 4–6 — EDA và trực quan hóa

Phân tích `eda.py` trước khi chia L4, L5 và L6. Nếu file phải được chia qua nhiều
commit, nội dung cuối Lecture 6 phải hash-match file nguồn đầy đủ; mở xem figure
thực tế khi phần đó được chuyển.

### Lecture 7 — modeling

Chuyển `modeling.py`, test, artifact cần thiết và contract dự đoán theo nguồn;
phân biệt artifact đóng gói khỏi artifact sinh trong lần chạy mới.

### Lecture 8

Kiểm tra nguồn có phần tương ứng không. Nếu không có, ghi bằng chứng và dừng;
không tự thêm Spark, Dask, dữ liệu nhân tạo hay tính năng mới.

### Hoàn thiện sản phẩm

Sau các Lecture, chuyển backend, frontend, tài nguyên và test còn lại cần để
đối chiếu giao diện/chức năng/cấu trúc với nguồn; không copy `dist` hay dependencies cục bộ.
