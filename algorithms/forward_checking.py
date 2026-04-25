"""Module đơn giản: Forward Checking cho CSP.

Mô tả ngắn gọn:
- Đây là trình giải Backtracking kết hợp "Forward-Checking" (lọc miền của
  các biến chưa gán sau mỗi gán) và tuỳ chọn MAC (sử dụng AC-3 để duy trì
  nhất quán cung đoạn). Dùng để giảm không gian tìm kiếm so với Backtracking
  thuần túy.

Lớp chính: `ForwardCheckingSolver` với phương thức `solve(csp, mac=False)`.
"""

from typing import Dict, Any, Optional, Tuple
from copy import deepcopy

from .ac3 import ac3


# Trình giải: Backtracking + Forward Checking (tùy chọn MAC via AC-3)
class ForwardCheckingSolver:
    """Gói hàm giải CSP:
    - `solve(csp, mac=False)`: chạy forward-checking
    - `mac=True` để bật MAC (AC-3) thay vì chỉ forward-checking
    """

    def __init__(self) -> None:
        # Bộ đếm thống kê cho một lần chạy
        self.steps: int = 0
        self.constraint_checks: int = 0

    def _is_consistent(self, csp, var: str, value: Any, assignment: Dict[str, Any]) -> bool:
        # Kiểm tra nhanh tính nhất quán của (var=value) với các láng giềng đã gán
        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                self.constraint_checks += 1
                if not csp.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def _forward_check(self, csp, var: str, value: Any) -> bool:
        # Forward-checking: loại những giá trị trong miền của láng giềng không tương thích
        # Trả về False nếu một miền bị rỗng sau khi lọc
        for neighbor in csp.get_neighbors(var):
            domain = csp.domains[neighbor]
            for val in list(domain):
                self.constraint_checks += 1
                if not csp.constraint(neighbor, val, var, value):
                    try:
                        domain.remove(val)
                    except ValueError:
                        pass
            if len(domain) == 0:
                return False
        return True

    def backtrack(self, csp, assignment: Dict[str, Any], mac: bool) -> Optional[Dict[str, Any]]:
        # Đệ quy Backtracking với bước forward-checking hoặc MAC
        if csp.is_complete(assignment):
            return assignment.copy()

        var = csp.get_unassigned_variables(assignment)[0]

        for value in list(csp.get_domain(var)):
            self.steps += 1
            if not self._is_consistent(csp, var, value, assignment):
                continue

            # Lưu miền hiện tại để có thể khôi phục khi backtrack
            domains_backup = {v: list(vals) for v, vals in csp.domains.items()}

            # Gán tạm và chạy forward-checking hoặc MAC
            csp.assign(var, value, assignment)

            ok = True
            if mac:
                # MAC: đặt miền của var là giá trị đã chọn và chạy AC-3 khởi tạo
                csp.domains[var] = [value]
                queue = [(Xk, var) for Xk in csp.get_neighbors(var)]
                ok = ac3(csp, queue=queue)
            else:
                # Chỉ forward-checking
                ok = self._forward_check(csp, var, value)

            if ok:
                result = self.backtrack(csp, assignment, mac)
                if result is not None:
                    return result

            # Khôi phục trạng thái nếu thất bại
            csp.unassign(var, assignment)
            csp.domains = {v: list(vals) for v, vals in domains_backup.items()}

        return None

    def solve(self, csp, mac: bool = False) -> Tuple[Optional[Dict[str, Any]], int, int]:
        # Reset bộ đếm và bắt đầu backtracking
        self.steps = 0
        self.constraint_checks = 0

        solution = self.backtrack(csp, {}, mac)
        return solution, self.steps, self.constraint_checks
