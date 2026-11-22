# Dữ liệu, phiên bản và nguồn

## Nguyên tắc provenance

Tất cả dữ liệu ở đây được chuyển nguyên trạng từ
`../it-jobmarket-react/it-jobmarket-react/` ngày 22/11/2026. Việc chuyển không
phải là crawl mới hay tạo dataset mới. Dự án nguồn tự mô tả snapshot lịch sử là
kế thừa từ “Nhóm 14”; quyền sử dụng, cách thu thập ban đầu và quyền phân phối chưa
được xác minh độc lập, nên không được diễn giải mạnh hơn thông tin đó.

## Snapshot đã chuyển và đối chiếu

| File đích | Loại / schema | Bản ghi logic | SHA-256 |
|---|---|---:|---|
| `data/raw/reference_2026/careerviet_historical_raw.csv` | Historical, 13 cột | 950 | `28B88B414C6600E85D1E8165A92B04CAB4D43116BB0707DCAA22CB2456532754` |
| `data/raw/reference_2026/itviec_historical_raw.csv` | Historical, 13 cột | 823 | `78A71847B1F843BD29ADC343E44B917C44ACFBFDA22DBB54B3BA34434CDFA65E` |
| `data/raw/reference_2026/linkedin_historical_raw.csv` | Historical, 13 cột | 743 | `F31542CAC6396692BC7841D5C1C9C401C784751C48DF34BC424B19FF3134E4B7` |
| `data/raw/reference_2026/topcv_historical_raw.csv` | Historical, 13 cột | 3.323 | `F7BE3A7F26CEDA79DAAA1B24A99653007B9A129D6BCC161172021AC4C5EBC77D` |
| `data/raw/live/live_20261117T150738Z.csv` | Existing live crawl, 18 cột | 1.090 | `8F713C4C6492706A8E3CBB56B6A90CAB539EBCB8E6305529B355450966A1939F` |
| `data/raw/live/live_20261117T150738Z_log.json` | Log của snapshot live | — | `8840A39B9BB0C591B342F8B59841AFCE0D2A81A3392EF689DFC831E70A0999BC` |

Số bản ghi là số CSV logical (không phải số dòng vật lý, vì mô tả công việc có
thể chứa xuống dòng). Hash của tất cả file trên đã so trực tiếp với nguồn và trùng.
Một số mô tả trong CSV nguồn có khoảng trắng cuối dòng; chúng được giữ nguyên thay
vì dọn định dạng, để file tiếp tục byte-identical với nguồn.

Log live được giữ nguyên byte, kể cả trường `file` trỏ tới đường dẫn gốc `F:\\...`.
Đường dẫn đó là bằng chứng lịch sử của nguồn, **không** phải vị trí hiện tại của
file trong repository đích.

## Hợp đồng dữ liệu raw

`jobmarket.schema.COLUMNS` có 18 trường theo thứ tự:

`job_title`, `company_name`, `location`, `salary_min`, `salary_max`,
`salary_currency`, `experience_required`, `skills`, `job_type`, `job_level`,
`posted_date`, `source`, `job_description`, `url`, `salary_raw`, `salary_period`,
`experience_raw`, `crawled_at`.

Snapshot historical chỉ có 13 trường đầu đến `job_description`. Lecture 3 phải
đọc chúng như dữ liệu legacy và bổ sung giá trị thiếu trong bộ nhớ/code; không sửa
CSV raw hay bịa `url`/`crawled_at`. Live snapshot đã có đủ 18 trường.

## Tạo raw output trong code nguồn đã chuyển

- `seed_urls.txt` cung cấp URL listing ban đầu. `crawl_urls` kiểm tra robots.txt,
  tìm link detail, lấy HTML, parse JSON-LD `JobPosting` trước rồi fallback HTML.
- `parse_job_html` chỉ trả record khi có title và company; trường thiếu là `None`,
  ghi CSV thành ô rỗng. Lương không rõ hoặc chu kỳ không phải tháng không tự quy đổi.
- `save_crawl` ghi CSV 18 cột và log JSON timestamp UTC vào `data/raw/live/`.
  Các output mới mặc định bị `.gitignore` bỏ qua để không nhầm với snapshot mốc.
- Fixture offline chỉ dùng để test parser; không đi vào dữ liệu nghiên cứu. Không có
  crawl mạng nào được thực hiện trong lượt này.

## Lưu dữ liệu và output sau này

Bốn historical CSV, một live snapshot và log là input mốc được version trong Git
nhờ whitelist tường minh. `data/interim/`, `data/processed/`, report/artifact và
live output mới bị ignore cho tới khi nhóm chốt provenance/chủ đích version. Không
commit môi trường ảo, mô hình nhị phân không rõ nguồn hoặc cache.
