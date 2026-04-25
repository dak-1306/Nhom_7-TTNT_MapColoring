from typing import Dict, Any, Optional, Tuple


# Trình giải Backtracking cho CSP
# - Đếm `steps`: số lần thử giá trị cho các biến
# - Đếm `constraint_checks`: số lần kiểm tra ràng buộc giữa biến và láng giềng
# Cung cấp các phương thức: `is_consistent`, `backtrack` (đệ quy), `solve` (gọi ngoài)
class BacktrackingSolver:
    def __init__(self) -> None:
        # Khởi tạo bộ đếm cho một lần chạy `solve()`
        self.steps: int = 0
        self.constraint_checks: int = 0

    def is_consistent(self, csp, var: str, value: Any, assignment: Dict[str, Any]) -> bool:
        # Kiểm tra tính nhất quán của gán (var = value) so với các láng giềng đã có trong `assignment`.
        # Đồng thời tăng `constraint_checks` mỗi khi so sánh một ràng buộc.
        """Check consistency against assigned neighbors while counting checks."""
        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                self.constraint_checks += 1
                if not csp.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def backtrack(self, csp, assignment: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # Đệ quy Backtracking:
        # 1) Kiểm tra mục tiêu (tất cả biến đã được gán)
        # 2) Chọn biến chưa gán (chiến lược đơn giản: đầu danh sách)
        # 3) Thử từng giá trị trong miền, gán, đệ quy, nếu thất bại thì hủy gán (backtrack)
        if csp.is_complete(assignment):
            return assignment.copy()

        unassigned = csp.get_unassigned_variables(assignment)
        var = unassigned[0]

        for value in csp.get_domain(var):
            self.steps += 1
            if self.is_consistent(csp, var, value, assignment):
                csp.assign(var, value, assignment)
                result = self.backtrack(csp, assignment)
                if result is not None:
                    return result
                csp.unassign(var, assignment)

        return None

    def solve(self, csp) -> Tuple[Optional[Dict[str, Any]], int, int]:
        # Giao diện gọi: đặt lại bộ đếm, chạy backtracking, trả về (lời giải hoặc None, steps, constraint_checks)
        """Solve the given `csp` using backtracking.

        Returns a tuple: (solution|None, steps, constraint_checks)
        """
        self.steps = 0
        self.constraint_checks = 0

        solution = self.backtrack(csp, {})
        return solution, self.steps, self.constraint_checks
