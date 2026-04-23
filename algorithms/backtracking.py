from typing import Dict, Any, Optional, Tuple


class BacktrackingSolver:
    def __init__(self) -> None:
        # counters collected during a single `solve()` run
        self.steps: int = 0
        self.constraint_checks: int = 0

    def is_consistent(self, csp, var: str, value: Any, assignment: Dict[str, Any]) -> bool:
        """Check consistency against assigned neighbors while counting checks."""
        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                self.constraint_checks += 1
                if not csp.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def backtrack(self, csp, assignment: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        # goal test
        if csp.is_complete(assignment):
            return assignment.copy()

        # select an unassigned variable (simple ordering)
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
        """Solve the given `csp` using backtracking.

        Returns a tuple: (solution|None, steps, constraint_checks)
        """
        # reset counters
        self.steps = 0
        self.constraint_checks = 0

        solution = self.backtrack(csp, {})
        return solution, self.steps, self.constraint_checks
