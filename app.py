from __future__ import annotations

import csv
import json
import math
import tkinter as tk
import unicodedata
from pathlib import Path
from tkinter import ttk

from visualization.name_normalizer import canonical_province_name


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data"
EXPERIMENTS_PATH = ROOT / "experiments" / "results"

GEOJSON_PATH = DATA_PATH / "vietnam_provinces.geojson"
SOLUTION_PATH = EXPERIMENTS_PATH / "solution_63.json"
RESULTS_PATH = EXPERIMENTS_PATH / "results_63.csv"
ADJACENCY_PATH = DATA_PATH / "adjacency_63.json"
COLORS_PATH = DATA_PATH / "colors.json"

APP_BG = "#F6F1E6"
SIDEBAR_BG = "#ECE2CE"
CARD_BG = "#FFFCF7"
NAVY = "#1F3A5F"
TEXT = "#16263A"
MUTED = "#6C5731"
BORDER = "#D9CFBB"
CANVAS_BG = "#F8F4EC"
UNASSIGNED = "#D8D6D0"

ALGORITHMS = ["AC-3", "Forward Checking"]
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 760
REMOTE_ISLAND_MIN_LON = 111.5

FALLBACK_COLOR_MAP = {
    "Do": "#FF0000",
    "Xanh": "#0000FF",
    "Vang": "#FFFF00",
    "Tim": "#800080",
    "Chua to": UNASSIGNED,
}

COLOR_ALIASES = {
    "do": "Do",
    "red": "Do",
    "xanh": "Xanh",
    "blue": "Xanh",
    "vang": "Vang",
    "yellow": "Vang",
    "tim": "Tim",
    "purple": "Tim",
    "chua to": "Chua to",
    "unassigned": "Chua to",
}

COLOR_LABELS = {
    "Do": "Đỏ",
    "Xanh": "Xanh",
    "Vang": "Vàng",
    "Tim": "Tím",
    "Chua to": "Chưa tô",
}

ALGORITHM_NAME_MAP = {
    "AC3": "AC-3",
    "AC-3": "AC-3",
    "ForwardChecking": "Forward Checking",
    "Forward Checking": "Forward Checking",
    "ForwardChecking_MAC": "Forward Checking (MAC)",
    "Backtracking": "Backtracking",
}


def normalize_color_label(color: str | None) -> str:
    if not color:
        return "Chua to"

    lowered = unicodedata.normalize("NFD", str(color))
    lowered = "".join(ch for ch in lowered if unicodedata.category(ch) != "Mn")
    lowered = (
        lowered.lower()
        .replace("đ", "d")
        .replace("ä‘", "d")
        .replace("ð", "d")
        .replace("-", " ")
        .replace(".", " ")
    )
    lowered = " ".join(lowered.split())
    return COLOR_ALIASES.get(lowered, "Chua to")


def normalize_algorithm_name(name: str) -> str:
    return ALGORITHM_NAME_MAP.get(name, name)


def load_color_values(path: Path) -> dict[str, str]:
    color_values = dict(FALLBACK_COLOR_MAP)
    if not path.exists():
        return color_values

    payload = json.loads(path.read_text(encoding="utf-8"))
    for color_name, color_hex in payload.items():
        color_values[normalize_color_label(color_name)] = color_hex
    color_values["Chua to"] = UNASSIGNED
    return color_values


COLOR_VALUE_MAP = load_color_values(COLORS_PATH)


def load_solution_data(path: Path) -> dict:
    # Try to load from specified path, fallback to data/solution.json if not found
    if not path.exists():
        fallback_path = Path(__file__).resolve().parent / "data" / "solution.json"
        if fallback_path.exists():
            path = fallback_path
        else:
            raise FileNotFoundError(f"Solution file not found at {path} or {fallback_path}")
    
    payload = json.loads(path.read_text(encoding="utf-8"))
    assignment_raw = payload.get("solution", {})
    assignment = {
        canonical_province_name(province): normalize_color_label(color)
        for province, color in assignment_raw.items()
    }
    display_names = {
        canonical_province_name(province): province
        for province in assignment_raw.keys()
    }
    return {
        "assignment": assignment,
        "sequence": [canonical_province_name(name) for name in assignment_raw.keys()],
        "display_names": display_names,
        "meta": {
            "time": float(payload.get("meta", {}).get("time", 0.0)),
            "steps": int(payload.get("meta", {}).get("steps", 0)),
            "checks": int(payload.get("meta", {}).get("checks", 0)),
        },
    }


