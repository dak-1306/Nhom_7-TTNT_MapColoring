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
from algorithms.forward_checking import ForwardCheckingSolver
from algorithms.ac3 import AC3Solver


def run_solver(solver_class, csp):
    solver = solver_class()
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
        provinces_file=str(data / "vietnam_regions_34.json"),
        adjacency_file=str(data / "adjacency_34.json"),
        colors_file=str(data / "colors.json"),
    )

    print("Running CSP solvers for 34 regions...")

    solvers = {
        "Backtracking": BacktrackingSolver,
        "Forward Checking": ForwardCheckingSolver,
        "AC-3": AC3Solver
    }

    results_meta = {}
    best_solution = None

    for name, solver_class in solvers.items():
        print(f"Running {name}...")
        csp_copy = deepcopy(csp)
        result = run_solver(solver_class, csp_copy)

        results_meta[name] = {
            "time": result["time"],
            "steps": result["steps"],
            "checks": result["checks"]
        }

        # Keep the first valid solution for frontend rendering
        if best_solution is None:
            best_solution = result["solution"]

        print(f"  -> Time: {result['time']:.4f}s, Steps: {result['steps']}, Checks: {result['checks']}")

    # Save JSON for frontend
    out_path = ROOT / "experiments" / "results" / "solution_34.json"
    out_path.parent.mkdir(exist_ok=True)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump({
            "solution": best_solution,
            "meta": results_meta
        }, f, ensure_ascii=False, indent=2)

    print(f"Saved aggregated solution to: {out_path}")


if __name__ == "__main__":
    main()