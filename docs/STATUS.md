# Trạng thái và bàn giao

Cập nhật thực tế: 22/11/2026 (Asia/Saigon). Mọi trạng thái dưới đây là kết quả
quan sát/chuyển vào repository đích, không phải tuyên bố về lịch sử phát triển
ở dự án tham chiếu.

## Trạng thái tổng quan

| Hạng mục | Trạng thái | Bằng chứng thực tế |
|---|---|---|
| Git root / branch | Đã xác minh | `it-job-insights/`, branch `vuong` |
| Phạm vi nguồn | Đã khóa chỉ đọc | `../it-jobmarket-react/it-jobmarket-react/`; không sửa file nguồn |
| Khởi tạo | DONE | Commit `d75492b`; README, `.gitignore`, `AGENTS.md`, docs và `requirements.txt` |
| Lecture 2 — schema/raw | DONE | `schema.py`, raw snapshots, `seed_urls.txt`, metadata nguồn |
| Lecture 2 — crawler/test | DONE | `crawler.py`, config/package, fixture và 2 test offline/mock |
| Đối chiếu nguyên vẹn L2 | PASS | SHA-256 của 15/15 file được chuyển trùng nguồn |
| Môi trường test | PASS | `.venv` mới với Python 3.13.2 và dependency từ `requirements.txt` |
| Test L2 | PASS | `12 passed in 0.37s` với parser, fixture, listing và crawler mocked |
| Lecture 3–8, API, UI | Chưa chuyển | Không thuộc lượt này |

## Kiểm tra đã chạy

| Lệnh / kiểm tra | Kết quả |
|---|---|
| `git diff --no-index -- requirements.txt ../it-jobmarket-react/it-jobmarket-react/requirements.txt` | Không có diff |
| SHA-256 15 file L2 | Tất cả `Match=True`, gồm code, test, fixture, seed, 5 CSV/log |
| `git check-ignore` với 4 CSV lịch sử, CSV/live log mốc | Không bị ignore; `.venv/probe` và `.pytest_cache/probe` bị ignore |
| `python -m venv .venv` | Tạo môi trường đích mới, không dùng `.venv` của nguồn |
| `.\\.venv\\Scripts\\python.exe -m pip install -r requirements.txt` | Hoàn tất sau khi quyền tải dependency được cấp |
| `.\\.venv\\Scripts\\python.exe -m pytest tests/test_crawler.py tests/test_listing_crawler.py -q` | `12 passed in 0.37s` |
| `git -c core.whitespace=cr-at-eol diff --cached --check` | Các file code/docs sạch; raw CSV báo các khoảng trắng cuối dòng vốn có và được giữ nguyên để bảo toàn hash |

Không chạy crawler trực tuyến. Test crawler dùng fixture, HTML/mock session; không tạo
CSV crawl mới. `.venv` và `.pytest_cache` là local/ignored, không nằm trong commit.

## Phạm vi Lecture 2 đã chuyển

Nguyên vẹn từ nguồn: `requirements.txt`; `jobmarket/__init__.py`, `config.py`,
`schema.py`, `crawler.py`; `tests/test_crawler.py`, `tests/test_listing_crawler.py`,
`tests/fixtures/example_jobposting.html`; `data/seed_urls.txt`; bốn CSV historical;
`live_20261117T150738Z.csv` và log cùng tên.

`config.py` tạo cả đường dẫn cho các giai đoạn sau nhưng được chuyển sớm vì
`crawler.py` import trực tiếp nó. `requirements.txt` cũng được chuyển sớm như
dependency dùng chung; việc đó không đồng nghĩa cleaning/EDA/modeling đã được chuyển.

## Chưa chuyển và giới hạn

- `jobmarket/cli.py` chứa lệnh `clean`, `eda`, `train`, `report` và import cleaning;
  để lại cho Lecture 3 trở đi thay vì chép trước code sau giai đoạn hiện tại.
- `tests/test_raw_contract.py` và `tests/test_more.py` nhập `jobmarket.cleaning`;
  chưa chạy/chưa chuyển. Các test cleaning/modeling và mọi EDA/backend/frontend cũng chưa chạy.
- Bốn CSV lịch sử chỉ có 13 cột; live snapshot có 18 cột. Không tạo cột, sửa số liệu
  hoặc chạy cleaning để làm chúng trùng output đóng gói.
- Quyền sử dụng/phân phối dataset và mô tả “Nhóm 14” chỉ là thông tin tự mô tả từ
  nguồn, chưa được xác minh độc lập.

## Bàn giao

- Task / Lecture: INIT-01, L2-01 và L2-02 hoàn thành trong lượt này.
- Người thực hiện / branch: Codex (agent) / `vuong`; dùng Git identity đã cấu hình,
  không tự thay đổi danh tính.
- Đầu vào / đầu ra: URL seed hoặc HTML fixture → parser/crawler → record theo schema
  18 cột → CSV/log raw; snapshot historical được giữ nguyên làm input kế thừa.
- Bước tiếp theo: Lecture 3 chuyển `cleaning.py`, `skills.py` cùng test/CLI phần liên
  quan, rồi chạy các test cleaning/raw contract; người nhận chưa được chỉ định.
