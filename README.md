# IT Job Insights

IT Job Insights là hệ thống quan sát dữ liệu tuyển dụng IT, tập trung vào nguồn
đăng, địa điểm, kỹ năng, nhóm nghề và thông tin lương công bố. Dự án được tổ
chức theo các Lecture, từ thu thập dữ liệu thô đến làm sạch, phân tích, mô hình
dự đoán và dashboard.

## Phạm vi hiện tại

Lecture 2 cung cấp hợp đồng dữ liệu raw, parser/crawler, fixture offline, URL
seed và các snapshot raw có phiên bản. Crawler ưu tiên JSON-LD `JobPosting`,
giữ các trường thiếu ở trạng thái rỗng và ghi kết quả theo schema 18 cột.

Chi tiết tiến độ, hợp đồng dữ liệu và hướng dẫn bàn giao nằm trong `docs/`.

## Thiết lập

Cần Python tương thích với `requirements.txt`.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Kiểm thử Lecture 2

Chạy parser/crawler với fixture và request mocked, không truy cập các website
tuyển dụng thật:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_crawler.py tests/test_listing_crawler.py -q
```

## Dữ liệu raw

Các snapshot raw được lưu có phiên bản trong `data/raw/`; output crawler mới,
dữ liệu trung gian, dữ liệu đã xử lý và artifacts được ignore mặc định. Chỉ chạy
crawler trực tuyến khi đã xác nhận quyền truy cập và điều khoản của từng nguồn.
