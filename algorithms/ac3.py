from collections import deque
from typing import Callable, Any


def ac3(csp, queue=None, constraint: Callable[[Any, Any], bool] = None) -> bool:
    """
    Thuật toán AC-3 (Arc Consistency)

    Mục đích:
        Giảm domain của các biến trong CSP bằng cách loại bỏ các giá trị
        không thỏa mãn ràng buộc.

    Input:
        csp:
            - variables: danh sách biến (vd: tỉnh)
            - domains: dict {var: list/set các giá trị}
            - neighbors: dict {var: danh sách biến kề}

        queue (optional):
            danh sách các arc (Xi, Xj). Nếu None → tự khởi tạo

        constraint (optional):
            hàm kiểm tra ràng buộc giữa 2 giá trị
            mặc định: x != y (map coloring)

    Output:
        True  -> còn nghiệm (không domain nào rỗng)
        False -> có domain bị rỗng (fail)
    """

    # Constraint mặc định: khác màu
    if constraint is None:
        constraint = lambda x, y: x != y

    # Validate CSP
    _validate_csp(csp)

    # Khởi tạo queue
    if queue is None:
        queue = deque(
            (Xi, Xj)
            for Xi in csp.variables
            for Xj in csp.neighbors.get(Xi, [])
        )
    else:
        queue = deque(queue)

    # Vòng lặp chính
    while queue:
        Xi, Xj = queue.popleft()

        if revise(csp, Xi, Xj, constraint):
            # Nếu domain rỗng → fail
            if len(csp.domains[Xi]) == 0:
                return False

            # Thêm lại các arc liên quan
            for Xk in csp.neighbors.get(Xi, []):
                if Xk != Xj:
                    queue.append((Xk, Xi))

    return True


def revise(csp, Xi, Xj, constraint: Callable[[Any, Any], bool]) -> bool:
    """
    Làm cho Xi nhất quán với Xj

    Ý tưởng:
        Xóa các giá trị x trong domain(Xi) nếu không tồn tại y trong domain(Xj)
        sao cho constraint(x, y) = True

    Input:
        Xi, Xj: 2 biến
        constraint: hàm ràng buộc

    Output:
        True  -> có thay đổi domain
        False -> không thay đổi
    """

    revised = False
    domain_Xi = csp.domains[Xi]
    domain_Xj = csp.domains[Xj]

    # Duyệt bản sao để tránh lỗi khi xóa
    for x in list(domain_Xi):
        # Kiểm tra có tồn tại y hợp lệ không
        if not any(constraint(x, y) for y in domain_Xj):
            _remove_value(domain_Xi, x)
            revised = True

    return revised


def _remove_value(domain, value):
    """Xóa value khỏi domain (hỗ trợ list/set)"""
    if isinstance(domain, set):
        domain.discard(value)
    else:
        try:
            domain.remove(value)
        except ValueError:
            pass


def _validate_csp(csp):
    """Kiểm tra dữ liệu CSP hợp lệ"""
    for var in csp.variables:
        if var not in csp.domains:
            raise ValueError(f"Variable '{var}' không có domain")

    for var, neighbors in csp.neighbors.items():
        for n in neighbors:
            if n not in csp.variables:
                raise ValueError(f"Neighbor '{n}' không tồn tại trong variables")


from typing import Dict, Any, Optional, Tuple

class AC3Solver:
    """
    Trình giải bài toán tô màu bản đồ sử dụng Backtracking kết hợp với AC-3 (MAC - Maintaining Arc Consistency).
    """
    def solve(self, csp) -> Tuple[Optional[Dict[str, Any]], int, int]:
        from .forward_checking import ForwardCheckingSolver
        solver = ForwardCheckingSolver()
        return solver.solve(csp, mac=True)