# Lộ trình chuyển nguyên trạng theo Lecture

Repository này là đích chuyển mã từ `it-jobmarket-react`, không phải nơi viết lại
chức năng tương đương. Các commit phải mô tả phần **đã chuyển và đã kiểm tra**,
không mô tả chúng như lịch sử phát triển gốc.

## Giao thức áp dụng cho mọi giai đoạn

1. Đọc cấu trúc và dependency của nguồn ở chế độ chỉ đọc.
2. Chỉ chuyển file/phần file cần cho Lecture hiện tại; copy nguyên byte khi file
   thuộc duy nhất một giai đoạn.
3. Cho phép đưa dependency dùng chung vào sớm, ghi rõ lý do. Với file nhiều Lecture,
   chỉ chuyển phần liên quan hoặc hoãn toàn bộ file nếu việc tách làm sai hành vi.
4. So SHA-256 cho file nguyên vẹn và chạy kiểm tra không đòi thành phần chưa chuyển.
5. Ghi nguồn dữ liệu, giới hạn chạy và kết quả thực tế vào `STATUS.md`,
   `TASK_BOARD.md` và `DATA_AND_SOURCES.md`; sau đó mới commit.

Không chuyển `.git`, môi trường ảo, `node_modules`, cache hoặc build output. Dữ liệu
raw/fixture/artifact có sẵn phải được mô tả là kế thừa từ nguồn, không phải tạo mới.

## Trạng thái lượt hiện tại

| Giai đoạn | Trạng thái trước khi chuyển | Mốc đối chiếu |
|---|---|---|
| Khởi tạo | IN_PROGRESS | Gốc repo, docs, ignore rules, README và dependency tối thiểu |
| Lecture 2 | TODO | Schema/raw/crawler/fixture/test, dữ liệu raw và log |
| Lecture 3–7 | TODO | Chờ theo thứ tự phụ thuộc |
| Lecture 8 | BLOCKED | Chỉ xác minh phần tương ứng trong nguồn khi đến giai đoạn |
| API/UI/final | TODO | Chờ pipeline Lecture hoàn chỉnh |

## Theo giai đoạn

### Khởi tạo

- Hợp nhất bộ tài liệu vào gốc repo đích; xác định branch, thay đổi có sẵn và Git identity.
- Tạo README, `.gitignore` và dependency để bắt đầu với môi trường mới.
- Ghi rõ nguồn tham chiếu và cách dữ liệu được lưu để đối chiếu lại.

### Lecture 2 — Thu thập và dữ liệu thô

- Chuyển `jobmarket/schema.py`, `jobmarket/crawler.py`, package/config dùng chung,
  fixture, test parser/listing crawler, `seed_urls.txt`, CSV raw tham chiếu và log live.
- Dữ liệu lịch sử 13 cột và live snapshot 18 cột giữ nguyên; không crawl mới.
- `jobmarket/cli.py` và `tests/test_raw_contract.py` được hoãn vì cùng chứa/nhập
  trực tiếp logic cleaning của Lecture 3. Test L2 chỉ được chạy offline/mocked.

### Lecture 3 — Làm sạch và tích hợp

- Chuyển `cleaning.py`, `skills.py`, các phần CLI/test liên quan và dữ liệu/đầu ra cần
  thiết để đối chiếu. Không tạo số liệu thay thế khi output đóng gói khác lần chạy mới.

### Lecture 4–6 — EDA và trực quan hóa

- Phân tích `eda.py` trước khi chia theo Lecture 4, 5 và 6. Các phần được chuyển qua
  nhiều commit phải ghép lại đúng nội dung file nguồn ở cuối Lecture 6.

### Lecture 7 — Modeling

- Chuyển `modeling.py`, test và artifacts cần thiết; phân biệt model đóng gói với model
  sinh trong lần chạy mới.

### Lecture 8

- Kiểm tra nguồn có phần tương ứng hay không. Nếu không có, ghi bằng chứng và dừng;
  không tự viết công nghệ hoặc chức năng mới.

### Hoàn thiện sản phẩm

- Chỉ sau các Lecture, chuyển `backend/`, `frontend/`, tài nguyên cần thiết và test còn
  lại; đối chiếu giao diện/chức năng/cấu trúc với nguồn, không copy build output.
