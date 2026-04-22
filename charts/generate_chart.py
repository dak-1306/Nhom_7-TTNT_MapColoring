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
    csv_path_63 = "experiments/results/results_63.csv"
    csv_path_34 = "experiments/results/results_34.csv"

    data_63 = load_data(csv_path_63)
    data_34 = load_data(csv_path_34)

    # TIME
    time_data_34 = group_by_colors(data_34, "time")
    plot_chart(
        time_data_34,
        title="Execution Time Comparison (34 provinces)",
        ylabel="Time (seconds)",
        filename="time_chart_34.png"
    )

    time_data_63 = group_by_colors(data_63, "time")
    plot_chart(
        time_data_63,
        title="Execution Time Comparison (63 provinces)",
        ylabel="Time (seconds)",
        filename="time_chart_63.png"
    )

    # STEPS
    steps_data_34 = group_by_colors(data_34, "steps")
    plot_chart(
        steps_data_34,
        title="Steps Comparison (34 provinces)",
        ylabel="Number of Steps",
        filename="steps_chart_34.png"
    )

    steps_data_63 = group_by_colors(data_63, "steps")
    plot_chart(
        steps_data_63,
        title="Steps Comparison (63 provinces)",
        ylabel="Number of Steps",
        filename="steps_chart_63.png"
    )

    # CHECKS
    checks_data_34 = group_by_colors(data_34, "checks")
    plot_chart(
        checks_data_34,
        title="Constraint Checks Comparison (34 provinces)",
        ylabel="Number of Checks",
        filename="checks_chart_34.png"
    )

    checks_data_63 = group_by_colors(data_63, "checks")
    plot_chart(
        checks_data_63,
        title="Constraint Checks Comparison (63 provinces)",
        ylabel="Number of Checks",
        filename="checks_chart_63.png"
    )


if __name__ == "__main__":
    main()