sudokusolver
============

Converts ASCII sudoku to CNF then solves the CNF via MiniSAT

python

from solver import Sudoku

p = """
+-------+-------+-------+
| . 8 4 | . . 6 | . . 2 |
| . 2 . | . . 3 | . . 6 |
| . . 5 | . . . | . 4 . |
+-------+-------+-------+
| 5 . 3 | 8 . . | 2 . . |
| 7 4 . | 9 . 2 | . 6 5 |
| . . 2 | . . 5 | 9 . 7 |
+-------+-------+-------+
| . 3 . | . . . | 1 . . |
| 2 . . | 6 . . | . 7 . |
| 8 . . | 2 . . | 6 5 . |
+-------+-------+-------+"""

sol = Sudoku(p)

#print solution
sol.solve()

# print all cases
sol.get_dimacs()
