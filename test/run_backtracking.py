import json
import os

here = os.path.dirname(__file__)
# data is in the repository root `data/` — go up one level from `test/`
root = os.path.abspath(os.path.join(here, '..'))
provinces_path = os.path.join(root, 'data', 'vietnam_provinces.json')
adj_path = os.path.join(root, 'data', 'adjacency.json')

with open(provinces_path, encoding='utf-8') as f:
    data = json.load(f)
provinces = data['provinces']
colors = data['colors']

with open(adj_path, encoding='utf-8') as f:
    adjacency = json.load(f)

# build domains
domains = {p: list(colors) for p in provinces}

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
