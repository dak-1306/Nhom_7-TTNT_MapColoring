class BacktrackingSolver:
    def _init_(self, variables, domains, adjacency):
        self.variables = variables
        self.domains = domains
        self.adjacency = adjacency
        self.steps = 0
        self.constraint_checks = 0
    def is_consistent(self, var, value, assignment):
        for neighbor in self.adjacency.get(var, []):
            self.constraint_checks += 1
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        return True