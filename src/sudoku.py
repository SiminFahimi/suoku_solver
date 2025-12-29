from __future__ import annotations
from typing import Dict, List
from csp import CSP

class Sudoku(CSP):
    """Sudoku CSP specialization using AC-3 and backtracking."""

    def __init__(self, filled: Dict[str, int]) -> None:
        self.filled = filled
        squares = [str(i) for i in range(81)]
        domains: Dict[str, List[int]] = {
            s: self._compute_domain(s, filled) for s in squares if s not in filled
        }

        regions: Dict[str, List[str]] = {
            f"region{i}": [
                str(3 * (i // 3) * 9 + (i % 3) * 3 + j)
                for j in [0, 1, 2, 9, 10, 11, 18, 19, 20]
            ]
            for i in range(9)
        }
        cols: Dict[str, List[str]] = {f"col{j}": [str(j + 9 * i) for i in range(9)] for j in range(9)}
        rows: Dict[str, List[str]] = {f"row{i}": [str(i * 9 + j) for j in range(9)] for i in range(9)}

        neighbors = self._build_neighbors(squares, rows, cols, regions)
        variables = [s for s in squares if s not in self.filled]
        super().__init__(variables, domains, self.is_valid, neighbors)

    @staticmethod
    def square_index(row: int, col: int) -> str:
        return str(9 * row + col)

    @staticmethod
    def row_of(square: str) -> int:
        return int(square) // 9

    @staticmethod
    def col_of(square: str) -> int:
        return int(square) % 9

    @staticmethod
    def region_of(square: str) -> int:
        return (int(square) // 27) * 3 + (int(square) % 9 // 3)

    def _compute_domain(self, square: str, filled: Dict[str, int]) -> List[int]:
        candidates = list(range(1, 10))
        for s, value in filled.items():
            same_row = self.row_of(s) == self.row_of(square)
            same_col = self.col_of(s) == self.col_of(square)
            same_region = self.region_of(s) == self.region_of(square)
            if (same_row or same_col or same_region) and value in candidates:
                candidates.remove(value)
        return candidates

    def _build_neighbors(
        self, variables: List[str], rows: Dict[str, List[str]],
        cols: Dict[str, List[str]], regions: Dict[str, List[str]]
    ) -> Dict[str, List[str]]:
        neighbors: Dict[str, List[str]] = {}
        for square in variables:
            if square in self.filled:
                continue
            r = self.row_of(square)
            c = self.col_of(square)
            reg = self.region_of(square)
            neighbor_set = set(rows[f"row{r}"] + cols[f"col{c}"] + regions[f"region{reg}"])
            neighbor_set.discard(square)
            neighbor_set -= set(self.filled.keys())
            neighbors[square] = list(neighbor_set)
        return neighbors

    def is_valid(self, x: str, vx: int, y: str, vy: int) -> bool:
        if y in self.neighbors.get(x, []):
            return vx != vy
        return True
