from sudoku import Sudoku
from csp import backtracking_search
from util import print_grid, grid_from_assignment

start_grid = [
    [0, 0, 0, 2, 0, 0, 0, 6, 3],
    [3, 0, 0, 0, 0, 5, 4, 0, 1],
    [0, 0, 1, 0, 0, 3, 9, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 9, 0],
    [0, 0, 0, 5, 3, 8, 0, 0, 0],
    [0, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 6, 3, 0, 0, 5, 0, 0],
    [5, 0, 3, 0, 0, 0, 0, 0, 8],
    [9, 0, 0, 0, 0, 1, 0, 0, 0],
]

filled_cells = {
    Sudoku.square_index(r, c): start_grid[r][c]
    for r in range(9)
    for c in range(9)
    if start_grid[r][c] != 0
}

sudoku = Sudoku(filled_cells)

print("Initial puzzle:")
print_grid(start_grid)

solution = backtracking_search(sudoku)
if solution is None:
    print("\nNo solution found.")
else:
    print("\nSolved puzzle:")
    solved_grid = grid_from_assignment(solution, sudoku.filled)
    print_grid(solved_grid)
