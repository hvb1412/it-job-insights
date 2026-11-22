# Kiến trúc và hợp đồng dự kiến

Tài liệu mô tả đích triển khai. Đối chiếu repo trước khi coi một thành phần là đã có.

## Thành phần
| Thành phần | Trách nhiệm | Đầu ra / nơi lưu dự kiến |
|---|---|---|
| jobmarket/schema.py | Schema dữ liệu thô | Danh sách trường dùng chung |
| jobmarket/crawler.py | Parser và thu thập | data/raw, log |
| jobmarket/cleaning.py, skills.py | Chuẩn hóa và tích hợp | data/interim, data/processed |
| jobmarket/eda.py | Bảng thống kê và biểu đồ | reports/tables, reports/figures |
| jobmarket/modeling.py | Train, đánh giá và inference | reports/artifacts |
| jobmarket/cli.py | Điều phối tác vụ theo giai đoạn | Lệnh CLI |
| backend/main.py | API dashboard và dự đoán | HTTP JSON |
| frontend/ | Năm trang React | Giao diện trình duyệt |
| tests/ | Kiểm thử hành vi và hợp đồng | Kết quả kiểm tra |

Luồng: dữ liệu thô → cleaning → dữ liệu sạch → EDA/biểu đồ và training → artifacts → FastAPI → React. UI không trực tiếp huấn luyện mô hình. Mỗi giai đoạn chỉ nhập những module đã triển khai.

## Hợp đồng dữ liệu
Schema raw và quy tắc biến đổi nằm trong DATA_AND_SOURCES. Thay tên, kiểu hoặc đơn vị phải ghi DECISIONS và thông báo task phụ thuộc. Không sửa âm thầm CSV để làm biểu đồ đẹp hoặc tăng điểm mô hình.

## API dự kiến
| Endpoint | Vai trò | Đầu vào / đầu ra chính |
|---|---|---|
| GET /api/options | Lấy lựa chọn bộ lọc/form | source, location, category, job_type, skills |
| GET /api/dashboard | Thống kê theo bộ lọc | Lọc nhiều source/location; total, salary_count, sources_count, median; bảng nguồn, địa điểm, cấp bậc, nhóm nghề, tháng, kỹ năng, lương; sample, quality, metrics |
| POST /api/predict | Ước lượng lương | location, job_level, category, job_type, experience_years, skills → salary |
| GET /figures/{filename} | Hình phân tích | File ảnh được phép phục vụ |

Lương trả về dự kiến theo triệu VND/tháng, trong phạm vi dữ liệu được xác minh. Bộ lọc không chọn mục nào phải có ý nghĩa rõ ràng; thống nhất với UI trước khi triển khai. Quy tắc ban đầu: không chọn mục nào trả tập rỗng, thiếu tham số trả tất cả.

Trước API-01, bổ sung JSON mẫu, kiểu trường, ý nghĩa null, mã lỗi, cách phân trang/giới hạn sample và việc quality/metrics thuộc toàn bộ lần chạy hay tập lọc. Không để UI suy diễn phạm vi từ nhãn.

## Kiểm tra tích hợp tối thiểu
- Tổng số tin và số nhãn lương khớp CSV đang dùng.
- Bộ lọc một/nhiều/không mục có kết quả đúng.
- Không có lương hợp lệ trả null phù hợp, không tạo số trung bình giả.
- Form dự đoán dùng cùng thứ tự và ý nghĩa đặc trưng với mô hình.
- Thiếu artifact hoặc mất API hiển thị thông báo có thể hiểu được.
