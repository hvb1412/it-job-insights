# Bắt đầu làm việc — IT Job Insights

## Mục tiêu và cách làm

Repository này là đích chuyển từng giai đoạn từ dự án tham chiếu
`../it-jobmarket-react/it-jobmarket-react/`. Dự án tham chiếu chỉ đọc; các
commit tại đây ghi nhận việc sao chép và đối chiếu, không phải lịch sử phát
triển gốc. Không viết lại, đổi tên, refactor hoặc bổ sung hành vi của file
được chuyển.

Luồng sản phẩm đích vẫn là raw → cleaning → thống kê/biểu đồ → mô hình → API →
dashboard, nhưng chỉ thành phần của Lecture đã hoàn thành mới được coi là có.

## Trạng thái đã xác nhận

- Git root đích là `it-job-insights/`, branch đang dùng là `vuong`.
- Commit `d75492b` đã đặt tài liệu, ignore rules, README và dependency chung.
- Lecture 2 đã được chuyển và kiểm tra offline; chi tiết hash, data provenance
  và lệnh kiểm tra nằm ở `STATUS.md` và `DATA_AND_SOURCES.md`.
- Chưa chuyển Lecture 3, các phần EDA/modeling, backend hoặc frontend.

## Quy trình cho task kế tiếp

1. Đọc `AGENTS.md`, `STATUS.md`, `TASK_BOARD.md`, `ROADMAP.md` và tài liệu dữ liệu.
2. Kiểm tra Git root, branch, `git status` và nguồn tham chiếu trước khi sửa.
3. Chọn đúng Lecture hiện tại; đưa dependency dùng chung vào sớm chỉ khi cần và
   ghi lý do. File nhiều Lecture có thể hoãn thay vì cắt gây sai hành vi.
4. Copy file nguồn nguyên byte khi có thể, so SHA-256 và chỉ chạy test không cần
   thành phần chưa chuyển. Không dùng `.venv`, cache hay build của nguồn.
5. Cập nhật `STATUS.md`, `TASK_BOARD.md`, `DATA_AND_SOURCES.md` và tài liệu liên
   quan theo kết quả thực tế, review diff rồi commit bằng Git identity đã có.

## Mẫu bàn giao

- Task / Lecture:
- Người thực hiện / branch / commit:
- File chuyển nguyên vẹn; file chuyển một phần hoặc hoãn:
- Nguồn, input, output và SHA-256 đối chiếu:
- Lệnh kiểm tra và kết quả thực tế:
- Lỗi, giới hạn hoặc kiểm tra chưa chạy:
- Ảnh hưởng tới task khác / hợp đồng dữ liệu:
- Bước tiếp theo và người tiếp nhận:
