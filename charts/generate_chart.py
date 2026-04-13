"""
Đọc file results.csv và vẽ biểu đồ

Output:
    - time_chart.png
    - steps_chart.png
    - checks_chart.png

Lưu tại: report/images/
"""

import csv
import os
from collections import defaultdict
import matplotlib.pyplot as plt


# =========================
# Đọc dữ liệu từ CSV
# =========================
def load_data(csv_path):
    data = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # convert kiểu dữ liệu
            data.append({
                "algorithm": row["algorithm"],
                "colors": int(row["colors"]),
                "time": float(row["time_avg_s"]),
                "steps": float(row["steps_avg"]),
                "checks": float(row["checks_avg"]),
                "valid": float(row["valid_ratio"]),
            })

    return data


# =========================
# Gom nhóm dữ liệu
# =========================
def group_by_colors(data, metric):
    """
    Trả về:
        {
            2: {Backtracking: value, FC: value, ...},
            3: {...},
            4: {...}
        }
    """
    result = defaultdict(dict)

    for row in data:
        algo = row["algorithm"]
        colors = row["colors"]

        # bỏ AC3 vì không có steps/checks meaningful
        if algo == "AC3":
            continue

        result[colors][algo] = row[metric]

    return result


# =========================
# Vẽ chart
# =========================
def plot_chart(grouped_data, title, ylabel, filename):
    """
    grouped_data:
        {colors: {algorithm: value}}
    """
    colors_list = sorted(grouped_data.keys())
    algorithms = list(next(iter(grouped_data.values())).keys())

    x = range(len(colors_list))

    # width mỗi cột
    width = 0.2

    plt.figure()

    # vẽ từng thuật toán
    for i, algo in enumerate(algorithms):
        values = [grouped_data[c].get(algo, 0) for c in colors_list]
        positions = [p + i * width for p in x]

        plt.bar(positions, values, width=width, label=algo)

    # label trục X
    plt.xticks(
        [p + width for p in x],
        [f"{c} colors" for c in colors_list]
    )

    plt.xlabel("Number of Colors")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()

    # lưu ảnh
    os.makedirs("report/images", exist_ok=True)
    path = os.path.join("report/images", filename)
    plt.savefig(path)

    print(f"Saved: {path}")

    plt.close()


# =========================
# MAIN
# =========================
def main():
    csv_path = "experiments/results/results.csv"

    data = load_data(csv_path)

    # TIME
    time_data = group_by_colors(data, "time")
    plot_chart(
        time_data,
        title="Execution Time Comparison",
        ylabel="Time (seconds)",
        filename="time_chart.png"
    )

    # STEPS
    steps_data = group_by_colors(data, "steps")
    plot_chart(
        steps_data,
        title="Steps Comparison",
        ylabel="Number of Steps",
        filename="steps_chart.png"
    )

    # CHECKS
    checks_data = group_by_colors(data, "checks")
    plot_chart(
        checks_data,
        title="Constraint Checks Comparison",
        ylabel="Number of Checks",
        filename="checks_chart.png"
    )


if __name__ == "__main__":
    main()