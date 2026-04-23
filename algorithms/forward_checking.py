from typing import Dict, Any, Optional, Tuple
from copy import deepcopy

from .ac3 import ac3


class ForwardCheckingSolver:
    """Backtracking with Forward-Checking and optional MAC (AC-3) maintenance.

    Usage:
        solver = ForwardCheckingSolver()
        solution, steps, checks = solver.solve(csp, mac=False)
    """

    def __init__(self) -> None:
        self.steps: int = 0
        self.constraint_checks: int = 0

    def _is_consistent(self, csp, var: str, value: Any, assignment: Dict[str, Any]) -> bool:
        # check against already-assigned neighbors and count checks
        for neighbor in csp.get_neighbors(var):
            if neighbor in assignment:
                self.constraint_checks += 1
                if not csp.constraint(var, value, neighbor, assignment[neighbor]):
                    return False
        return True

    def _forward_check(self, csp, var: str, value: Any) -> bool:
        """Perform forward-checking: prune neighbors' domains. Returns True if ok."""
        for neighbor in csp.get_neighbors(var):
            # only check unassigned neighbors
            # domains are mutable in csp.domains
            domain = csp.domains[neighbor]
            for val in list(domain):
                self.constraint_checks += 1
                if not csp.constraint(neighbor, val, var, value):
                    # remove incompatible value
                    try:
                        domain.remove(val)
                    except ValueError:
                        pass
            if len(domain) == 0:
                return False
        return True

    def backtrack(self, csp, assignment: Dict[str, Any], mac: bool) -> Optional[Dict[str, Any]]:
        if csp.is_complete(assignment):
            return assignment.copy()

        var = csp.get_unassigned_variables(assignment)[0]

        for value in list(csp.get_domain(var)):
            self.steps += 1
            if not self._is_consistent(csp, var, value, assignment):
                continue

            # save domains to restore on backtrack
            domains_backup = {v: list(vals) for v, vals in csp.domains.items()}

            # assign
            csp.assign(var, value, assignment)

            ok = True
            if mac:
                # run AC-3 (MAC): initialize queue with arcs (Xk, var)
                csp.domains[var] = [value]
                queue = [(Xk, var) for Xk in csp.get_neighbors(var)]
                ok = ac3(csp, queue=queue)
            else:
                # forward checking
                ok = self._forward_check(csp, var, value)

            if ok:
                result = self.backtrack(csp, assignment, mac)
                if result is not None:
                    return result

            # restore on failure
            csp.unassign(var, assignment)
            csp.domains = {v: list(vals) for v, vals in domains_backup.items()}

        return None

    def solve(self, csp, mac: bool = False) -> Tuple[Optional[Dict[str, Any]], int, int]:
        """Solve CSP using forward-checking or MAC.

        Returns (solution_or_None, steps, constraint_checks).
        """
        self.steps = 0
        self.constraint_checks = 0

        solution = self.backtrack(csp, {}, mac)
        return solution, self.steps, self.constraint_checks
