# GUI Submission

Đây là danh sách file cần dùng để nộp phần GUI của Nhóm 2.

## File cần giữ

### Code

- `app.py`
- `visualization/name_normalizer.py`
- `visualization/__init__.py`

### Dữ liệu

- `data/solution.json`
- `data/results_63.csv`
- `data/adjacency_63.json`
- `data/colors.json`
- `data/vietnam_provinces.geojson`

### Tài liệu

- `README.md`
- `requirements.txt`
- `GUI_SUBMISSION.md`
- `.gitignore`

## File chính để chạy

- `app.py`

Chạy bằng:

```bash
python app.py
```

## GUI hiện tại làm được gì

- Hiển thị bản đồ Việt Nam 63 tỉnh/thành
- Tô màu theo dữ liệu mới nhất của Nhóm 1
- Mô phỏng tô màu dần bằng nút `Run`
- Hiển thị ngay nghiệm cuối
- Đổi giữa `AC-3` và `Forward Checking` để xem số liệu tương ứng
- Kiểm tra xung đột màu theo `adjacency_63.json`

## Trạng thái

- Đây là bản clean để up GitHub
- Không chứa mockup
- Không chứa file thử nghiệm cũ
- Không chứa `__pycache__`

## Checklist trước khi up

- Chạy `python app.py`
- Kiểm tra map hiển thị đủ
- Kiểm tra `Run`
- Kiểm tra `Hiển thị ngay`
- Kiểm tra số liệu đổi theo thuật toán
