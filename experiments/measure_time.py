"""
Module đo hiệu năng cho các thuật toán CSP.

Chức năng:
- Chạy solver nhiều lần (repeats)
- Đo thời gian, số bước, số lần check constraint
- Kiểm tra nghiệm có hợp lệ không
"""

from copy import deepcopy
import time
import statistics
from typing import Callable, Dict, Any, Tuple, List


def verify_solution(csp, assignment) -> Tuple[bool, str]:
    """
    Kiểm tra nghiệm có hợp lệ không

    Output:
        (True, "OK") nếu đúng
        (False, message) nếu sai
    """
    if assignment is None:
        return False, "No solution"

    # Kiểm tra đủ biến
    if set(assignment.keys()) != set(csp.variables):
        return False, "Incomplete assignment"

    # Kiểm tra constraint
    for var, val in assignment.items():
        for n in csp.get_neighbors(var):
            if n in assignment:
                if not csp.constraint(var, val, n, assignment[n]):
                    return False, f"Constraint violated: {var} - {n}"

    return True, "OK"


def run_solver_once(
    solver_callable: Callable[[Any], Tuple[Any, int, int]],
    csp
) -> Dict[str, Any]:
    """
    Chạy solver 1 lần

    Input:
        solver_callable: hàm solve
        csp: bài toán CSP

    Output:
        dict chứa:
            time, steps, checks, valid, message
    """
    csp_copy = deepcopy(csp)

    t0 = time.perf_counter()
    solution, steps, checks = solver_callable(csp_copy)
    t1 = time.perf_counter()

    valid, msg = verify_solution(csp_copy, solution)

    return {
        "time": t1 - t0,
        "steps": steps,
        "checks": checks,
        "valid": valid,
        "message": msg,
    }


def measure_solver(
    csp,
    solver_callable: Callable[[Any], Tuple[Any, int, int]],
    repeats: int = 3
) -> Dict[str, Any]:
    """
    Chạy solver nhiều lần và tính thống kê

    Output:
        time_avg, min, max
        steps_avg
        checks_avg
        valid_ratio
    """
    times: List[float] = []
    steps_list: List[int] = []
    checks_list: List[int] = []
    valids: List[bool] = []

    for _ in range(max(1, repeats)):
        res = run_solver_once(solver_callable, csp)

        times.append(res["time"])
        steps_list.append(res["steps"])
        checks_list.append(res["checks"])
        valids.append(res["valid"])

    return {
        "time_avg": statistics.mean(times),
        "time_min": min(times),
        "time_max": max(times),

        "steps_avg": statistics.mean(steps_list),
        "steps_min": min(steps_list),
        "steps_max": max(steps_list),

        "checks_avg": statistics.mean(checks_list),
        "checks_min": min(checks_list),
        "checks_max": max(checks_list),

        "valid_ratio": sum(valids) / len(valids),
    }