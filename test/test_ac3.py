import os
import sys
import copy

# Thêm root project vào path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from algorithms.ac3 import ac3


class CSP:
    """
    Mock CSP để test

    Input:
        variables: list biến
        domains: dict {var: list/set}
        neighbors: dict {var: list biến kề}
    """
    def __init__(self, variables, domains, neighbors):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors


# =========================
# TEST 1: Giảm domain
# =========================
def test_case_1():
    variables = ["A", "B"]
    domains = {"A": ["Red"], "B": ["Red", "Green"]}
    neighbors = {"A": ["B"], "B": ["A"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    result = ac3(csp)

    assert result is True
    assert csp.domains["B"] == ["Green"]

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# TEST 2: Fail
# =========================
def test_case_2():
    variables = ["A", "B"]
    domains = {"A": ["Red"], "B": ["Red"]}
    neighbors = {"A": ["B"], "B": ["A"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    result = ac3(csp)

    assert result is False

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# TEST 3: Propagation
# =========================
def test_case_3():
    variables = ["A", "B", "C"]
    domains = {
        "A": ["Red"],
        "B": ["Red", "Green"],
        "C": ["Red", "Green"]
    }
    neighbors = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    ac3(csp)

    assert csp.domains["B"] == ["Green"]

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# TEST 4: Không đổi
# =========================
def test_case_4():
    variables = ["A", "B"]
    domains = {"A": ["Red", "Green"], "B": ["Red", "Green"]}
    neighbors = {"A": ["B"], "B": ["A"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    ac3(csp)

    assert csp.domains == domains

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# TEST 5: Domain dạng set
# =========================
def test_case_5():
    variables = ["A", "B"]
    domains = {"A": {"Red"}, "B": {"Red", "Green"}}
    neighbors = {"A": ["B"], "B": ["A"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    ac3(csp)

    assert csp.domains["B"] == {"Green"}

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# TEST 6: Custom constraint
# =========================
def test_case_6():
    variables = ["A", "B"]
    domains = {"A": ["Red"], "B": ["Red", "Green"]}
    neighbors = {"A": ["B"], "B": ["A"]}

    csp = CSP(variables, copy.deepcopy(domains), neighbors)

    ac3(csp, constraint=lambda x, y: x == y)

    assert csp.domains["B"] == ["Red"]

    # in ra để debug nếu test fail
    print("Domains sau AC3:", csp.domains)


# =========================
# RUN
# =========================
if __name__ == "__main__":
    test_case_1()
    test_case_2()
    test_case_3()
    test_case_4()
    test_case_5()
    test_case_6()

    print("=== ALL TESTS PASSED ===")