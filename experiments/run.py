from pathlib import Path
import sys
import time
from copy import deepcopy
import json

# Setup path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from algorithms.csp import create_map_coloring_csp
from algorithms.backtracking import BacktrackingSolver


def run_backtracking(csp):
    solver = BacktrackingSolver()
    start = time.perf_counter()
    solution, steps, checks = solver.solve(csp)
    elapsed = time.perf_counter() - start

    return {
        "solution": solution,
        "time": elapsed,
        "steps": steps,
        "checks": checks
    }


def main():
    data = ROOT / "data"

    csp = create_map_coloring_csp(
        provinces_file=str(data / "vietnam_provinces.json"),
        adjacency_file=str(data / "adjacency.json"),
        colors_file=str(data / "colors.json"),
    )

    print("Running CSP solver...")

    csp_copy = deepcopy(csp)
    result = run_backtracking(csp_copy)

    solution = result["solution"]

    # Save JSON for frontend
    out_path = ROOT / "experiments" / "results" / "solution.json"
    out_path.parent.mkdir(exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "solution": solution,
            "meta": {
                "time": result["time"],
                "steps": result["steps"],
                "checks": result["checks"]
            }
        }, f, ensure_ascii=False, indent=2)

    print(f"Saved solution to: {out_path}")


if __name__ == "__main__":
    main()