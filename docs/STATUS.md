# Trạng thái và bàn giao

Cập nhật thực tế: 22/11/2026 (Asia/Saigon). Tài liệu này phân biệt trạng thái
quan sát được với kế hoạch chuyển mã; không coi một file trong dự án tham chiếu
là kết quả do repository này tự phát triển.

## Mốc đã xác minh trước khi chuyển

| Hạng mục | Trạng thái | Bằng chứng thực tế |
|---|---|---|
| Repository đích | Đã xác minh | Git root là `it-job-insights/`; branch hiện tại `vuong` |
| Nội dung đã tracked ban đầu | Đã xác minh | Chỉ có `README.md`; chưa có mã pipeline, test hay dữ liệu |
| Thay đổi có sẵn | Đã bảo toàn | Gói tài liệu khởi động là untracked; đã đặt `AGENTS.md` và `docs/` vào gốc repo |
| Repository tham chiếu | Đã khảo sát, chỉ đọc | `../it-jobmarket-react/it-jobmarket-react/`; không có `.git` ở thư mục nguồn được cung cấp |
| Danh tính Git | Đã phát hiện | Có cấu hình Git hiện có; không thay đổi cấu hình danh tính |
| Python hệ thống | Đã kiểm tra | Python 3.13.2; `bs4` chưa có trong môi trường hệ thống, nên chưa dùng nó để xác nhận test |
| INIT-01 | Đang thực hiện | Đang hoàn thiện cấu trúc, ignore rules, README và môi trường tối thiểu |
| Lecture 2 | Chưa chuyển | Đã xác định phạm vi nguồn và dependency; chưa chép file vào commit |
| Lecture 3–8, API, UI | Chưa chuyển | Không thuộc lượt hiện tại |

## Ràng buộc đang áp dụng

- Chỉ đọc `it-jobmarket-react/`; không sửa, chạy crawler live hay dùng lại `.venv` của nguồn.
- Chỉ ghi trong `it-job-insights/`; không copy `.git`, `.venv`, `node_modules`, cache hay build output.
- File chuyển nguyên trạng được đối chiếu SHA-256. File nhiều Lecture chỉ được chuyển phần
  đúng giai đoạn hoặc để lại cho giai đoạn sau.
- Snapshot kế thừa và live snapshot có sẵn phải được ghi là dữ liệu đã tồn tại trước lần chuyển.

## Bàn giao tạm thời

- Task / Lecture: INIT-01 đang thực hiện; đã khảo sát đầy đủ phạm vi Lecture 2.
- Người thực hiện / branch: Codex (agent) / `vuong`; dùng cấu hình Git hiện có, không tự đặt danh tính.
- Bước tiếp theo: hoàn tất khởi tạo, chuyển và đối chiếu các file Lecture 2, chạy test offline, rồi cập nhật trạng thái cuối.
