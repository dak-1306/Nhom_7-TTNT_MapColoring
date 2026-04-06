# Nhom_7-TTNT_MapColoring

## Thành viên nhóm 7

Nhóm 1:

- Trần Hải Đăng
- Hồ Tấn Đạt
- Trần Hoàng Phương

Nhóm 2:

- Trần Thái Bảo
- Vương Hoàng Lâm
- Nguyễn Hoàng Như

## Cấu trúc thư mục

```
map-coloring-project/
│
├── data/
│   ├── vietnam_provinces.json     # Danh sách tất cả tỉnh/thành (variables của CSP)
│   ├── adjacency.json             # Danh sách tỉnh nào giáp tỉnh nào (constraints)
│   └── colors.json                # Danh sách màu có thể dùng (domain của CSP)
│
├── algorithms/
│   ├── csp.py                     # Định nghĩa CSP model: variables, domain, constraints
│   ├── backtracking.py            # Thuật toán Backtracking để tô màu bản đồ
│   ├── forward_checking.py        # Thuật toán Forward Checking (cải tiến Backtracking)
│   └── ac3.py                     # Thuật toán AC-3 để giảm domain trước khi search
│
├── experiments/
│   ├── run_experiments.py         # Chạy tất cả thuật toán với số màu khác nhau
│   ├── measure_time.py            # Đo thời gian chạy, số bước, số lần check constraint
│   └── results.csv                # Lưu kết quả: algorithm, colors, time, steps
│
├── visualization/
│   ├── vietnam.geojson            # File bản đồ Việt Nam (dữ liệu hình dạng tỉnh)
│   ├── map.js                     # Load bản đồ và hiển thị lên màn hình
│   ├── draw_map.js                # Vẽ bản đồ bằng SVG/Canvas
│   ├── color_map.js               # Tô màu tỉnh theo kết quả thuật toán
│   └── animation.js               # Hiệu ứng tô màu từng bước (animation)
│
├── ui/
│   ├── index.html                 # Giao diện web chính (nút chọn thuật toán, số màu)
│   ├── app.js                     # Xử lý sự kiện UI, gọi thuật toán, hiển thị kết quả
│   └── style.css                  # CSS giao diện
│
├── charts/
│   ├── chart_time.js              # Vẽ biểu đồ thời gian chạy thuật toán
│   ├── chart_comparison.js        # Vẽ biểu đồ so sánh các thuật toán
│   └── generate_chart.py          # Đọc results.csv và tạo dữ liệu cho biểu đồ
│
├── report/
│   ├── report.docx                # Báo cáo cuối cùng
│   └── images/                    # Ảnh biểu đồ, ảnh demo để chèn vào report
│
├── slides/
│   └── presentation.pptx          # Slide thuyết trình
│
├── demo/
│   └── demo_script.txt            # Kịch bản demo khi thuyết trình
│
└── README.md                      # Hướng dẫn chạy project, mô tả cấu trúc project
```

**Cơ bản là thế mọi người có thể tùy chỉnh cho phù hợp**

## Phân chia thư mục theo nhóm

```
                MAP COLORING PROJECT
                        │
        ┌───────────────┴───────────────┐
        │                               │
      NHÓM 1                         NHÓM 2
   (Algorithms)                  (Visualization)
        │                               │
   data/                           visualization/
   algorithms/                     ui/
   experiments/                    charts/
                                   report/

```

**slide/ và demo/ cả 2 nhóm làm chung**

## Luồng dữ liệu giữa 2 nhóm

```
Nhóm 1:
Adjacency + Algorithms
        ↓
Run experiments
        ↓
results.csv
        ↓
-------------------------
        ↓
Nhóm 2:
Read results.csv
        ↓
Draw charts
        ↓
Visualization map
        ↓
Slide + Report + Demo
```
