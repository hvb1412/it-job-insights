# Phân công và bảng nhiệm vụ

Nguồn tham chiếu là `../it-jobmarket-react/it-jobmarket-react/` và chỉ được đọc.
Trạng thái nói về việc chuyển/đối chiếu vào repository đích, không phải lịch sử
phát triển gốc. Trạng thái dùng: TODO, IN_PROGRESS, BLOCKED, REVIEW, DONE.

Người điều phối: chưa điền. Người tích hợp: chưa điền. Danh sách thành viên: nhóm bổ sung.

| ID | Nhiệm vụ | Phụ thuộc | Phụ trách | Trạng thái | Phạm vi chính / bằng chứng |
|---|---|---|---|---|---|
| INIT-01 | Kiểm tra repo, hợp nhất tài liệu, cấu hình và môi trường tối thiểu | — | Codex (agent) | DONE | Commit `d75492b`; README, docs, ignore rules, dependency và `.venv` mới |
| L2-01 | Chuyển schema, nguồn raw và cách nhập snapshot | INIT-01 | Codex (agent) | DONE | Schema, seed, 4 historical CSV, 1 live CSV/log; hash trùng nguồn |
| L2-02 | Chuyển parser/crawler, fixture, log và kiểm thử offline | L2-01 | Codex (agent) | DONE | Crawler/config/package, fixture và 12 test offline/mock pass |
| L3-01 | Chuyển gộp nguồn và chuẩn hóa dữ liệu | L2-01, L2-02 | Chưa nhận | TODO | `cleaning.py`, `skills.py`, phần CLI/test L3 |
| L3-02 | Chuyển loại trùng, chất lượng, kiểm thử và xuất CSV | L3-01 | Chưa nhận | TODO | cleaning, quality, test |
| L4-01 | Chuyển thống kê và nhận xét EDA | L3-02 | Chưa nhận | TODO | phần L4 của `eda.py`, bảng |
| L5-01 | Chuyển biểu đồ cơ bản | L4-01 | Chưa nhận | TODO | phần L5 của `eda.py`, figures |
| L6-01 | Chuyển biểu đồ nhiều biến | L5-01 | Chưa nhận | TODO | phần L6 của `eda.py`, figures |
| L7-01 | Chuyển đặc trưng và chia train/test | L6-01 | Chưa nhận | TODO | modeling, test |
| L7-02 | Chuyển baseline, mô hình, đánh giá và dự đoán | L7-01 | Chưa nhận | TODO | modeling, artifacts |
| L8-01 | Kiểm tra phần Lecture 8 tương ứng trong nguồn | Bài giảng, L7-02 | Chưa nhận | BLOCKED | Không tự bổ sung nếu nguồn không có |
| API-01 | Chuyển contract/API FastAPI sau các Lecture | L7-02 | Chưa nhận | TODO | backend, api contract |
| UI-01 | Chuyển dashboard React và tích hợp | API-01 | Chưa nhận | TODO | frontend |
| FINAL-01 | Đối chiếu đầy đủ với nguồn và hướng dẫn tái lập | UI-01, giải quyết L8-01 | Chưa nhận | TODO | docs, integration |

L3 không được bắt đầu trong lượt này. Người nhận L3 phải kiểm tra `git status`,
hash source và scope trước khi thêm file.
