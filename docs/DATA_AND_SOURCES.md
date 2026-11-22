# Dữ liệu, phiên bản và nguồn

## Nguyên tắc
Ghi đúng dữ liệu, mã, tài sản hoặc phương pháp được kế thừa. Tách nguồn dữ liệu khỏi đóng góp triển khai của thành viên. Chưa xác minh quyền sử dụng hoặc metadata thì đánh dấu chờ xác nhận, không tự ghi “nhóm tự thu thập” hoặc “đã được cho phép”.

## Thông tin đã quan sát khi lập kế hoạch
Các số dưới đây được đọc từ gói tài liệu/mã nguồn được cung cấp để khảo sát, không phải đầu ra mới của IT Job Insights.

| Bộ dữ liệu / artifact | Số lượng quan sát | Cách diễn giải |
|---|---:|---|
| Snapshot CareerViet | 950 dòng | CSV lịch sử có sẵn |
| Snapshot ITviec | 823 dòng | CSV lịch sử có sẵn |
| Snapshot LinkedIn | 743 dòng | CSV lịch sử có sẵn |
| Snapshot TopCV | 3.323 dòng | CSV lịch sử có sẵn |
| Tổng bốn snapshot | 5.839 dòng | Tổng đầu vào lịch sử |
| CSV live_20261117T150738Z | 1.090 dòng | File crawl có sẵn; chưa phải crawl của lần triển khai mới |
| CSV sạch đóng gói | 2.946 dòng | Đầu ra sẵn có; không mặc định khớp code cleaning hiện tại |

Tài liệu khảo sát có ghi nguồn snapshot kế thừa Nhóm 14. Nhóm cần xác nhận mô tả nguồn gốc, quyền sử dụng và cách trích dẫn trước khi phân phối hoặc nộp. Các kết quả chất lượng và mô hình đóng gói có thể thuộc phiên bản quy tắc cũ; dùng chúng như thông tin khảo sát, không ghi làm kết quả mới.

## Sổ nguồn cần hoàn thiện
| Đối tượng | Nguồn/tác giả | Phiên bản/checksum | Phạm vi sử dụng | Trạng thái |
|---|---|---|---|---|
| Snapshot lịch sử | Theo metadata/tài liệu được cung cấp, cần xác nhận | Chưa ghi | Dự kiến phân tích và huấn luyện | Chờ xác nhận |
| CSV crawl có sẵn | Theo log đi kèm, cần kiểm tra | Chưa ghi | Chưa chốt gộp cùng lịch sử | Chờ xác nhận |
| Mã/thành phần tái sử dụng | Điền nguồn thực tế khi đưa vào repo | Commit hoặc phiên bản thực tế | Ghi file/phần kế thừa và sửa đổi | Chưa kiểm kê |
| Fixture offline | Người tạo fixture phải được ghi | Theo Git | Chỉ kiểm thử | Chưa nhập |

## Schema raw đích
18 trường: job_title, company_name, location, salary_min, salary_max, salary_currency, experience_required, skills, job_type, job_level, posted_date, source, job_description, url, salary_raw, salary_period, experience_raw, crawled_at.

Snapshot cũ được quan sát chỉ có 13 trường đầu đến job_description. Nhập dữ liệu phải bổ sung trường thiếu bằng giá trị rỗng và ghi file gốc; không tạo URL hoặc thời điểm crawl giả.

## Quy tắc xử lý dự kiến
- Thiếu tiêu đề/công ty: loại và đếm rõ.
- Nhận diện vị trí IT bằng quy tắc: công bố giới hạn, kiểm tra tay mẫu phù hợp.
- Địa điểm, kinh nghiệm, cấp bậc, ngày đăng: chuẩn hóa và giữ khả năng truy nguyên raw.
- Không tự quy đổi USD nếu thiếu tỷ giá có nguồn và ngày áp dụng.
- Lương có kỳ ghi rõ không phải tháng không làm nhãn lương tháng nếu chưa có quy tắc chuyển đổi được chấp nhận.
- Chu kỳ lương không rõ phải ghi là chưa xác minh; không tự coi chắc chắn theo tháng.
- Chỉ tính midpoint khi có hai cận hợp lệ; không điền lương thiếu bằng trung bình để huấn luyện.
- Fixture offline không đi vào dữ liệu nghiên cứu.
- Lưu raw bất biến; mọi biến đổi thực hiện bằng code có phiên bản.

## Bằng chứng mỗi lần chạy
Ghi input/checksum, nguồn, thời gian thực thi, code commit, dependencies, tham số, số raw/clean/loại, artifacts và giới hạn. Không gộp dữ liệu live vào lịch sử mặc định khi chưa ghi rõ phạm vi và kiểm tra trùng.

## Lưu dữ liệu cho người nhận
Nhóm chọn lưu snapshot được phép trong Git hoặc nơi chia sẻ có phiên bản/checksum và hướng dẫn lấy. Nếu .gitignore bỏ CSV, README phải có cách nhận đúng input. Không commit môi trường ảo hoặc mô hình nhị phân không rõ nguồn; mô hình phục vụ nên được tái tạo từ pipeline đã kiểm tra.
