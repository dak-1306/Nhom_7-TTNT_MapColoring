import sys
import os

# Ensure project root is on sys.path so we can import the algorithms module
here = os.path.dirname(__file__)
root = os.path.abspath(os.path.join(here, '..'))
if root not in sys.path:
    sys.path.insert(0, root)

from algorithms.csp import create_map_coloring_csp

# Load CSP (uses data/*.json by default) and extract variables/domains/neighbors
csp = create_map_coloring_csp()
provinces = csp.variables
domains = csp.domains
adjacency = csp.neighbors

constraint_checks = 0

def is_consistent(var, value, assignment):
    global constraint_checks
    for neighbor in adjacency.get(var, []):
        constraint_checks += 1
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True


def backtrack(assignment):
    if len(assignment) == len(provinces):
        return assignment
    # select unassigned variable (simple ordering)
    unassigned = [v for v in provinces if v not in assignment]
    var = unassigned[0]
    for value in domains[var]:
        if is_consistent(var, value, assignment):
            assignment[var] = value
            result = backtrack(assignment)
            if result:
                return result
            del assignment[var]
    return None

if __name__ == '__main__':
    solution = backtrack({})
    if solution:
        print('Found solution:')
        for p in provinces:
            print(f"{p}: {solution[p]}")
        print(f"Constraint checks: {constraint_checks}")
    else:
        print('No solution found')
