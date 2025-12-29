from typing import Dict, List
from sudoku import Sudoku

def print_grid(grid: List[List[int]]) -> None:
    for i, row in enumerate(grid):
        for j, num in enumerate(row):
            end_char = " "
            if (j + 1) % 3 == 0 and j != 8:
                end_char = " | "
            print(num, end=end_char)
        print()
        if (i + 1) % 3 == 0 and i != 8:
            print("-" * 21)

def grid_from_assignment(assignment: Dict[str, int], fixed: Dict[str, int]) -> List[List[int]]:
    full_values: Dict[str, int] = {**fixed}
    full_values.update(assignment)
    grid: List[List[int]] = []
    for r in range(9):
        row: List[int] = []
        for c in range(9):
            index = Sudoku.square_index(r, c)
            row.append(full_values.get(index, 0))
        grid.append(row)
    return grid
