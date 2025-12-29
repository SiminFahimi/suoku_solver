from __future__ import annotations
from copy import deepcopy
from typing import Callable, Dict, List, Optional, Tuple

class CSP:
    """Generic Constraint Satisfaction Problem (CSP) base class."""

    def __init__(
        self,
        variables: List[str],
        domains: Dict[str, List[int]],
        constraints: Callable[[str, int, str, int], bool],
        neighbors: Dict[str, List[str]],
    ) -> None:
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.neighbors = neighbors

def ac3(csp: CSP) -> bool:
    """AC-3 algorithm for arc consistency."""
    queue: List[Tuple[str, str]] = [
        (x, y) for x in csp.variables for y in csp.neighbors.get(x, [])
    ]
    while queue:
        x, y = queue.pop(0)
        if _revise(csp, x, y):
            if not csp.domains[x]:
                return False
            for k in csp.neighbors.get(x, []):
                if k != y and (k, x) not in queue:
                    queue.append((k, x))
    return True

def _revise(csp: CSP, x: str, y: str) -> bool:
    revised = False
    original_domain = list(csp.domains[x])
    for dx in original_domain:
        if not any(csp.constraints(x, dx, y, dy) for dy in csp.domains[y]):
            csp.domains[x].remove(dx)
            revised = True
    return revised

def backtracking_search(csp: CSP) -> Optional[Dict[str, int]]:
    return _backtrack({}, csp)

def _backtrack(assignment: Dict[str, int], csp: CSP) -> Optional[Dict[str, int]]:
    if len(assignment) == len(csp.variables):
        return assignment

    var = _mrv_heuristic(assignment, csp)
    if var is None:
        return None

    for value in csp.domains[var]:
        if _is_consistent(var, value, assignment, csp):
            assignment[var] = value
            csp_copy = deepcopy(csp)
            csp_copy.domains[var] = [value]

            if ac3(csp_copy):
                result = _backtrack(assignment, csp_copy)
                if result is not None:
                    return result

            del assignment[var]
    return None

def _is_consistent(var: str, value: int, assignment: Dict[str, int], csp: CSP) -> bool:
    for x in assignment:
        if var in csp.neighbors.get(x, []):
            if not csp.constraints(var, value, x, assignment[x]):
                return False
    return True

def _mrv_heuristic(assignment: Dict[str, int], csp: CSP) -> Optional[str]:
    unassigned = [v for v in csp.variables if v not in assignment]
    if not unassigned:
        return None
    return min(unassigned, key=lambda v: len(csp.domains[v]))