def load_results(path: Path) -> list[dict]:
    # Try to load from specified path, fallback to data/results_63.csv if not found
    if not path.exists():
        fallback_path = Path(__file__).resolve().parent / "data" / "results_63.csv"
        if fallback_path.exists():
            path = fallback_path
        else:
            raise FileNotFoundError(f"Results file not found at {path} or {fallback_path}")
    
    rows: list[dict] = []
    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(
                {
                    "algorithm": normalize_algorithm_name(row.get("algorithm", "")),
                    "colors": int(float(row.get("colors", "0") or 0)),
                    "time": float(row.get("time_avg_s", "0") or 0.0),
                    "steps": int(float(row.get("steps_avg", "0") or 0)),
                    "checks": int(float(row.get("checks_avg", "0") or 0)),
                    "valid_ratio": float(row.get("valid_ratio", "0") or 0.0),
                }
            )
    return rows


def load_adjacency(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}

    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        canonical_province_name(province): [canonical_province_name(neighbor) for neighbor in neighbors]
        for province, neighbors in payload.items()
    }


def validate_assignment(assignment: dict[str, str], adjacency: dict[str, list[str]]) -> list[tuple[str, str, str]]:
    conflicts: list[tuple[str, str, str]] = []
    seen_pairs: set[tuple[str, str]] = set()

    for province, neighbors in adjacency.items():
        province_color = assignment.get(province, "Chua to")
        if province_color == "Chua to":
            continue

        for neighbor in neighbors:
            pair = tuple(sorted((province, neighbor)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            neighbor_color = assignment.get(neighbor, "Chua to")
            if province_color == neighbor_color and province_color != "Chua to":
                conflicts.append((province, neighbor, province_color))

    return conflicts


def simplify_ring(ring: list[list[float]], target_points: int = 90) -> list[tuple[float, float]]:
    if len(ring) <= target_points:
        return [(point[0], point[1]) for point in ring]

    step = max(1, len(ring) // target_points)
    simplified = [(point[0], point[1]) for point in ring[::step]]
    if simplified[0] != simplified[-1]:
        simplified.append(simplified[0])
    return simplified


def load_geojson_shapes(path: Path) -> tuple[dict[str, list[list[tuple[float, float]]]], tuple[float, float, float, float]]:
    geojson = json.loads(path.read_text(encoding="utf-8"))
    province_shapes: dict[str, list[list[tuple[float, float]]]] = {}
    min_x = math.inf
    min_y = math.inf
    max_x = -math.inf
    max_y = -math.inf

    for feature in geojson.get("features", []):
        properties = feature.get("properties", {})
        geometry = feature.get("geometry", {})
        province_name = canonical_province_name(properties.get("ten_tinh", ""))
        geometry_type = geometry.get("type")
        coordinates = geometry.get("coordinates", [])
        rings: list[list[tuple[float, float]]] = []

        polygons = coordinates if geometry_type == "MultiPolygon" else [coordinates]
        for polygon in polygons:
            if not polygon:
                continue

            ring = simplify_ring(polygon[0])
            if len(ring) < 3:
                continue

            xs = [point[0] for point in ring]
            ys = [point[1] for point in ring]
            if min(xs) >= REMOTE_ISLAND_MIN_LON:
                continue

            rings.append(ring)
            for lon, lat in ring:
                min_x = min(min_x, lon)
                max_x = max(max_x, lon)
                min_y = min(min_y, lat)
                max_y = max(max_y, lat)

        province_shapes[province_name] = rings

    return province_shapes, (min_x, min_y, max_x, max_y)


def find_result_row(results: list[dict], algorithm: str, color_count: int) -> dict | None:
    for row in results:
        if row["algorithm"] == algorithm and row["colors"] == color_count:
            return row
    return None


def format_time_value(value: float) -> str:
    if value < 0.01:
        return f"{value * 1000:.2f} ms"
    return f"{value:.2f} s"


class VietnamMapCanvas(tk.Canvas):
    def __init__(self, master, province_shapes: dict[str, list[list[tuple[float, float]]]], bounds, **kwargs):
        super().__init__(master, **kwargs)
        self.province_shapes = province_shapes
        self.bounds = bounds
        self.province_items: dict[str, list[int]] = {}
        self.current_assignment: dict[str, str] = {}
        self.current_highlight: str | None = None
        self.bind("<Configure>", self._on_resize)
        self.draw_map()

    def _on_resize(self, _event) -> None:
        self.draw_map()
        self.apply_assignment(self.current_assignment, self.current_highlight)

    def project(self, lon: float, lat: float) -> tuple[float, float]:
        min_x, min_y, max_x, max_y = self.bounds
        pad = 20
        canvas_width = max(self.winfo_width(), 480)
        canvas_height = max(self.winfo_height(), 480)
        width = canvas_width - pad * 2
        height = canvas_height - pad * 2
        scale_x = width / max(max_x - min_x, 1e-9)
        scale_y = height / max(max_y - min_y, 1e-9)
        scale = min(scale_x, scale_y)

        map_width = (max_x - min_x) * scale
        map_height = (max_y - min_y) * scale
        offset_x = pad + (width - map_width) / 2
        offset_y = pad + (height - map_height) / 2

        x = offset_x + (lon - min_x) * scale
        y = offset_y + (max_y - lat) * scale
        return x, y

    def draw_map(self) -> None:
        self.delete("all")
        self.province_items.clear()
        for province, rings in self.province_shapes.items():
            items: list[int] = []
            for ring in rings:
                points: list[float] = []
                for lon, lat in ring:
                    x, y = self.project(lon, lat)
                    points.extend([x, y])

                item_id = self.create_polygon(
                    points,
                    fill=UNASSIGNED,
                    outline="#FFFDF7",
                    width=1.0,
                    smooth=False,
                )
                items.append(item_id)
            self.province_items[province] = items

    def apply_assignment(self, assignment: dict[str, str], highlight: str | None = None) -> None:
        self.current_assignment = assignment.copy()
        self.current_highlight = highlight
        highlight_key = canonical_province_name(highlight) if highlight else None

        for province, items in self.province_items.items():
            color_label = assignment.get(province, "Chua to")
            fill_color = COLOR_VALUE_MAP.get(color_label, UNASSIGNED)
            is_highlighted = province == highlight_key
            for item_id in items:
                self.itemconfig(
                    item_id,
                    fill=fill_color,
                    outline=NAVY if is_highlighted else "#FFFDF7",
                    width=2.4 if is_highlighted else 1.0,
                )


class MapColoringApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Map Coloring Vietnam")
        self.root.geometry("1420x900")
        self.root.minsize(1260, 800)
        self.root.configure(bg=APP_BG)

        self.solution_data = load_solution_data(SOLUTION_PATH)
        self.results = load_results(RESULTS_PATH)
        self.adjacency = load_adjacency(ADJACENCY_PATH)
        self.conflicts = validate_assignment(self.solution_data["assignment"], self.adjacency)
        self.province_shapes, self.bounds = load_geojson_shapes(GEOJSON_PATH)

        self.solution_color_count = len(
            {color for color in self.solution_data["assignment"].values() if color != "Chua to"}
        )
        self.algorithm_var = tk.StringVar(value="Forward Checking")
        self.animate_var = tk.BooleanVar(value=True)
        self.time_var = tk.StringVar(value="N/A")
        self.steps_var = tk.StringVar(value="N/A")
        self.checks_var = tk.StringVar(value="N/A")
        self.status_var = tk.StringVar(value="Bấm Run để mô phỏng quá trình tô màu.")
        self.info_var = tk.StringVar(value="")

        self.animation_job: str | None = None
        self.sequence = list(self.solution_data["sequence"])
        self.display_names = dict(self.solution_data["display_names"])
        self.used_colors = [
            color for color in ["Do", "Xanh", "Vang", "Tim"]
            if color in set(self.solution_data["assignment"].values())
        ]
        self.sequence_index = 0

        self._setup_style()
        self._build_ui()
        self.refresh_dashboard()

    def _setup_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=APP_BG)
        style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
        style.configure("Card.TFrame", background=CARD_BG, relief="flat")
        style.configure("TLabel", background=APP_BG, foreground=TEXT, font=("Times New Roman", 12))
        style.configure("Sidebar.TLabel", background=SIDEBAR_BG, foreground=TEXT, font=("Times New Roman", 12))
        style.configure("Title.TLabel", background=APP_BG, foreground=NAVY, font=("Times New Roman", 28, "bold"))
        style.configure("Subtitle.TLabel", background=APP_BG, foreground=TEXT, font=("Times New Roman", 14))
        style.configure("Section.TLabel", background=APP_BG, foreground=NAVY, font=("Times New Roman", 19, "bold"))
        style.configure("SidebarTitle.TLabel", background=SIDEBAR_BG, foreground=NAVY, font=("Times New Roman", 18, "bold"))
        style.configure("CardTitle.TLabel", background=CARD_BG, foreground=MUTED, font=("Times New Roman", 12))
        style.configure("CardValue.TLabel", background=CARD_BG, foreground=NAVY, font=("Times New Roman", 19, "bold"))
        style.configure("TButton", font=("Times New Roman", 12, "bold"))

    def _build_metric_card(self, master, title: str, variable: tk.StringVar) -> ttk.Frame:
        frame = ttk.Frame(master, style="Card.TFrame", padding=(16, 14))
        ttk.Label(frame, text=title, style="CardTitle.TLabel").pack(anchor="w")
        ttk.Label(frame, textvariable=variable, style="CardValue.TLabel").pack(anchor="w", pady=(6, 0))
        return frame

    def _build_ui(self) -> None:
        sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", padding=(18, 22))
        sidebar.pack(side="left", fill="y")

        ttk.Label(sidebar, text="Điều khiển", style="SidebarTitle.TLabel").pack(anchor="w")
        ttk.Label(
            sidebar,
            text="GUI này dùng để trực quan hóa output mới nhất của Nhóm 1.",
            style="Sidebar.TLabel",
            wraplength=220,
            justify="left",
        ).pack(anchor="w", pady=(8, 18))

        ttk.Label(sidebar, text="Thuật toán", style="Sidebar.TLabel").pack(anchor="w")
        algorithm_box = ttk.Combobox(sidebar, textvariable=self.algorithm_var, values=ALGORITHMS, state="readonly", width=20)
        algorithm_box.pack(anchor="w", fill="x", pady=(6, 14))
        algorithm_box.bind("<<ComboboxSelected>>", lambda _event: self.refresh_dashboard())

        ttk.Label(sidebar, text="Số màu của nghiệm hiện có", style="Sidebar.TLabel").pack(anchor="w")
        ttk.Label(
            sidebar,
            text=f"{self.solution_color_count} màu",
            style="Sidebar.TLabel",
        ).pack(anchor="w", pady=(6, 14))

        tk.Checkbutton(
            sidebar,
            text="Animation tô màu",
            variable=self.animate_var,
            bg=SIDEBAR_BG,
            fg=TEXT,
            activebackground=SIDEBAR_BG,
            activeforeground=TEXT,
            selectcolor=CARD_BG,
            font=("Times New Roman", 12),
            relief="flat",
            highlightthickness=0,
            bd=0,
        ).pack(anchor="w", pady=(4, 18))

        ttk.Button(sidebar, text="Run", command=self.run_demo).pack(fill="x", pady=(0, 14))
        ttk.Button(sidebar, text="Hiển thị ngay", command=self.show_full_solution).pack(fill="x")

        ttk.Label(
            sidebar,
            text=(
                "Nguồn dữ liệu:\n"
                "- data/solution.json\n"
                "- data/results_63.csv\n"
                "- data/adjacency_63.json\n"
                "- data/colors.json\n"
                "- data/vietnam_provinces.geojson"
            ),
            style="Sidebar.TLabel",
            justify="left",
            wraplength=220,
        ).pack(anchor="w", pady=(24, 0))

        content = ttk.Frame(self.root, padding=(18, 18, 18, 18))
        content.pack(side="left", fill="both", expand=True)

        ttk.Label(content, text="Map Coloring Vietnam", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            content,
            text="Bản desktop bằng tkinter để demo kết quả tô màu bản đồ 63 tỉnh/thành Việt Nam.",
            style="Subtitle.TLabel",
            wraplength=980,
        ).pack(anchor="w", pady=(6, 16))

        metrics = ttk.Frame(content)
        metrics.pack(fill="x", pady=(0, 14))
        self._build_metric_card(metrics, "Thời gian", self.time_var).pack(side="left", fill="x", expand=True, padx=(0, 10))
        self._build_metric_card(metrics, "Số bước", self.steps_var).pack(side="left", fill="x", expand=True, padx=5)
        self._build_metric_card(metrics, "Số lần kiểm tra", self.checks_var).pack(side="left", fill="x", expand=True, padx=(10, 0))

        body = ttk.Frame(content)
        body.pack(fill="both", expand=True)

        map_frame = ttk.Frame(body)
        map_frame.pack(side="left", fill="both", expand=True)
        ttk.Label(map_frame, text="Bản đồ tô màu", style="Section.TLabel").pack(anchor="w")
        ttk.Label(
            map_frame,
            text=f"Bản đồ hiển thị nghiệm {self.solution_color_count} màu hiện có trong solution.json của Nhóm 1.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 10))

        self.map_canvas = VietnamMapCanvas(
            map_frame,
            self.province_shapes,
            self.bounds,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=CANVAS_BG,
            highlightthickness=1,
            highlightbackground=BORDER,
        )
        self.map_canvas.pack(fill="both", expand=True)

        side_panel = ttk.Frame(body)
        side_panel.pack(side="left", fill="y", padx=(18, 0))
        ttk.Label(side_panel, text="Thông tin dữ liệu", style="Section.TLabel").pack(anchor="w")

        self.status_label = tk.Label(
            side_panel,
            textvariable=self.status_var,
            justify="left",
            wraplength=280,
            bg=CARD_BG,
            fg=TEXT,
            font=("Times New Roman", 12),
            bd=1,
            relief="solid",
            padx=14,
            pady=12,
        )
        self.status_label.pack(fill="x", pady=(8, 16))

        legend_frame = ttk.Frame(side_panel, style="Card.TFrame", padding=(12, 10))
        legend_frame.pack(fill="x", pady=(0, 16))
        ttk.Label(legend_frame, text="Bảng màu", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))

        legend_order = [color for color in self.used_colors]
        legend_order.append("Chua to")
        for color_key in legend_order:
            row = ttk.Frame(legend_frame, style="Card.TFrame")
            row.pack(anchor="w", fill="x", pady=1)
            swatch = tk.Canvas(row, width=18, height=18, bg=CARD_BG, highlightthickness=0)
            swatch.pack(side="left")
            swatch.create_rectangle(
                1,
                1,
                17,
                17,
                fill=COLOR_VALUE_MAP[color_key],
                outline=COLOR_VALUE_MAP[color_key],
            )
            ttk.Label(row, text=COLOR_LABELS[color_key], style="CardTitle.TLabel").pack(side="left", padx=(8, 0))

        note_frame = ttk.Frame(side_panel, style="Card.TFrame", padding=(12, 10))
        note_frame.pack(fill="x")
        ttk.Label(note_frame, text="Ghi chú", style="CardTitle.TLabel").pack(anchor="w", pady=(0, 6))
        ttk.Label(
            note_frame,
            textvariable=self.info_var,
            style="Subtitle.TLabel",
            wraplength=300,
            justify="left",
        ).pack(anchor="w")

    def refresh_dashboard(self) -> None:
        selected_row = find_result_row(self.results, self.algorithm_var.get(), self.solution_color_count)
        if selected_row is None:
            self.time_var.set("N/A")
            self.steps_var.set("N/A")
            self.checks_var.set("N/A")
            self.status_var.set("Không có thông số phù hợp trong results_63.csv cho lựa chọn hiện tại.")
        else:
            self.time_var.set(format_time_value(selected_row["time"]))
            self.steps_var.set(f"{selected_row['steps']:,}")
            self.checks_var.set(f"{selected_row['checks']:,}")
            self.status_var.set("Bấm Run để mô phỏng quá trình tô màu.")

        if self.conflicts:
            conflict_message = f"Cảnh báo: còn {len(self.conflicts)} cặp tỉnh giáp nhau trùng màu theo adjacency_63.json."
        else:
            conflict_message = "Kiểm tra theo adjacency_63.json: không có tỉnh giáp nhau trùng màu."

        self.info_var.set(
            f"Thuật toán đang chọn: {self.algorithm_var.get()}\n"
            f"Thông số ở trên lấy từ results_63.csv của Nhóm 1 với nghiệm {self.solution_color_count} màu.\n"
            f"{conflict_message}\n"
            "Map đang hiển thị nghiệm cuối từ solution.json; lựa chọn thuật toán dùng để đổi thông số đo."
        )
        self.clear_map()

    def clear_map(self) -> None:
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.map_canvas.apply_assignment({})

    def show_full_solution(self) -> None:
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.map_canvas.apply_assignment(self.solution_data["assignment"])
        self.status_var.set("Đã hiển thị ngay nghiệm tô màu hiện có.")

    def run_demo(self) -> None:
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None

        if not self.animate_var.get():
            self.show_full_solution()
            return

        self.clear_map()
        self.sequence_index = 0
        self.status_var.set("Đang mô phỏng quá trình tô màu trên bản đồ.")
        self._animate_step()

    def _animate_step(self) -> None:
        if self.sequence_index >= len(self.sequence):
            self.map_canvas.apply_assignment(self.solution_data["assignment"])
            self.status_var.set("Đã hiển thị xong kết quả tô màu.")
            self.animation_job = None
            return

        province = self.sequence[self.sequence_index]
        partial_assignment = {
            key: self.solution_data["assignment"][key]
            for key in self.sequence[: self.sequence_index + 1]
            if key in self.solution_data["assignment"]
        }
        self.map_canvas.apply_assignment(partial_assignment, highlight=province)
        display_name = self.display_names.get(province, province)
        self.status_var.set(f"Đang xét: {display_name}")

        self.sequence_index += 1
        self.animation_job = self.root.after(140, self._animate_step)


def main() -> None:
    root = tk.Tk()
    MapColoringApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
