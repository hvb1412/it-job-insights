# Hướng dẫn làm việc — IT Job Insights

## Mục tiêu
Xây dựng hệ thống thu thập, làm sạch, phân tích tin tuyển dụng IT và minh họa dự đoán lương. Triển khai tuần tự Lecture 2–8; sản phẩm dự kiến dùng Python, FastAPI, React và TypeScript.

## Đọc trước khi bắt đầu
1. `docs/START_HERE.md` — bối cảnh và cách tiếp nhận công việc.
2. `docs/STATUS.md` — trạng thái thực tế, bằng chứng và công việc tiếp theo.
3. `docs/ROADMAP.md` — phụ thuộc và điều kiện hoàn thành từng Lecture.
4. `docs/TASK_BOARD.md` — người phụ trách, phạm vi và trạng thái nhiệm vụ.
5. `docs/ARCHITECTURE.md`, `docs/DATA_AND_SOURCES.md`, `docs/DECISIONS.md`.

Đây là bộ tài liệu khởi động. Không suy ra rằng code, Git hoặc kiểm thử đã tồn tại chỉ vì chúng được mô tả trong kế hoạch. Đối chiếu workspace và lịch sử Git thực tế trước khi sửa.

## Phạm vi chỉnh sửa
- Chỉ chỉnh sửa trong repository `it-job-insights/` và phạm vi nhiệm vụ đang nhận.
- Không thay đổi thư mục cùng cấp, đặc biệt `it-jobmarket-react/`.
- Không xóa thay đổi của người khác; không reset, force push hoặc sửa lịch sử dùng chung.
- Kiểm tra `git status`, branch và repository root trước khi thao tác Git. Không tự ý stash thay đổi chưa rõ chủ sở hữu.
- Nếu file cần sửa đang được người khác phụ trách, ghi phụ thuộc và thống nhất người tích hợp trước.
- Không commit môi trường ảo, node_modules, cache, thông tin đăng nhập hoặc file tạm.

## Quy trình mỗi nhiệm vụ
1. Đọc hướng dẫn và trạng thái; kiểm tra repo thực tế.
2. Chọn task đã được giao, ghi người nhận và phạm vi file trong TASK_BOARD.
3. Triển khai phần nhỏ có đầu vào, đầu ra và tiêu chí nghiệm thu rõ.
4. Chạy kiểm tra phù hợp. Nếu không chạy được, ghi nguyên nhân và phần chưa xác minh.
5. Rà soát diff; commit các file của nhiệm vụ đã được kiểm tra.
6. Cập nhật STATUS, TASK_BOARD và ghi bàn giao theo mẫu trong START_HERE.

Chỉ làm Lecture đã được giao. Khởi tạo và Lecture trước phải đạt điều kiện cần trước khi bắt đầu Lecture sau. Có thể làm song song tài liệu hoặc thành phần độc lập khi đã chốt hợp đồng dữ liệu; không chạy nhiều tác vụ ghi đè cùng đầu ra.

## Tính chính xác
- Tách rõ kế hoạch, quan sát từ tài liệu và kết quả đã chạy.
- Dữ liệu lịch sử, crawl mới và fixture kiểm thử phải phân biệt được.
- Ghi nguồn dữ liệu, mã hoặc tài sản kế thừa và phạm vi sử dụng trong DATA_AND_SOURCES.
- Không bịa số liệu, kết quả kiểm thử, tác giả, thời gian commit hoặc đóng góp thành viên.
- Không tự chọn danh tính Git; thiếu thông tin thì hỏi người phụ trách. Chỉ cấu hình local khi được cung cấp.
- Không push khi chưa được giao quyền hoặc yêu cầu tương ứng.
- Lecture 8 cần nội dung bài giảng trước khi quyết định công nghệ.

## Định nghĩa hoàn thành
Code đáp ứng tiêu chí task, kiểm tra có bằng chứng, tài liệu phản ánh đúng trạng thái và người tiếp nhận có thể chạy lại. Tên commit nên theo `feat(l3): ...`, `fix(api): ...`, `test(l2): ...`, `docs: ...`; nội dung phải mô tả thay đổi thực tế.
