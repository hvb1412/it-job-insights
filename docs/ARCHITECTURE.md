# Kiến trúc và phạm vi chuyển

Tài liệu này phân biệt thành phần đã chuyển với kiến trúc đích trong nguồn. Một
thành phần chỉ được coi là có khi đã xuất hiện trong repository này và được ghi
trạng thái thực tế.

## Thành phần hiện có — Lecture 2

| Thành phần | Trạng thái | Vai trò / dependency |
|---|---|---|
| `jobmarket/schema.py` | Đã chuyển nguyên vẹn | Hợp đồng 18 trường raw dùng chung |
| `jobmarket/config.py` | Đã chuyển nguyên vẹn | Đường dẫn raw/live/interim/processed/reports; crawler import trực tiếp |
| `jobmarket/crawler.py` | Đã chuyển nguyên vẹn | Parser JSON-LD/HTML, listing/pagination, robots, offline crawl và lưu raw/log |
| `tests/test_crawler.py` | Đã chuyển nguyên vẹn | Parser + fixture offline |
| `tests/test_listing_crawler.py` | Đã chuyển nguyên vẹn | Listing/pagination/crawler với request mocked |
| `data/raw/**`, `seed_urls.txt` | Đã chuyển nguyên vẹn | Input raw có sẵn và URL seed, không phải output lần chạy này |

`config.py` có định nghĩa đường dẫn của giai đoạn sau do đó có thư mục rỗng xuất
hiện khi import; điều này không có nghĩa cleaning, EDA hay model tồn tại.

## Luồng dữ liệu Lecture 2

```text
data/seed_urls.txt ──► crawl_urls (robots + listing/detail HTML)
                                 │
fixture HTML ─────────► parse_job_html ─► record COLUMNS (18 trường)
                                 │
                         save_crawl ─► data/raw/live/<mode>_<UTC>.csv
                                              + <mode>_<UTC>_log.json

reference_2026/*.csv (13 cột, dữ liệu lịch sử có sẵn) ─► giữ nguyên cho Lecture 3
live_20261117T150738Z.csv (18 cột, crawl có sẵn) ─────► giữ nguyên, không crawl lại
```

`crawl_urls` chỉ dành cho URL được phép truy cập; thao tác live chưa chạy ở đây.
`crawl_offline_html` chỉ phục vụ fixture test, và timestamp của fixture không phải
bằng chứng crawl Internet.

## Thành phần chưa chuyển

| Thành phần nguồn | Giai đoạn dự kiến | Lý do chưa có |
|---|---|---|
| `cleaning.py`, `skills.py`, phần `cli.py` | L3 | Phụ thuộc làm sạch/tích hợp |
| `eda.py`, `reporting.py` | L4–6 | Chứa EDA/figure nhiều Lecture |
| `modeling.py` | L7 | Phụ thuộc cleaned data và artifacts |
| `backend/`, `frontend/` | Sau L7 | Phụ thuộc pipeline/API contract |

API endpoints và React dashboard mô tả trong nguồn vẫn chỉ là kiến trúc đích; không
được xem là endpoint/UI đang hoạt động cho tới khi các file tương ứng được chuyển và test.
