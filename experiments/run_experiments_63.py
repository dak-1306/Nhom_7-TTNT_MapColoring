"""
Chạy experiments cho Map Coloring CSP

Tính năng:
- So sánh nhiều thuật toán
- Test nhiều số màu (2, 3, 4)
- Xuất CSV
"""

from pathlib import Path
import sys
import argparse
import csv
from pprint import pprint
from copy import deepcopy
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from algorithms.csp import create_map_coloring_csp
from algorithms.backtracking import BacktrackingSolver
from algorithms.forward_checking import ForwardCheckingSolver
from algorithms.ac3 import ac3

from experiments.measure_time import measure_solver


# =========================
# Solver wrappers
# =========================
def backtracking(csp):
    return BacktrackingSolver().solve(csp)


def forward_checking(mac=False):
    def _run(csp):
        return ForwardCheckingSolver().solve(csp, mac=mac)
    return _run


# =========================
# AC3 đo riêng
# =========================
def measure_ac3(csp):
    csp_copy = deepcopy(csp)

    t0 = time.perf_counter()
    ok = ac3(csp_copy)
    t1 = time.perf_counter()

    domain_sizes = [len(csp_copy.domains[v]) for v in csp_copy.variables]

    return {
        "algorithm": "AC3",
        "time_avg_s": t1 - t0,
        "steps_avg": 0,
        "checks_avg": 0,
        "valid_ratio": 1.0 if ok else 0.0,
        "ac3_min_domain": min(domain_sizes),
        "ac3_max_domain": max(domain_sizes),
    }


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--out", type=str, default=str(ROOT / "experiments" / "results" / "results_63.csv"))
    args = parser.parse_args()

    # Test nhiều số màu
    color_configs = [2, 3, 4]

    algorithms = [
        ("Backtracking", backtracking),
        ("ForwardChecking", forward_checking(False)),
        ("ForwardChecking_MAC", forward_checking(True)),
    ]

    rows = []

    for num_colors in color_configs:
        print(f"\n===== COLORS = {num_colors} =====")

        # Tạo CSP (từ file dữ liệu) và giới hạn số màu trong domains
        csp = create_map_coloring_csp()

        # Trim domains to the requested number of colors (if necessary)
        try:
            sample_var = csp.variables[0]
            full_domain = list(csp.get_domain(sample_var))
            if len(full_domain) > num_colors:
                for v in csp.variables:
                    # preserve list type
                    csp.domains[v] = list(csp.get_domain(v))[:num_colors]
        except Exception:
            # If anything unexpected happens, continue with the original CSP
            pass

        for name, solver in algorithms:
            print(f"Running {name}...")

            stats = measure_solver(csp, solver, repeats=args.repeats)

            row = {
                "algorithm": name,
                "colors": num_colors,
                "time_avg_s": stats["time_avg"],
                "steps_avg": stats["steps_avg"],
                "checks_avg": stats["checks_avg"],
                "valid_ratio": stats["valid_ratio"],
            }

            pprint(row)
            rows.append(row)

        # AC3 riêng
        ac3_row = measure_ac3(csp)
        ac3_row["colors"] = num_colors

        pprint(ac3_row)
        rows.append(ac3_row)

    # =========================
    # Ghi CSV
    # =========================
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = sorted({k for r in rows for k in r.keys()})

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nSaved to: {out_path}")


if __name__ == "__main__":
    main()