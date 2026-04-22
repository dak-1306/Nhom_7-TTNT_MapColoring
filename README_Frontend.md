# Map Coloring GUI

Đây là bản clean của phần GUI cho đề tài `Map Coloring` 63 tỉnh/thành Việt Nam.

## Chức năng

- Hiển thị bản đồ Việt Nam 63 tỉnh/thành
- Tô màu bản đồ theo output mới nhất của Nhóm 1
- Mô phỏng quá trình tô màu bằng nút `Run`
- Hiển thị ngay nghiệm cuối bằng nút `Hiển thị ngay`
- Hiển thị `Thời gian`, `Số bước`, `Số lần kiểm tra`
- Kiểm tra lại xung đột màu theo `data/adjacency_63.json`

## Cấu trúc chính

- `app.py`: chương trình GUI chính
- `visualization/name_normalizer.py`: chuẩn hóa tên tỉnh
- `data/solution.json`: nghiệm tô màu cuối
- `data/results_63.csv`: số liệu đo thuật toán
- `data/adjacency_63.json`: dữ liệu giáp ranh mới
- `data/colors.json`: bảng màu
- `data/vietnam_provinces.geojson`: dữ liệu hình học bản đồ

## Cách chạy

```bash
python app.py
```

## Ghi chú

- GUI hiện tại chạy độc lập
- GUI đọc output có sẵn của Nhóm 1
- App chưa gọi trực tiếp solver của Nhóm 1 khi bấm `Run`
- Lựa chọn thuật toán dùng để đổi thông số hiển thị từ `results_63.csv`
