# Bắt đầu làm việc — IT Job Insights

## Dự án đang hướng tới điều gì?
Hệ thống hỗ trợ quan sát các tin tuyển dụng IT: nguồn đăng, địa điểm, nhóm nghề, kỹ năng và lương công bố. Phần học máy ước lượng lương để minh họa kiến thức môn học; kết quả phụ thuộc mẫu dữ liệu, không đại diện toàn bộ thị trường.

Sản phẩm đích có năm khu vực: Tổng quan, Phân tích thị trường, Phân tích kỹ năng, Dự đoán lương, Chất lượng dữ liệu. Luồng kỹ thuật: raw → làm sạch → thống kê/biểu đồ → mô hình → API → dashboard.

## Trạng thái ban đầu của bộ tài liệu
Bộ tài liệu được chuẩn bị ngày 22/11/2026. Theo thông tin được cung cấp lúc lập kế hoạch, `it-job-insights/` là thư mục dự án mới. Bộ tài liệu không xác nhận trạng thái hiện tại trên máy thành viên, chưa khởi tạo Git và chưa triển khai pipeline.

## Cách đặt tài liệu
Đặt `AGENTS.md` vào gốc `it-job-insights/`, các file còn lại vào `docs/`. Nếu đã tồn tại file cùng tên, đọc và hợp nhất; không ghi đè tiến độ hoặc hướng dẫn hiện có. Đánh dấu task khởi tạo là hoàn thành chỉ sau khi kiểm tra repository thực tế.

## Quy trình cộng tác
1. Người điều phối điền tên thành viên và người tích hợp trong TASK_BOARD.
2. Thành viên hoặc agent đọc AGENTS và STATUS, nhận một task rõ phạm vi.
3. Dùng branch riêng cho phần việc, ví dụ `feat/l3-salary-cleaning`, nếu nhóm dùng nhiều checkout.
4. Kiểm tra, commit, ghi bàn giao và mở PR nếu repository đã có quy trình review.
5. Người tích hợp review phụ thuộc, chạy kiểm tra liên quan rồi tích hợp theo thứ tự Lecture.

Không nhiều agent cùng sửa một checkout khi chưa phân định phạm vi. Task cùng file hoặc cùng đầu ra cần thực hiện tuần tự. Không giả định tên thành viên hay số người; bảng phân công đang để trống để nhóm xác nhận.

## Lệnh giao việc cho agent tiếp theo
> Đọc AGENTS.md, docs/STATUS.md và docs/TASK_BOARD.md. Kiểm tra workspace thực tế. Thực hiện task [ID] trong phạm vi đã giao; chỉ triển khai giai đoạn hiện tại. Kiểm tra kết quả, commit phần việc của task nếu đã có danh tính Git và cập nhật bàn giao. Không thay đổi file ngoài phạm vi hoặc công việc đang được thành viên khác phụ trách.

## Mẫu bàn giao sau mỗi task
- Task / Lecture:
- Người thực hiện / branch / commit:
- Thay đổi và phạm vi file:
- Đầu vào, đầu ra:
- Lệnh kiểm tra và kết quả thực tế:
- Lỗi, giới hạn hoặc kiểm tra chưa chạy:
- Ảnh hưởng tới task khác / hợp đồng dữ liệu:
- Bước tiếp theo và người tiếp nhận:

Bàn giao phải nằm trong Git cùng phần việc liên quan. Ghi branch và commit triển khai đã có; không tạo vòng commit chỉ để ghi hash của chính commit tài liệu.
